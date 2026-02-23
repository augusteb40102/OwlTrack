import flet as ft
from ui.themes.themes import *
from ui.themes.backgrounds import auth_background

def register_view(page: ft.Page):

    def go_back(e):
        page.go("/")

    def validate_password(password: str) -> str | None:
        if len(password) < 8:
            return "Slaptažodis turi būti bent 8 simbolių"
        if not any(c.isupper() for c in password):
            return "Slaptažodis turi turėti bent vieną didžiąją raidę"
        if not any(c.isdigit() for c in password):
            return "Slaptažodis turi turėti bent vieną skaičių"
        return None
    
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

    password_confirm_field = ft.TextField(
        label="Pakartokite slaptažodį",
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
        label="Jūsų vardas",
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
            error_text.value = "Įveskite el. pašto adresą"
            error_text.visible = True
            page.update()
            return

        if not name_field.value:
            name_field.border_color = ERROR
            error_text.value = "Įveskite savo vardą"
            error_text.visible = True
            page.update()
            return

        if not password_field.value:
            password_field.border_color = ERROR
            error_text.value = "Įveskite slaptažodį"
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
            error_text.value = "Slaptažodžiai nesutampa!"
            error_text.visible = True
            page.update()
            return

        # Viskas gerai — čia vėliau bus registracijos logika
        print(f"Registruojamas: {name_field.value}, {email_field.value}")
        page.go("/login")

    content = ft.Column(
        [
            ft.Text(
                "Registracija",
                size=FONT_LG,
                weight="bold",
                color=TEXT_PRIMARY,
            ),
            ft.Text(
                "Sukurkite naują paskyrą",
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
                "Registruotis",
                width=320,
                height=45,
                on_click=register,
            ),
            ft.TextButton(
                "← Atgal",
                on_click=go_back,
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