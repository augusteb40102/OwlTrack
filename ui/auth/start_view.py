import flet as ft
import asyncio
from ui.themes import *

def start_view(page: ft.Page):

    def go_login(e):
        page.go("/login")

    title_text = ft.Text(
        "OwlTrack 🦉",
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
            width = 220,
            height = 45,
            opacity=0,
            animate_opacity=600,
            on_click=go_login,
            ),
        ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=SPACE_SM,
    )

    content = ft.Column(
        [title_text,buttons],
         alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand = True,
    )

    async def animate_logo():
        title_text.opacity = 1
        page.update()
        await asyncio.sleep(3) 

        title_text.opacity = 0
        page.update()
        await asyncio.sleep(0.8)

        title_text.size = FONT_LG
        title_text.opacity = 1
        buttons.controls[0].opacity = 1
        page.update()

    page.run_task(animate_logo)
    
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=content,
                expand=True,
                bgcolor=BACKGROUND
            ),
        ],
        expand=True,
        padding=0,
    )


