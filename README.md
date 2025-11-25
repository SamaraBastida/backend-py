# 🚀 API Flask + PostgreSQL (Railway)

Este projeto é uma API simples desenvolvida em **Flask**, utilizando **SQLAlchemy** como ORM e **PostgreSQL** hospedado no Railway.

---

## 📦 Tecnologias utilizadas

- Python 3.x
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PostgreSQL (Railway)

---

## 📁 Estrutura do projeto

```
.
├── app.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🔧 Configuração local

### 1️⃣ Criar e ativar o ambiente virtual

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```
python3 -m venv venv
source venv/bin/activate
```

---

### 2️⃣ Instalar as dependências

```
pip install -r requirements.txt
```

---

### 3️⃣ Criar arquivo `.env`

Dentro do arquivo `.env`, coloque:

```
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_do_banco
FLASK_ENV=development
```

O arquivo `.env` já está no `.gitignore`, então ele não será enviado ao GitHub.

---

## ▶️ Executar o projeto

```
python app.py
```

A API ficará disponível em:

```
http://localhost:5000
```

---

## 🚀 Deploy no Railway

### 1️⃣ Criar serviço no Railway

- Acesse: [https://railway.app](https://railway.app)
- Clique em **New → Project → Deploy from GitHub Repository**
- Escolha o seu repositório

---

### 2️⃣ Configurar variáveis no Railway

No menu **Variables**, adicione:

```
DATABASE_URL=postgresql://postgres:SENHA@HOST:5432/railway
```

---

### 3️⃣ Deploy automático

Sempre que você fizer `git push`, o Railway fará o deploy automaticamente.

---

## 🔍 Rotas de Exemplo

| Método | Rota     | Descrição      |
| ------ | -------- | -------------- |
| GET    | `/`      | Teste da API   |
| GET    | `/users` | Lista usuários |
| POST   | `/users` | Cria usuário   |

---

## 🛠 Manutenção

### 📜 Atualizar o requirements.txt

```
pip freeze > requirements.txt
```

---

## 📄 Licença

Este projeto é livre para uso educacional.

---

## 🧑‍💻 Autor

Projeto criado com apoio do ChatGPT 🤖
