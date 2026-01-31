# 📦 StockMaster 

StockMaster est une application web de **gestion d’inventaire** moderne et sécurisée, développée avec **FastAPI**.  
Elle permet de gérer des produits, suivre les stocks en temps réel et enregistrer toutes les transactions.

---
### 🔐 Authentification
| Connexion | Création de Compte |
|-----------|--------------------|
| ![Login Page](screenshots/login.png) | ![Register Page](screenshots/create_account.png) |

### 📊 Tableau de Bord & Stocks
![Dashboard](screenshots/dashboard.png)

### 📜 Historique des Transactions
![Transactions](screenshots/transactions.png)

## ✨ Features

- 📊 Dashboard avec statistiques globales
- 🧾 CRUD complet des produits
- 🔄 Vente et réapprovisionnement de stock
- 🚨 Alerte visuelle pour stock faible (≤ 5)
- 📜 Historique des transactions
- 🔐 Authentification sécurisée avec JWT

---

## 🛠 Tech Stack

- **Backend** : FastAPI (Python)
- **Database** : SQLite + SQLAlchemy
- **Frontend** : HTML, CSS (Bootstrap 5), JavaScript
- **Auth & Security** : JWT, Passlib (bcrypt)

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/TON_PSEUDO/stock-master-pro.git
cd stock-master-pro

# Create virtual environment
python -m venv venv

# Activate venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
````

📍 Open your browser at:
👉 `http://127.0.0.1:8000`

---

## 📁 Project Structure

```text
app/
├── crud/           # Business logic
├── routes/         # API endpoints
├── models.py       # Database models
├── schemas.py      # Pydantic schemas
├── database.py     # DB configuration
├── screenshots     # website screeshots
└── main.py         # App entry point

static/             # CSS & JavaScript
templates/          # HTML templates
requirements.txt
README.md
```

---

## 🔐 Authentication

* JSON Web Tokens (JWT)
* Password hashing with bcrypt
* Protected API routes

---

## 👤 Author

**Karim El GHMARI**
Engineering Student – ENSAM Casablanca


