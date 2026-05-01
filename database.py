import sqlite3
import os
import sys
import bcrypt
import shutil
from datetime import datetime, date, timedelta

def _get_app_data_dir() -> str:
    """Grąžina pastovų OwlTrack duomenų katalogą pagal OS."""
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "OwlTrack")
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        if appdata:
            return os.path.join(appdata, "OwlTrack")
    return os.path.join(os.path.expanduser("~"), ".owltrack")


def _get_legacy_db_path() -> str:
    if getattr(sys, 'frozen', False):
        legacy_base_dir = os.path.dirname(os.path.dirname(sys.executable))
    else:
        legacy_base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(legacy_base_dir, "owltrack.db")


APP_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DATA_DIR, "owltrack.db")

LEGACY_DB_PATH = _get_legacy_db_path()
if not os.path.exists(DB_PATH) and os.path.exists(LEGACY_DB_PATH):
    try:
        shutil.copy2(LEGACY_DB_PATH, DB_PATH)
    except Exception:
        pass

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
    except Exception:
        pass
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    def ensure_column(table: str, column: str, definition: str):
        cursor.execute(f"PRAGMA table_info({table})")
        existing_columns = {row[1] for row in cursor.fetchall()}
        if column not in existing_columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            entry_date  TEXT NOT NULL,
            activity    TEXT,
            mood        TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email    TEXT NOT NULL,
            title         TEXT NOT NULL,
            type          TEXT NOT NULL DEFAULT 'Assignment',
            due_date      TEXT NOT NULL,
            completed     INTEGER NOT NULL DEFAULT 0,
            completed_at  TEXT DEFAULT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_email ON tasks(user_email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_completed_at ON tasks(completed_at)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grade_modules (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            name        TEXT NOT NULL,
            ects        REAL NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grade_assessments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id   INTEGER NOT NULL,
            type        TEXT NOT NULL,
            grade       REAL NOT NULL,
            weight      REAL,
            FOREIGN KEY (module_id) REFERENCES grade_modules(id) ON DELETE CASCADE
        )
    """)

    for column, definition in [
        ("user_email", "TEXT NOT NULL DEFAULT ''"),
        ("title", "TEXT NOT NULL DEFAULT ''"),
        ("type", "TEXT NOT NULL DEFAULT 'Assignment'"),
        ("due_date", "TEXT NOT NULL DEFAULT ''"),
        ("completed", "INTEGER NOT NULL DEFAULT 0"),
        ("completed_at", "TEXT DEFAULT NULL"),
        ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
    ]:
        try:
            ensure_column("tasks", column, definition)
        except Exception:
            pass

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

    # Ensure modules/assessments tables exist
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            name        TEXT NOT NULL,
            ects        REAL NOT NULL DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_modules_user_email ON modules(user_email)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id  INTEGER NOT NULL,
            type       TEXT,
            grade      REAL,
            weight     REAL,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_module_id ON assessments(module_id)")
    conn.commit()
    conn.close()

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


def save_grade_modules(user_email: str, modules: list[dict]) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM grade_assessments WHERE module_id IN (SELECT id FROM grade_modules WHERE user_email = ?)",
        (user_email,)
    )
    cursor.execute("DELETE FROM grade_modules WHERE user_email = ?", (user_email,))

    for module in modules:
        cursor.execute(
            "INSERT INTO grade_modules (user_email, name, ects) VALUES (?, ?, ?)",
            (user_email, module.get("name", ""), module.get("ects", 0.0))
        )
        module_id = cursor.lastrowid
        for assessment in module.get("assessments", []):
            cursor.execute(
                "INSERT INTO grade_assessments (module_id, type, grade, weight) VALUES (?, ?, ?, ?)",
                (module_id, assessment.get("type", ""), assessment.get("grade", 0.0), assessment.get("weight"))
            )

    conn.commit()
    conn.close()


def load_grade_modules(user_email: str) -> list[dict]:
    if not user_email:
        return []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, ects FROM grade_modules WHERE user_email = ? ORDER BY id",
        (user_email,)
    )
    modules = []
    for row in cursor.fetchall():
        module_id = row["id"]
        cursor.execute(
            "SELECT type, grade, weight FROM grade_assessments WHERE module_id = ? ORDER BY id",
            (module_id,)
        )
        assessments = [
            {"type": a["type"], "grade": a["grade"], "weight": a["weight"]}
            for a in cursor.fetchall()
        ]
        modules.append({"name": row["name"], "ects": row["ects"], "assessments": assessments})

    conn.close()
    return modules


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

def save_calendar_entry(user_email: str, entry_date: str, activity: str, mood: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    # Check if entry already exists
    cursor.execute("""
        SELECT rowid FROM calendar_entries
        WHERE user_email = ? AND entry_date = ?
    """, (user_email, entry_date))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing entry
        cursor.execute("""
            UPDATE calendar_entries
            SET activity = ?, mood = ?
            WHERE user_email = ? AND entry_date = ?
        """, (activity, mood, user_email, entry_date))
    else:
        # Insert new entry
        cursor.execute("""
            INSERT INTO calendar_entries (user_email, entry_date, activity, mood)
            VALUES (?, ?, ?, ?)
        """, (user_email, entry_date, activity, mood))
    
    conn.commit()
    conn.close()
    return {"success": True}

def get_calendar_entries(user_email: str, entry_date: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT activity, mood FROM calendar_entries
        WHERE user_email = ? AND entry_date = ?
    """, (user_email, entry_date))
    rows = cursor.fetchall()
    conn.close()
    return [{"activity": r["activity"], "mood": r["mood"]} for r in rows]

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


def list_modules(user_email: str) -> list[dict]:
    """Grąžina vartotojo modulius su jų įvertinimais."""
    if not user_email:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, ects
        FROM modules
        WHERE user_email = ?
        ORDER BY id ASC
        """,
        (user_email,)
    )
    rows = cursor.fetchall()
    modules = []
    for row in rows:
        cursor.execute(
            "SELECT type, grade, weight FROM assessments WHERE module_id = ? ORDER BY id ASC",
            (row["id"],),
        )
        assess_rows = cursor.fetchall()
        assessments = [
            {"type": a["type"], "grade": (a["grade"] if a["grade"] is not None else None), "weight": (a["weight"] if a["weight"] is not None else None)}
            for a in assess_rows
        ]
        modules.append({"id": row["id"], "name": row["name"], "ects": row["ects"], "assessments": assessments})
    conn.close()
    return modules


def create_module(user_email: str, name: str, ects: float, assessments: list[dict]) -> dict:
    if not user_email:
        return {"success": False, "error": "missing_user_email"}
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        cursor.execute(
            "INSERT INTO modules (user_email, name, ects) VALUES (?, ?, ?)",
            (user_email, name, ects),
        )
        module_id = cursor.lastrowid
        for a in assessments:
            cursor.execute(
                "INSERT INTO assessments (module_id, type, grade, weight) VALUES (?, ?, ?, ?)",
                (module_id, a.get("type"), a.get("grade"), a.get("weight")),
            )
        conn.commit()
        return {"success": True, "module_id": module_id}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def update_module(module_id: int, user_email: str, name: str, ects: float, assessments: list[dict]) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        # Verify ownership
        cursor.execute("SELECT user_email FROM modules WHERE id = ?", (module_id,))
        row = cursor.fetchone()
        if not row or row["user_email"] != user_email:
            conn.rollback()
            return {"success": False, "error": "not_allowed"}
        cursor.execute(
            "UPDATE modules SET name = ?, ects = ? WHERE id = ?",
            (name, ects, module_id),
        )
        # Replace assessments: delete old, insert new
        cursor.execute("DELETE FROM assessments WHERE module_id = ?", (module_id,))
        for a in assessments:
            cursor.execute(
                "INSERT INTO assessments (module_id, type, grade, weight) VALUES (?, ?, ?, ?)",
                (module_id, a.get("type"), a.get("grade"), a.get("weight")),
            )
        conn.commit()
        return {"success": True}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def delete_module(module_id: int, user_email: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM modules WHERE id = ? AND user_email = ?",
            (module_id, user_email),
        )
        conn.commit()
        return {"success": cursor.rowcount > 0}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()

def email_exists(email: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone() is not None
    conn.close()
    return result

def delete_old_tokens(email: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM password_reset_tokens WHERE email = ?", (email,))
    conn.commit()
    conn.close()

def save_reset_token(email: str, token: str, expires_at: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        delete_old_tokens(email)
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

def verify_reset_token(token: str) -> dict:
    """
    Patikrina ar reset tokenas galioja.
    Returns:
        {"valid": True,  "email": str}   – tokenas geras
        {"valid": False, "reason": str}  – tokenas blogas
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, expires_at, used FROM password_reset_tokens WHERE token = ?",
        (token,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"valid": False, "reason": "invalid"}

    if row["used"]:
        return {"valid": False, "reason": "already_used"}

    expires_at = datetime.fromisoformat(row["expires_at"])
    if datetime.now() > expires_at:
        return {"valid": False, "reason": "expired"}

    return {"valid": True, "email": row["email"]}

def mark_token_used(token: str) -> None:
    """Pažymi tokeną kaip panaudotą po sėkmingo slaptažodžio keitimo."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE password_reset_tokens SET used = 1 WHERE token = ?",
        (token,)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email: str) -> dict | None:
    """Grąžina vartotojo duomenis pagal email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return None
    return {
        "id":         user["id"],
        "name":       user["name"],
        "email":      user["email"],
        "avatar_src": user["avatar_src"],
        "theme":      user["theme"] if user["theme"] else "purple",
    }

def get_user_by_email(email: str) -> dict | None:
    """Grąžina vartotojo duomenis pagal email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return None
    return {
        "id":         user["id"],
        "name":       user["name"],
        "email":      user["email"],
        "avatar_src": user["avatar_src"],
        "theme":      user["theme"] if user["theme"] else "purple",
    }

def set_password_from_token(email: str, plain_password: str) -> bool:
    """
    Išsaugo laikiną kodą kaip naują hash'intą slaptažodį.
    Vartotojas gali prisijungti su šiuo kodu kol nepakeis slaptažodžio per Settings.
    """
    import bcrypt
    try:
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Klaida išsaugant laikiną slaptažodį: {e}")
        return False


def list_user_tasks(user_email: str) -> list[dict]:
    """Grąžina vartotojo užduotis, surikiuotas pagal terminą ir id."""
    if not user_email:
        return []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, type, due_date, completed, completed_at
        FROM tasks
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (user_email,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "type": row["type"],
            "due_date": row["due_date"],
            "completed": bool(row["completed"]),
            "completed_at": row["completed_at"],
        }
        for row in rows
    ]


def create_task(user_email: str, title: str, task_type: str, due_date: str) -> dict:
    """Sukuria naują vartotojo užduotį."""
    if not user_email:
        return {"success": False, "error": "missing_user_email"}

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO tasks (user_email, title, type, due_date, completed, completed_at)
            VALUES (?, ?, ?, ?, 0, NULL)
            """,
            (user_email, title, task_type, due_date),
        )
        conn.commit()
        return {"success": True, "task_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def update_task(task_id: int, user_email: str, title: str, task_type: str, due_date: str) -> dict:
    """Atnaujina vartotojo užduoties bazinius laukus."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET title = ?,
                type = ?,
                due_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_email = ?
            """,
            (title, task_type, due_date, task_id, user_email),
        )
        conn.commit()
        return {"success": cursor.rowcount > 0}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def delete_task(task_id: int, user_email: str) -> dict:
    """Ištrina vartotojo užduotį."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_email = ?",
            (task_id, user_email),
        )
        conn.commit()
        return {"success": cursor.rowcount > 0}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def set_task_completed(task_id: int, user_email: str, completed: bool, completed_at: str | None = None) -> dict:
    """Pažymi užduotį atlikta / neatlikta, atnaujina completed_at."""
    completed_at_value = None
    if completed:
        completed_at_value = completed_at or date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET completed = ?,
                completed_at = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_email = ?
            """,
            (1 if completed else 0, completed_at_value, task_id, user_email),
        )
        conn.commit()
        return {"success": cursor.rowcount > 0}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def _parse_iso_date(value: str | None):
    if not value:
        return None
    value = str(value).strip()
    if not value:
        return None

    # Primary format used in tasks: YYYY-MM-DD
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except Exception:
        pass

    # Fallback for full ISO strings
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return None


def _empty_monthly_task_stats(year: int, month: int, upcoming_window_days: int = 7) -> dict:
    weekday_labels = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return {
        "month": f"{year:04d}-{month:02d}",
        "totals": {
            "all_tasks": 0,
            "completed_tasks": 0,
            "completion_percent": 0.0,
        },
        "deadlines": {
            "overdue_tasks": 0,
            "upcoming_tasks": 0,
            "upcoming_window_days": upcoming_window_days,
        },
        "streak": {
            "current_days": 0,
        },
        "weekday_productivity": [
            {"day": day, "tasks": 0} for day in weekday_labels
        ],
        "most_productive_day": {
            "day": None,
            "tasks": 0,
        },
    }


def get_monthly_task_statistics(user_email: str, year: int, month: int, upcoming_window_days: int = 7) -> dict:
    """
    Apskaičiuoja vartotojo mėnesinę užduočių statistiką ir grąžina GUI tinkamą formatą.

    Grąžinimo formatas:
    {
        "month": "YYYY-MM",
        "totals": {
            "all_tasks": int,
            "completed_tasks": int,
            "completion_percent": float,
        },
        "deadlines": {
            "overdue_tasks": int,
            "upcoming_tasks": int,
            "upcoming_window_days": int,
        },
        "streak": {"current_days": int},
        "weekday_productivity": [
            {"day": "Monday", "tasks": int}, ...
        ],
        "most_productive_day": {
            "day": str | None,
            "tasks": int,
        },
    }
    """
    try:
        year = int(year)
        month = int(month)
    except Exception:
        today = date.today()
        return _empty_monthly_task_stats(today.year, today.month, upcoming_window_days)

    if month < 1 or month > 12:
        return _empty_monthly_task_stats(year, 1, upcoming_window_days)

    stats = _empty_monthly_task_stats(year, month, upcoming_window_days)
    if not user_email:
        return stats

    weekday_labels = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    try:
        selected_start = date(year, month, 1)
        selected_end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    except Exception:
        return stats

    today = date.today()
    upcoming_limit = today + timedelta(days=max(int(upcoming_window_days), 0))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT due_date, completed, completed_at
            FROM tasks
            WHERE user_email = ?
            """,
            (user_email,),
        )
        rows = cursor.fetchall()
    except Exception:
        conn.close()
        return stats
    finally:
        conn.close()

    month_total = 0
    month_completed = 0
    month_overdue = 0
    month_upcoming = 0

    weekday_counts = [0] * 7
    completed_days = set()

    for row in rows:
        due = _parse_iso_date(row["due_date"])
        completed_at = _parse_iso_date(row["completed_at"])
        is_completed = bool(row["completed"])

        if is_completed and completed_at:
            completed_days.add(completed_at)

        if due and selected_start <= due < selected_end:
            month_total += 1

            if is_completed:
                month_completed += 1
            else:
                if due < today:
                    month_overdue += 1
                if today <= due <= upcoming_limit:
                    month_upcoming += 1

        if is_completed and completed_at and selected_start <= completed_at < selected_end:
            weekday_counts[completed_at.weekday()] += 1

    # Current streak: consecutive days up to today with at least 1 completed task.
    streak = 0
    cursor_day = today
    while cursor_day in completed_days:
        streak += 1
        cursor_day -= timedelta(days=1)

    completion_percent = 0.0
    if month_total > 0:
        completion_percent = round((month_completed / month_total) * 100, 2)

    stats["totals"]["all_tasks"] = month_total
    stats["totals"]["completed_tasks"] = month_completed
    stats["totals"]["completion_percent"] = completion_percent
    stats["deadlines"]["overdue_tasks"] = month_overdue
    stats["deadlines"]["upcoming_tasks"] = month_upcoming
    stats["streak"]["current_days"] = streak

    stats["weekday_productivity"] = [
        {"day": weekday_labels[i], "tasks": weekday_counts[i]}
        for i in range(7)
    ]

    max_tasks = max(weekday_counts) if weekday_counts else 0
    if max_tasks > 0:
        best_day_idx = weekday_counts.index(max_tasks)
        stats["most_productive_day"] = {
            "day": weekday_labels[best_day_idx],
            "tasks": max_tasks,
        }

    return stats