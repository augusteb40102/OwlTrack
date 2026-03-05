# login_view.py
import flet as ft
from ui.themes.themes import *
from ui.themes.backgrounds import auth_background
from database import login_user

def login_view(page: ft.Page):
    def go_back(e):
        page.go("/")

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

    error_text = ft.Text(
        "",
        color=ERROR,
        size=FONT_XS,
        visible=False,
    )

    def on_login(e):
        if not email_field.value or not password_field.value:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
            page.update()
            return
        result = login_user(email_field.value, password_field.value)
        if not result["success"]:
            error_text.value = result["error"]
            error_text.visible = True
            page.update()
            return

        page.go("/dashboard")

    content = ft.Container(
        content=ft.Column(
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
                ft.Container(height=SPACE_LG),
                ft.Text(
                    "Login",
                    size=FONT_LG,
                    weight="bold",
                    color=TEXT_PRIMARY,
                ),
                ft.Text(
                    "Enter your details",
                    size=FONT_SM,
                    color=TEXT_SECONDARY,
                ),
                ft.Container(height=SPACE_LG),
                email_field,
                ft.Container(height=SPACE_SM),
                password_field,
                # Pamiršau slaptažodį
                ft.Container(
                    content=ft.TextButton(
                        "Forgot password?",
                        on_click=lambda e: page.go("/forgot-password"),
                        style=ft.ButtonStyle(
                            color=PRIMARY,
                        ),
                    ),
                    width=320,
                    alignment=ft.Alignment(-1, 0),
                ),
                error_text,
                ft.Container(height=SPACE_SM),
                ft.ElevatedButton(
                    "Log in",
                    width=320,
                    height=48,
                    style=primary_button_style(),
                    on_click=on_login,
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
        route="/login",
        controls=[auth_background(content)],
        expand=True,
        padding=0,
    )