import flet as ft
import asyncio
from ui.themes.themes import *
from ui.themes.backgrounds import auth_background

def start_view(page: ft.Page):

    def go_login(e):
        page.go("/login")

    def go_register(e):
        page.go("/register")

    owl = ft.Container(
        content=ft.Image(
                src="owl_clean.png",
                width=110,
                height=110,
                fit="contain",
            ),
            opacity=0,
            animate_opacity=800,
    #content=owl_logo(size=110),
    #opacity=0,
    #animate_opacity=800,
    )

    title_text = ft.Text(
        "OwlTrack",
        size=FONT_XL,
        weight="bold",
        color=TEXT_PRIMARY,
        opacity=0,
        animate_opacity=800,
    )

    buttons = ft.Column(
        [
            ft.ElevatedButton(
                "Log in",
                width=220,
                height=45,
                opacity=0,
                animate_opacity=600,
                on_click=go_login,
            ),
            ft.ElevatedButton(
                "Register",
                width=220,
                height=45,
                opacity=0,
                animate_opacity=600,
                on_click=go_register,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SPACE_SM,
    )

    content = ft.Column(
        [owl, title_text, buttons],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    async def animate_logo():
        owl.opacity = 1
        title_text.opacity = 1
        page.update()
        await asyncio.sleep(3)

        owl.opacity = 0
        title_text.opacity = 0
        page.update()
        await asyncio.sleep(0.8)

        title_text.size = FONT_LG
        owl.opacity = 1
        title_text.opacity = 1
        buttons.controls[0].opacity = 1
        buttons.controls[1].opacity = 1
        page.update()

    page.run_task(animate_logo)

    

    return ft.View(
    route="/",
    controls=[
        ft.Stack(
            expand=True,
            controls=[
                # GIF fonas
                ft.Image(
                    src="cosmos_purple.gif",
                    width=page.window.width,
                    height=page.window.height,
                    fit="fill",
                ),
                # Turinys ant fono
                ft.Container(
                    content=content,
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                ),
            ]
        )
    ],
    expand=True,
    padding=0,
)

