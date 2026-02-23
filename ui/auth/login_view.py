import flet as ft
from ui.themes import *

def login_view(page: ft.Page):
    def go_back(e):
        page.go("/")

    email_field = ft.TextField(
        label="El. pašto adresas",
        width=320,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    password_field = ft.TextField(
        label="Slaptažodis",
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
        # Validacija
        if not email_field.value or not password_field.value:
            error_text.value = "Prašome užpildyti visus laukus"
            error_text.visible = True
            page.update()
            return
        
        # TODO: AB – čia prisijungimo logika (SCRUM-31)
        # pvz: auth.login(email_field.value, password_field.value)
        error_text.visible = False
        page.update()

    content = ft.Column(
        [
            # Atgal mygtukas
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

            # Logotipas / antraštė
            ft.Text(
                "Prisijungimas",
                size=FONT_LG,
                weight="bold",
                color=TEXT_PRIMARY,
            ),
            ft.Text(
                "Įveskite savo duomenis",
                size=FONT_SM,
                color=TEXT_SECONDARY,
            ),

            ft.Container(height=SPACE_LG),

            # Laukai
            email_field,
            ft.Container(height=SPACE_SM),
            password_field,

            # Pamiršau slaptažodį funkcija Austejai


            ft.Container(height=SPACE_SM),
            error_text,
            ft.Container(height=SPACE_SM),

            # Prisijungti mygtukas
            ft.ElevatedButton(
                "Prisijungti",
                width=320,
                height=48,
                style=primary_button_style(),
                on_click=on_login,  # TODO: AB – prijungti prie auth (SCRUM-36)
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    return ft.View(
        route="/login",
        bgcolor=BACKGROUND,
        controls=[
            ft.Container(
                content=content,
                expand=True,
                alignment=ft.Alignment(0, 0),
            )
        ],
        expand=True,
        padding=ft.Padding(
            left=SPACE_LG,
            right=SPACE_LG,
            top=SPACE_MD,
            bottom=SPACE_LG,
        ),
    )