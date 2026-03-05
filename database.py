import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "owltrack.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL UNIQUE,
            password    TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Duomenų bazė paruošta.")

def register_user(name: str, email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    # Tikriname ar el. paštas jau egzistuoja
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "error": "An account with this email already exists"}

    # Užkoduojame slaptažodį
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Išsaugome vartotoją
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed.decode("utf-8"))
    )

    conn.commit()
    conn.close()
    return {"success": True}