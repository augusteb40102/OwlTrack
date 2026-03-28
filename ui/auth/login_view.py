import flet as ft
import re
import json
import os
import sys
import uuid
from datetime import datetime
from ui.themes.backgrounds import auth_background
from database import login_user, verify_reset_token, mark_token_used, set_password_from_token, get_user_by_email

# ── Fiksuotos purple spalvos – nesikeičia su tema ─────────────────────────────
_PRIMARY         = "#2D1B69"
_SURFACE         = "#F3EEFF"
_BORDER          = "#2D1B69"
_TEXT_PRIMARY    = "#1a1040"
_TEXT_SECONDARY  = "#6B5A9E"
_TEXT_ON_PRIMARY = "#FFFFFF"
_ERROR           = "#ef4444"

FONT_LG  = 32
FONT_SM  = 16
FONT_XS  = 14
SPACE_LG = 24
SPACE_SM = 8

_PRIMARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_PRIMARY,
    bgcolor=_PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=10),
)

# ── Remember Me failo vieta ───────────────────────────────────────────────────
def _get_remember_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(base) in ("ui", "auth"):
            base = os.path.dirname(os.path.dirname(base))
    return os.path.join(base, ".remember_me.json")

def _save_remember(email: str, password: str, device_id: str) -> None:
    """Save email+password+device_id for Remember Me"""
    try:
        with open(_get_remember_path(), "w") as f:
            json.dump({
                "email": email,
                "password": password,
                "device_id": device_id,
                "saved_at": datetime.now().isoformat()
            }, f)
    except Exception:
        pass

def _load_remember(device_id: str) -> dict | None:
    """Load email+password only if device_id matches"""
    try:
        path = _get_remember_path()
        if not os.path.exists(path):
            return None
        with open(path) as f:
            data = json.load(f)
        # Check if device ID matches
        if data.get("device_id") != device_id:
            return None
        return data
    except Exception:
        pass
    return None

def _clear_remember() -> None:
    try:
        path = _get_remember_path()
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def login_view(page: ft.Page):
    def go_back(e):
        page.go("/")

    def is_valid_email(email: str) -> bool:
        return bool(re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))

    # ── Užkrauti Remember Me duomenis (tik jei tas pats įrenginys) ────────────
    device_id = page.device_id if hasattr(page, "device_id") else ""
    saved = _load_remember(device_id)

    email_field = ft.TextField(
        label="Email address", width=320,
        value=saved.get("email", "") if saved else "",
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )
    password_field = ft.TextField(
        label="Password", width=320,
        value=saved.get("password", "") if saved else "",
        password=True, can_reveal_password=True,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )

    remember_me_checkbox = ft.Checkbox(
        label="Remember Me",
        value=bool(saved),
        active_color=_PRIMARY,
        check_color=_TEXT_ON_PRIMARY,
        label_style=ft.TextStyle(color=_TEXT_SECONDARY, size=FONT_XS),
    )

    error_text = ft.Text("", color=_ERROR, size=FONT_XS, visible=False)

    def on_login(e):
        error_text.visible = False

        if not email_field.value or not password_field.value:
            error_text.value   = "Please fill in all fields"
            error_text.visible = True
            page.update()
            return

        if not is_valid_email(email_field.value):
            error_text.value   = "Enter a valid email address"
            error_text.visible = True
            page.update()
            return

        email    = email_field.value.strip()
        password = password_field.value.strip()

        # 1. Bandyti prisijungti su slaptažodžiu
        result = login_user(email, password)
        if result["success"]:
            _handle_remember(email, password)
            _go_dashboard(result["user"])
            return

        # 2. Jei nepavyko – tikrinti ar tai laikinas kodas
        code = password.upper()
        token_result = verify_reset_token(code)

        if token_result["valid"] and token_result["email"].lower() == email.lower():
            set_password_from_token(email, code)
            mark_token_used(code)
            user = get_user_by_email(email)
            if user:
                _handle_remember(email, code)
                _go_dashboard(user)
                return

        # 3. Nei slaptažodis nei kodas netiko
        error_text.value   = result["error"]
        error_text.visible = True
        page.update()

    def _handle_remember(email: str, password: str):
        if remember_me_checkbox.value:
            _save_remember(email, password, device_id)
        else:
            _clear_remember()
        # Visada išsaugoti sesiją (su arba be remember_me žymos)
        if hasattr(page, "save_session"):
            page.save_session(page.data, remember_me=bool(remember_me_checkbox.value))

    def _go_dashboard(user: dict):
        if not hasattr(page, "data") or page.data is None:
            page.data = {}
        page.data["register_name"]  = user["name"]
        page.data["register_email"] = user["email"]
        page.data["avatar_src"]     = user["avatar_src"]
        page.data["theme"]          = user.get("theme", "purple")
        page.data["remember_me"]    = bool(remember_me_checkbox.value)

        page.go("/dashboard")

    content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=_TEXT_PRIMARY, on_click=go_back)],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=SPACE_LG),
                ft.Text("Login", size=FONT_LG, weight="bold", color=_TEXT_PRIMARY),
                ft.Text("Enter your details", size=FONT_SM, color=_TEXT_SECONDARY),
                ft.Container(height=SPACE_LG),
                email_field,
                ft.Container(height=SPACE_SM),
                password_field,
                ft.Container(
                    content=remember_me_checkbox,
                    width=320,
                    alignment=ft.Alignment(-1, 0),
                ),
                ft.Container(
                    content=ft.TextButton(
                        "Forgot password?",
                        on_click=lambda e: page.go("/forgot-password"),
                        style=ft.ButtonStyle(color=_PRIMARY),
                    ),
                    width=320,
                    alignment=ft.Alignment(-1, 0),
                ),
                error_text,
                ft.Container(height=SPACE_SM),
                ft.ElevatedButton(
                    "Log in",
                    width=320, height=48,
                    style=_PRIMARY_BTN_STYLE,
                    on_click=on_login,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        padding=ft.Padding(left=SPACE_LG, right=SPACE_LG, top=16, bottom=SPACE_LG),
    )

    return ft.View(
        route="/login",
        controls=[auth_background(content)],
        expand=True,
        padding=0,
    )