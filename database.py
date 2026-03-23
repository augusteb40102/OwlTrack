import sqlite3
import os
import sys
import bcrypt

if getattr(sys, 'frozen', False):
    # .exe - eik vienu lygiu aukštyn iš dist/ į projekto aplanką
    BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
else:
    # python main.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "owltrack.db")

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
            avatar_src  TEXT DEFAULT NULL,
            theme       TEXT DEFAULT 'purple',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT NOT NULL,
            token       TEXT NOT NULL UNIQUE,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at  TIMESTAMP NOT NULL,
            used        BOOLEAN DEFAULT 0,
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)

    for column, definition in [
        ("avatar_src", "TEXT DEFAULT NULL"),
        ("theme",      "TEXT DEFAULT 'purple'"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")
        except Exception:
            pass

    conn.commit()
    conn.close()
    print("Duomenų bazė paruošta.")

def register_user(name: str, email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "error": "An account with this email already exists"}
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed.decode("utf-8"))
    )
    conn.commit()
    conn.close()
    return {"success": True}

def save_avatar(email: str, avatar_src: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET avatar_src = ? WHERE email = ?", (avatar_src, email))
    conn.commit()
    conn.close()

def save_theme(email: str, theme: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET theme = ? WHERE email = ?", (theme, email))
    conn.commit()
    conn.close()

def get_theme(email: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT theme FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row["theme"] if row and row["theme"] else "purple"

def login_user(email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return {"success": False, "error": "Account with this email does not exist"}
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"success": False, "error": "Incorrect password"}
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "avatar_src": user["avatar_src"],
            "theme": user["theme"] if user["theme"] else "purple",
        }
    }

def change_user_password(email: str, old_password: str, new_password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user or not bcrypt.checkpw(old_password.encode("utf-8"), user["password"].encode("utf-8")):
            conn.rollback()
            return {"success": False, "error": "Unable to update password"}
        new_hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_hashed, email))
        conn.commit()
        return {"success": True}
    except Exception:
        conn.rollback()
        return {"success": False, "error": "Unable to update password"}
    finally:
        conn.close()

def email_exists(email: str) -> bool:
    """Patikrina ar el. pašto adresas egzistuoja duomenų bazėje"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone() is not None
    conn.close()
    return result

def delete_old_tokens(email: str) -> None:
    """Panaikina visus senus reset tokenus tam tikram emailui"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM password_reset_tokens WHERE email = ?", (email,))
    conn.commit()
    conn.close()

def save_reset_token(email: str, token: str, expires_at: str) -> bool:
    """Išsaugo reset tokeną duomenų bazėje. Panaikina senus tokenus tos pašto adreso."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Panaikinti senus tokus
        delete_old_tokens(email)
        
        # Saugoti naujasis token
        cursor.execute(
            "INSERT INTO password_reset_tokens (email, token, expires_at) VALUES (?, ?, ?)",
            (email, token, expires_at)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Klaida saugant reset tokeną: {e}")
        return False