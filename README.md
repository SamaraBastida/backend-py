# API Flask + PostgreSQL (Railway)

Este projeto é uma API desenvolvida em **Flask**, utilizando **SQLAlchemy** como ORM e **PostgreSQL** hospedado no Railway.

---

## Tecnologias utilizadas

- Python 3.x
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PostgreSQL (Railway)

---

## Estrutura do projeto

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

## Configuração local

### 1️ Criar e ativar o ambiente virtual

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

### 2️ Instalar as dependências

```
pip install -r requirements.txt
```

---

### 3️ Criar arquivo `.env`

Dentro do arquivo `.env`, coloque:

```
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_do_banco
FLASK_ENV=development
```

## Executar o projeto

```
python app.py
```

A API ficará disponível em:

```
http://localhost:5000
```


## Manutenção

### Atualizar o requirements.txt

```
pip freeze > requirements.txt
```

