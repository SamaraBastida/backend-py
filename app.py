import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuração do Banco (PostgreSQL no Railway ou SQLite local)
db_url = os.getenv("DATABASE_URL")

if db_url:
    # Railway usa postgres:// mas SQLAlchemy exige postgresql://
    db_url = db_url.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    # Ambiente local
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    reason = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'entrada' ou 'saida'
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "HOLA"})

# API - METODOS
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Nome de usuário já existe!"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso!", "user_id": new_user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return jsonify({
            "message": "Login bem-sucedido!",
            "user_id": user.id,
            "username": user.username
        }), 200
    else:
        return jsonify({"message": "Credenciais inválidas!"}), 401

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    user_id = data.get('user_id')
    value = data.get('value')
    description = data.get('description')
    reason = data.get('reason')
    payment_method = data.get('payment_method')
    type = data.get('type') # entrada ou saida

    new_transaction = Transaction(
        value=value,
        description=description,
        reason=reason,
        payment_method=payment_method,
        type=type,
        user_id=user_id
    )
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({"message": "Transação adicionada com sucesso!"}), 201

@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date_created.desc()).all()
    return jsonify([{
        "id": t.id,
        "value": t.value,
        "description": t.description,
        "reason": t.reason,
        "payment_method": t.payment_method,
        "type": t.type,
        "date_created": t.date_created
    } for t in transactions]), 200

@app.route('/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    balance = 0.0
    for t in transactions:
        if t.type == 'entrada':
            balance += t.value
        else:
            balance -= t.value
    return jsonify({"balance": balance}), 200

@app.route('/charts/expense_by_reason/<int:user_id>', methods=['GET'])
def get_expense_chart_data(user_id):
    # Filtra apenas as saídas e agrupa por motivo
    expenses = db.session.query(Transaction.reason, db.func.count(Transaction.id)).filter_by(user_id=user_id, type='saida').group_by(Transaction.reason).all()
    
    chart_data = []
    for reason, count in expenses:
        chart_data.append({
            "name": reason,
            "population": count,
            "color": getRandomColor(),
            "legendFontColor": "#333",
            "legendFontSize": 12
        })
    
    return jsonify(chart_data), 200

def getRandomColor():
    import random
    return f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

