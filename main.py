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
import uuid
from datetime import datetime, timedelta

def _get_session_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, ".session.json")

def _get_remember_me_path() -> str:
    """Get the path to the Remember Me file in OS-specific user data directory"""
    if sys.platform == "darwin":
        app_data_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "OwlTrack")
    elif os.name == "nt":
        appdata = os.getenv("APPDATA")
        app_data_dir = os.path.join(appdata, "OwlTrack") if appdata else os.path.join(os.path.expanduser("~"), "OwlTrack")
    else:
        app_data_dir = os.path.join(os.path.expanduser("~"), ".owltrack")
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, ".remember_me.json")

def _get_device_id_path() -> str:
    """Get the path to the device ID file in OS-specific user data directory"""
    if sys.platform == "darwin":
        app_data_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "OwlTrack")
    elif os.name == "nt":
        appdata = os.getenv("APPDATA")
        app_data_dir = os.path.join(appdata, "OwlTrack") if appdata else os.path.join(os.path.expanduser("~"), "OwlTrack")
    else:
        app_data_dir = os.path.join(os.path.expanduser("~"), ".owltrack")
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, ".device_id.json")

def _generate_or_load_device_id() -> str:
    """Generate a unique device ID or load existing one"""
    device_id_path = _get_device_id_path()
    try:
        if os.path.exists(device_id_path):
            with open(device_id_path) as f:
                data = json.load(f)
                return data.get("device_id", "")
    except Exception:
        pass
    
    # Generate new device ID
    device_id = str(uuid.uuid4())
    try:
        with open(device_id_path, "w") as f:
            json.dump({"device_id": device_id, "created_at": datetime.now().isoformat()}, f)
    except Exception:
        pass
    
    return device_id

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
    """Clear only the session file (for security). Remember Me stays while on same device."""
    try:
        path = _get_session_path()
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def clear_session_and_remember_me() -> None:
    """Clear both session and Remember Me data (for logout or explicit clearing)"""
    clear_session()
    try:
        remember_path = _get_remember_me_path()
        if os.path.exists(remember_path):
            os.remove(remember_path)
    except Exception:
        pass

def main(page: ft.Page):
    create_tables()
    page.title = "OwlTrack"
    page.padding = 0
    page.spacing = 0
    page.window.icon = "assets/owl_clean.ico"

    # ── Device ID for Remember Me binding ──────────────────────────────
    device_id = _generate_or_load_device_id()
    page.device_id = device_id
    page.save_session  = save_session
    page.clear_session = clear_session
    page.clear_session_and_remember_me = clear_session_and_remember_me

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

    # ── SECURITY FIX: Do not auto-login on startup ──────────────────────────
    # Always start at login screen. User must explicitly authenticate each time.
    # Session/Remember Me is only used to pre-populate form fields, not for auto-login.
    clear_session()
    route_change(page.route)
    page.update()

ft.run(main, assets_dir="assets")