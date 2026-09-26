# url_shortener

# 🔗 URL Shortener

A simple full-stack **URL Shortener web application** built with FastAPI and SQLAlchemy. 
It converts long URLs into short, easy-to-share links and provides basic URL management and click tracking.

## 🚀 Features

* Create shortened URLs
* Generate unique short URL keys
* Generate a private secret key for URL management
* Validate target URLs
* Redirect short URLs to the original URL
* Track URL clicks
* View created URLs in a dashboard
* Deactivate shortened URLs
* Reactivate deactivated URLs
* Prevent access to deactivated URLs
* Automatically remove deactivated URLs after 7 days

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Validation:** Pydantic, Validators
* **Frontend:** HTML, CSS, JavaScript
* **Templates:** Jinja2
* **Package Management:** uv

## 📌 How It Works

1. User enters a long URL.
2. The application validates the URL.
3. A unique short key is generated.
4. A private secret key is generated for URL management.
5. URL details are stored in the database.
6. The user receives a shortened URL.
7. When the shortened URL is visited, the application redirects the user to the original URL and increments the click count.

### URL Management

Each shortened URL has:

* **Short Key** — Used to access the shortened URL.
* **Secret Key** — Used to deactivate or reactivate the URL.

Deactivated URLs cannot be accessed and are scheduled for permanent deletion after 7 days.

## 📂 Project Structure

```text
url-shortener/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── keygen.py
│   └── config.py
│
├── templates/
│   ├── layout.html
│   └── home.html
│
├── static/
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Go to the project directory:

```bash
cd YOUR-REPOSITORY
```

Install dependencies using `uv`:

```bash
uv sync
```

## ▶️ Run the Application

Start the FastAPI server:

```bash
uv run uvicorn app.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

## 📖 API Documentation

FastAPI provides interactive API documentation:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## 🔐 Environment Variables

If environment variables are required, create a `.env` file in the project root.

Example:

```env
BASE_URL=http://127.0.0.1:8000
```
The `.env` file should not be committed to GitHub.

## 🗄️ Database

The project currently uses **SQLite** for local development.

The database file is excluded from the Git repository using `.gitignore`.

## 🔮 Future Improvements

* User authentication
* Custom short URLs
* QR code generation
* URL analytics
* PostgreSQL support
* Rate limiting
* Cloud deployment
* Improved favicon support


GitHub: https://github.com/YOUR-USERNAME
