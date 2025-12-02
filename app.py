import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(200) NOT NULL
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            value FLOAT NOT NULL,
            description VARCHAR(200),
            reason VARCHAR(50) NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            type VARCHAR(10) NOT NULL,
            date_created TIMESTAMP NOT NULL DEFAULT NOW(),
            user_id INTEGER NOT NULL REFERENCES users(id)
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "API funcionando SEM SQLAlchemy!"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        return jsonify({"message": "Nome de usuário já existe!"}), 400

    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;",
        (username, password),
    )
    user_id = cur.fetchone()["id"]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Usuário criado com sucesso!", "user_id": user_id}), 201



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()


    if user and user["password_hash"] == password:
        return jsonify(
            {
                "message": "Login bem-sucedido!",
                "user_id": user["id"],
                "username": user["username"],
            }
        )
    else:
        return jsonify({"message": "Credenciais inválidas!"}), 401


@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"message": "user_id obrigatório!"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO transactions (value, description, reason, payment_method, type, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (
            data["value"],
            data["description"],
            data["reason"],
            data["payment_method"],
            data["type"],
            data["user_id"],
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Transação adicionada com sucesso!"}), 201


@app.route("/transactions/<int:user_id>", methods=["GET"])
def get_transactions(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM transactions 
        WHERE user_id = %s 
        ORDER BY date_created DESC
    """,
        (user_id,),
    )

    transactions = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(transactions)


@app.route("/balance/<int:user_id>", methods=["GET"])
def get_balance(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT type, value FROM transactions WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    balance = sum(r["value"] if r["type"] == "entrada" else -r["value"] for r in rows)

    return jsonify({"balance": balance})


@app.route("/charts/expense_by_reason/<int:user_id>", methods=["GET"])
def get_expense_chart_data(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT reason, COUNT(id) AS total
        FROM transactions
        WHERE user_id = %s AND type = 'saida'
        GROUP BY reason;
    """,
        (user_id,),
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    chart_data = [
        {
            "name": row["reason"],
            "population": row["total"],
            "color": getRandomColor(),
            "legendFontColor": "#333",
            "legendFontSize": 12,
        }
        for row in rows
    ]

    return jsonify(chart_data)


def getRandomColor():
    import random

    return f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
