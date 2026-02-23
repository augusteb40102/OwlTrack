import flet as ft
from ui.themes.themes import *
from ui.themes.backgrounds import auth_background

def forgot_password_view(page: ft.Page):
    def go_back(e):
        page.go("/login")

    email_field = ft.TextField(
        label="El. pašto adresas",
        width=320,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    success_text = ft.Text(
        "",
        color=PRIMARY,
        size=FONT_XS,
        visible=False,
    )

    error_text = ft.Text(
        "",
        color=ERROR,
        size=FONT_XS,
        visible=False,
    )

    def on_send(e):
        if not email_field.value:
            error_text.value = "Įveskite el. pašto adresą"
            error_text.visible = True
            success_text.visible = False
            page.update()
            return
        error_text.visible = False
        success_text.value = "Nuoroda išsiųsta į " + email_field.value
        success_text.visible = True
        page.update()

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
                    "Pamiršau slaptažodį",
                    size=FONT_LG,
                    weight="bold",
                    color=TEXT_PRIMARY,
                ),
                ft.Text(
                    "Įveskite el. paštą ir išsiųsime atkūrimo nuorodą",
                    size=FONT_SM,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                    width=320,
                ),
                ft.Container(height=SPACE_LG),
                email_field,
                ft.Container(height=SPACE_SM),
                error_text,
                success_text,
                ft.Container(height=SPACE_SM),
                ft.ElevatedButton(
                    "Siųsti nuorodą",
                    width=320,
                    height=48,
                    style=primary_button_style(),
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