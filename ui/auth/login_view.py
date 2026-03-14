import flet as ft
import re
from ui.themes.backgrounds import auth_background
from database import login_user

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

def login_view(page: ft.Page):
    def go_back(e):
        page.go("/")

    def is_valid_email(email: str) -> bool:
        return bool(re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))

    email_field = ft.TextField(
        label="Email address", width=320,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )
    password_field = ft.TextField(
        label="Password", width=320,
        password=True, can_reveal_password=True,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )

    error_text = ft.Text("", color=_ERROR, size=FONT_XS, visible=False)

    def on_login(e):
        if not email_field.value or not password_field.value:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
            page.update()
            return

        if not is_valid_email(email_field.value):
            error_text.value = "Enter a valid email address"
            error_text.visible = True
            page.update()
            return

        result = login_user(email_field.value.strip(), password_field.value)
        if not result["success"]:
            error_text.value = result["error"]
            error_text.visible = True
            page.update()
            return

        if not hasattr(page, "data") or page.data is None:
            page.data = {}
        page.data["register_name"]  = result["user"]["name"]
        page.data["register_email"] = result["user"]["email"]
        page.data["avatar_src"]     = result["user"]["avatar_src"]
        page.data["theme"]          = result["user"].get("theme", "purple")
        page.go("/dashboard")

    content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=_TEXT_PRIMARY,
                            on_click=go_back,
                        )
                    ],
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