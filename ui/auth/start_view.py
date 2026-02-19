import flet as ft
import asyncio
from ui.themes import *

def start_view(page: ft.Page):

    title_text = ft.Text(
        "OwlTrack 🦉",
        size=FONT_XL,
        weight="bold",
        color=TEXT_PRIMARY,
        opacity=0, 
        animate_opacity=800,
    )

    login_button = ft.ElevatedButton(
        "Login",
        visible=False,  # pradžioje paslėptas
        on_click=lambda e: page.go("/login")
    )

    content = ft.Column(
        [title_text],
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

    page.run_task(animate_logo)
    
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=content,
                expand=True,
                bgcolor=BACKGROUND
            )
        ]
    )


def login_view(page: ft.Page):
    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BACKGROUND,
                content=ft.Column(
                    [
                        ft.Text("Login screen (čia vėliau bus forma)", size=FONT_L),
                        ft.ElevatedButton("Back", on_click=lambda e: page.go("/"))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        ]
    )