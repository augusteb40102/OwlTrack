import flet as ft
from ui.themes.themes import *
from ui.themes.backgrounds import auth_background
from database import register_user

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
    
    email_field = ft.TextField(
        label="Email adress",
        width=320,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    password_field = ft.TextField(
        label="Password",
        width=320,
        password=True,
        can_reveal_password=True,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    password_confirm_field = ft.TextField(
        label="Confirm password",
        width=320,
        password=True,
        can_reveal_password=True,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    name_field = ft.TextField(
        label="Name",
        width=320,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    error_text = ft.Text(
        "",
        color=ERROR,
        size=FONT_XS,
        visible=False,
    )

    def register(e):
        # Išvalome klaidas
        error_text.visible = False
        email_field.border_color = BORDER
        password_field.border_color = BORDER
        password_confirm_field.border_color = BORDER
        name_field.border_color = BORDER

        # Tikriname ar visi laukeliai užpildyti
        if not email_field.value:
            email_field.border_color = ERROR
            error_text.value = "Enter your email adress"
            error_text.visible = True
            page.update()
            return

        if not name_field.value:
            name_field.border_color = ERROR
            error_text.value = "Enter your name"
            error_text.visible = True
            page.update()
            return

        if not password_field.value:
            password_field.border_color = ERROR
            error_text.value = "Enter your password"
            error_text.visible = True
            page.update()
            return

        password_error = validate_password(password_field.value)
        if password_error:
            password_field.border_color = ERROR
            error_text.value = password_error
            error_text.visible = True
            page.update()
            return
        
        # Tikriname slaptažodžių sutapimą
        if password_field.value != password_confirm_field.value:
            password_field.border_color = ERROR
            password_confirm_field.border_color = ERROR
            error_text.value = "Passwords do not match!"
            error_text.visible = True
            page.update()
            return

        # Išsaugome į DB
        result = register_user(name_field.value, email_field.value, password_field.value)
        if not result["success"]:
            error_text.value = result["error"]
            error_text.visible = True
            page.update()
            return

        # Jei sėkminga — einame į pelėdžiuko pasirinkimą
        if not hasattr(page, "data") or page.data is None:
            page.data = {}
        page.data["register_name"] = name_field.value
        page.data["register_email"] = email_field.value
        page.go("/profile-photo")

    content = ft.Column(
        [
            ft.Row(               
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=TEXT_PRIMARY,
                        on_click=go_back,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Text(
                "Register",
                size=FONT_LG,
                weight="bold",
                color=TEXT_PRIMARY,
            ),
            ft.Text(
                "Create a new account",
                size=FONT_XS,
                color=TEXT_SECONDARY,
            ),
            ft.Divider(height=SPACE_MD, color=ft.Colors.TRANSPARENT),
            email_field,
            name_field,
            password_field,
            password_confirm_field,
            error_text,
            ft.Divider(height=SPACE_SM, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton(
                "Create account",
                width=320,
                height=45,
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