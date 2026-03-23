import flet as ft
import re
from ui.themes.backgrounds import auth_background
from logic.email_service import send_reset_email, generate_reset_token

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
SPACE_MD = 16

_PRIMARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_PRIMARY,
    bgcolor=_PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=10),
)

def forgot_password_view(page: ft.Page):
    def go_back(e):
        page.go("/login")

    def is_valid_email(email: str) -> bool:
        return bool(re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))

    email_field = ft.TextField(
        label="Email address", width=320,
        bgcolor=_SURFACE, border_color=_BORDER,
        focused_border_color=_PRIMARY,
        text_style=ft.TextStyle(color=_TEXT_PRIMARY),
        label_style=ft.TextStyle(color=_TEXT_SECONDARY),
    )

    success_text = ft.Text("", color=_PRIMARY, size=FONT_XS, visible=False)
    error_text   = ft.Text("", color=_ERROR,   size=FONT_XS, visible=False)

    def on_send(e):
        # Validacija
        if not email_field.value:
            error_text.value   = "Please enter your email address"
            error_text.visible = True
            success_text.visible = False
            page.update()
            return

        if not is_valid_email(email_field.value):
            error_text.value   = "Please enter a valid email address"
            error_text.visible = True
            success_text.visible = False
            page.update()
            return

        # Generuojame tokeną ir siunčiame laišką
        email = email_field.value.strip()
        reset_token = generate_reset_token()
        result = send_reset_email(email, reset_token)

        error_text.visible = False
        success_text.visible = False

        if result["success"]:
            success_text.value = "Reset link sent to " + email
            success_text.visible = True
            email_field.value = ""
        elif result["message"] == "rate_limited":
            error_text.value = f"Try again in {result.get('remaining', 60)} seconds"
            error_text.visible = True
        else:
            error_text.value = "Failed to send reset email. Please try again."
            error_text.visible = True

        page.update()

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
                ft.Text("Forgot Password", size=FONT_LG, weight="bold", color=_TEXT_PRIMARY),
                ft.Text(
                    "Enter your email and we'll send a reset link",
                    size=FONT_SM, color=_TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER, width=320,
                ),
                ft.Container(height=SPACE_LG),
                email_field,
                ft.Container(height=SPACE_SM),
                error_text,
                success_text,
                ft.Container(height=SPACE_SM),
                ft.ElevatedButton(
                    "Send Link",
                    width=320, height=48,
                    style=_PRIMARY_BTN_STYLE,
                    on_click=on_send,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        padding=ft.Padding(left=SPACE_LG, right=SPACE_LG, top=SPACE_MD, bottom=SPACE_LG),
    )

    return ft.View(
        route="/forgot-password",
        controls=[auth_background(content)],
        expand=True,
        padding=0,
    )