import flet as ft
from ui.auth.start_view import start_view
from ui.auth.login_view import login_view
from ui.auth.register_view import register_view
from ui.auth.forgot_password import forgot_password_view
from ui.auth.profile_photo_view import profile_photo_view
from ui.auth.dashboard_view import dashboard_view
from database import create_tables, get_user_by_email
import json
import os
import sys
from datetime import datetime, timedelta

def _get_session_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, ".session.json")

def _load_session() -> dict | None:
    try:
        path = _get_session_path()
        if not os.path.exists(path):
            return None
        with open(path) as f:
            data = json.load(f)
        # Sesija galioja 10 metų – praktiškai amžinai kol logout
        saved_at = datetime.fromisoformat(data.get("saved_at", "2000-01-01"))
        if datetime.now() - saved_at > timedelta(days=3650):
            os.remove(path)
            return None
        return data
    except Exception:
        return None


def save_session(user: dict, remember_me: bool = False) -> None:
    """Visada išsaugo sesiją. remember_me žyma tik lemia ar užpildyti login laukus."""
    try:
        with open(_get_session_path(), "w") as f:
            json.dump({
                **user,
                "saved_at": datetime.now().isoformat(),
                "remember_me": remember_me,
            }, f)
    except Exception:
        pass

def clear_session() -> None:
    try:
        path = _get_session_path()
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def main(page: ft.Page):
    create_tables()
    page.title = "OwlTrack"
    page.padding = 0
    page.spacing = 0
    page.window.icon = "assets/owl_clean.ico"

    page.save_session  = save_session
    page.clear_session = clear_session

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(start_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        elif page.route == "/forgot-password":
            page.views.append(forgot_password_view(page))
        elif page.route == "/profile-photo":
            page.views.append(profile_photo_view(page))
        elif page.route == "/dashboard":
            page.views.append(dashboard_view(page))
        page.update()

    page.on_route_change = route_change

    # ── Sesijos patikrinimas paleidžiant ──────────────────────────────
    session = _load_session()
    if session and session.get("register_email"):
        user = get_user_by_email(session["register_email"])
        if user:
            if not hasattr(page, "data") or page.data is None:
                page.data = {}
            page.data["register_name"]  = user["name"]
            page.data["register_email"] = user["email"]
            page.data["avatar_src"]     = user["avatar_src"]
            page.data["theme"]          = user.get("theme", "purple")
            page.data["remember_me"]    = session.get("remember_me", False)
            page.go("/dashboard")
            return

    route_change(page.route)
    page.update()

ft.run(main, assets_dir="assets")