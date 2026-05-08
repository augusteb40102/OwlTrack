import flet as ft
import re
from ui.themes.backgrounds import auth_background
from database import register_user

# ── Fiksuotos purple spalvos – nesikeičia su tema ─────────────────────────────
_PRIMARY    = "#2D1B69"
_SECONDARY  = "#7C3AED"
_SURFACE    = "#F3EEFF"
_BORDER     = "#2D1B69"
_TEXT_PRIMARY   = "#1a1040"
_TEXT_SECONDARY = "#6B5A9E"
_TEXT_ON_PRIMARY = "#FFFFFF"
_TEXT_ON_SURFACE = "#2D1B69"
_ERROR      = "#ef4444"
_TRANSPARENT = ft.Colors.TRANSPARENT

FONT_LG  = 32
FONT_XS  = 14
SPACE_SM = 8
SPACE_MD = 16
RADIUS_MD = 10

_PRIMARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_PRIMARY,
    bgcolor=_PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
)
_SECONDARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_SURFACE,
    bgcolor=_SURFACE,
    shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
    side=ft.BorderSide(width=2, color=_PRIMARY),
)

def register_view(page: ft.Page):

    def go_back(e):
        page.go("/")

    def validate_password(password: str) -> str | None:
        if len(password) < 8:
            return "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return "Password must contain at least one uppercase letter"
        if not any(c.isdigit() for c in password):
            return "Password must contain at least one number"
        return None

    def is_valid_email(email: str) -> bool:
        return bool(re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))

    email_field = ft.TextField(
        label="Email adress", width=320,
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
    password_confirm_field = ft.TextField(
        label="Confirm password", width=320,
        password=True, can_reveal_password=True,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )
    name_field = ft.TextField(
        label="Name", width=320,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )

    error_text = ft.Text("", color=_ERROR, size=FONT_XS, visible=False)

    def register(e):
        error_text.visible = False
        email_field.border_color          = _BORDER
        password_field.border_color       = _BORDER
        password_confirm_field.border_color = _BORDER
        name_field.border_color           = _BORDER

        if not email_field.value:
            email_field.border_color = _ERROR
            error_text.value = "Enter your email adress"
            error_text.visible = True
            page.update()
            return

        if not is_valid_email(email_field.value):
            email_field.border_color = _ERROR
            error_text.value = "Enter a valid email address"
            error_text.visible = True
            page.update()
            return

        if not name_field.value:
            name_field.border_color = _ERROR
            error_text.value = "Enter your name"
            error_text.visible = True
            page.update()
            return

        if not password_field.value:
            password_field.border_color = _ERROR
            error_text.value = "Enter your password"
            error_text.visible = True
            page.update()
            return

        password_error = validate_password(password_field.value)
        if password_error:
            password_field.border_color = _ERROR
            error_text.value = password_error
            error_text.visible = True
            page.update()
            return

        if password_field.value != password_confirm_field.value:
            password_field.border_color       = _ERROR
            password_confirm_field.border_color = _ERROR
            error_text.value = "Passwords do not match!"
            error_text.visible = True
            page.update()
            return

        result = register_user(name_field.value, email_field.value.strip(), password_field.value)
        if not result["success"]:
            error_text.value = result["error"]
            error_text.visible = True
            page.update()
            return

        if not hasattr(page, "data") or page.data is None:
            page.data = {}
        page.data["register_name"]  = name_field.value
        page.data["register_email"] = email_field.value.strip()
        page.go("/profile-photo")

    content = ft.Column(
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
            ft.Text("Register", size=FONT_LG, weight="bold", color=_TEXT_PRIMARY),
            ft.Text("Create a new account", size=FONT_XS, color=_TEXT_SECONDARY),
            ft.Divider(height=SPACE_MD, color=_TRANSPARENT),
            email_field,
            name_field,
            password_field,
            password_confirm_field,
            error_text,
            ft.Divider(height=SPACE_SM, color=_TRANSPARENT),
            ft.ElevatedButton(
                "Create account",
                width=320, height=45,
                style=_SECONDARY_BTN_STYLE,
                on_click=register,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=SPACE_SM,
    )

    return ft.View(
        route="/register",
        controls=[auth_background(content)],
        expand=True,
        padding=0,
    )