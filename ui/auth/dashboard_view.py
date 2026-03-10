import flet as ft
from ui.themes.themes import *

RADIUS_LG = 20
SPACE_LG = 24


def dashboard_view(page: ft.Page):

    username = "User"
    avatar_src = None

    if hasattr(page, "data") and page.data:
        username = page.data.get("register_name", "User")
        avatar_src = page.data.get("avatar_src", None)

    # Logout funkcija
    def logout(e):
        page.go("/login")

    # Avatar
    if avatar_src:
        avatar_widget = ft.Image(
            src=avatar_src,
            width=90,
            height=90,
            fit="contain",
        )
    else:
        avatar_widget = ft.Container(
            content=ft.Text(
                username[0].upper() if username else "U",
                size=28,
                weight="bold",
                color=TEXT_ON_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),
            width=72,
            height=72,
            border_radius=ft.border_radius.all(36),
            bgcolor=SECONDARY,
            alignment=ft.Alignment(0, 0),
        )

    # Viršus — OwlTrack + profilis
    top = ft.Column(
        [
            ft.Container(
                content=ft.Text(
                    "OwlTrack",
                    size=24,
                    weight="bold",
                    color=TEXT_ON_PRIMARY,
                ),
                padding=ft.padding.only(top=20, bottom=20),
                alignment=ft.Alignment(0, 0),
            ),
            avatar_widget,
            ft.Container(height=8),
            ft.Text(
                username,
                size=15,
                weight="bold",
                color=TEXT_ON_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # Apačia — Log Out mygtukas
    bottom = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.DOOR_FRONT_DOOR, color=TEXT_ON_PRIMARY, size=20),
                ft.Text("Log Out", size=14, color=TEXT_ON_PRIMARY, weight="w600"),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=180,
        height=44,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=[SECONDARY, PRIMARY],
        ),
        alignment=ft.Alignment(0, 0),
        bottom=24,
        left=20,
        on_click=logout,
        ink=True,
    )

    sidebar = ft.Container(
        width=220,
        bgcolor=PRIMARY,
        content=ft.Stack(
            [
                ft.Container(expand=True, bgcolor=PRIMARY),
                ft.Container(content=top, top=0, left=0, right=0),
                bottom,
            ],
            expand=True,
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=SURFACE,
        padding=SPACE_LG,
        content=ft.Container(
            expand=True,
            border_radius=RADIUS_LG,
            bgcolor=TEXT_ON_PRIMARY,
            border=ft.border.all(1, BORDER),
        ),
    )

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Row(
                [sidebar, main_content],
                spacing=0,
                expand=True,
            )
        ],
        expand=True,
        padding=0,
    )