import flet as ft

SIDEBAR_BG = "#7c5cbf"
SURFACE = "#c8b4f0"
BORDER = "#b89ee8"
RADIUS_LG = 20
SPACE_LG = 24

def dashboard_view(page: ft.Page):

    username   = "User"
    avatar_src = None

    if hasattr(page, "data") and page.data:
        username   = page.data.get("register_name", "User")
        avatar_src = page.data.get("avatar_src", None)

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
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            width=72,
            height=72,
            border_radius=ft.border_radius.all(36),
            bgcolor="#9d7de0",
            alignment=ft.Alignment(0, 0),
        )

    sidebar = ft.Container(
        width=220,
        bgcolor=SIDEBAR_BG,
        padding=ft.padding.symmetric(vertical=16, horizontal=8),
        content=ft.Column(
            [
                avatar_widget,
                ft.Container(height=8),
                ft.Text(
                    f"Hi, {username}!",
                    size=15,
                    weight="bold",
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=SURFACE,
        padding=SPACE_LG,
        content=ft.Container(
            expand=True,
            border_radius=RADIUS_LG,
            bgcolor="#ffffff",
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