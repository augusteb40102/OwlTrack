import flet as ft
from ui.themes.themes import *

RADIUS_LG = 20
SPACE_LG = 24

def dashboard_view(page: ft.Page):
    username = "User"
    avatar_src = None
    user_email = "user@example.com"

    if hasattr(page, "data") and page.data:
        username   = page.data.get("register_name", "User")
        avatar_src = page.data.get("avatar_src", None)
        user_email = page.data.get("register_email", "user@example.com")

    # Logout overlay
    logout_overlay = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=ft.Container(
            width=300,
            padding=ft.padding.all(28),
            border_radius=16,
            bgcolor=SURFACE,
            border=ft.border.all(1, BORDER),
            content=ft.Column(
                [
                    ft.Text("Log Out", size=18, weight="bold", color=TEXT_PRIMARY),
                    ft.Container(height=8),
                    ft.Text(
                        "Are you sure you want to log out?",
                        size=13,
                        color=TEXT_SECONDARY,
                    ),
                    ft.Container(height=24),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Cancel", size=13, color=TEXT_SECONDARY, weight="w600"),
                                on_click=lambda e: hide_overlay(),
                                ink=True,
                                border_radius=8,
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                border=ft.border.all(1, BORDER),
                            ),
                            ft.Container(
                                content=ft.Text("Log Out", size=13, color=TEXT_ON_PRIMARY, weight="w600"),
                                on_click=lambda e: page.go("/login"),
                                ink=True,
                                border_radius=8,
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                bgcolor=PRIMARY,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                    ),
                ],
                spacing=0,
                tight=True,
            ),
        ),
    )

    def show_overlay():
        logout_overlay.visible = True
        page.update()

    def hide_overlay():
        logout_overlay.visible = False
        page.update()

    def logout(e):
        show_overlay()

    # Avatar widget
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

    # Email row – pradžioje paslėptas
    email_container = ft.Container(
        content=ft.Text(
            user_email,
            size=11,
            color=TEXT_ON_PRIMARY,
            opacity=0.75,
            text_align=ft.TextAlign.CENTER,
        ),
        height=0,
        opacity=0,
        animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        alignment=ft.Alignment(0, 0),
    )

    arrow_icon = ft.Icon(
        icon=ft.Icons.KEYBOARD_ARROW_DOWN,
        color=TEXT_ON_PRIMARY,
        size=16,
        opacity=0.7,
    )

    expanded = [False]

    def toggle_email(e):
        expanded[0] = not expanded[0]
        if expanded[0]:
            email_container.height = 22
            email_container.opacity = 1
            arrow_icon.icon = ft.Icons.KEYBOARD_ARROW_UP
        else:
            email_container.height = 0
            email_container.opacity = 0
            arrow_icon.icon = ft.Icons.KEYBOARD_ARROW_DOWN
        page.update()

    username_row = ft.Container(
        content=ft.Row(
            [
                ft.Text(username, size=15, weight="bold", color=TEXT_ON_PRIMARY),
                arrow_icon,
            ],
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=toggle_email,
        ink=True,
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    top = ft.Column(
        [
            ft.Container(
                content=ft.Text("OwlTrack", size=24, weight="bold", color=TEXT_ON_PRIMARY),
                padding=ft.padding.only(top=20, bottom=20),
                alignment=ft.Alignment(0, 0),
            ),
            avatar_widget,
            ft.Container(height=8),
            username_row,
            email_container,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    bottom = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="logout_icon.png", width=20, height=20, fit="contain"),
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
            ft.Stack(
                [
                    ft.Row(
                        [sidebar, main_content],
                        spacing=0,
                        expand=True,
                    ),
                    logout_overlay,
                ],
                expand=True,
            )
        ],
        expand=True,
        padding=0,
    )