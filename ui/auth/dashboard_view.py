import flet as ft

SIDEBAR_BG = "#7c5cbf"
SIDEBAR_ACCENT = "#9d7de0"
SURFACE = "#c8b4f0"
BORDER = "#b89ee8"
RADIUS_LG = 20
SPACE_LG = 24

def dashboard_view(page: ft.Page):

    sidebar = ft.Container(
        width=220,
        bgcolor=SIDEBAR_BG,
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=SURFACE,
        padding=SPACE_LG,
        content=ft.Container(
            expand=True,
            border_radius=RADIUS_LG,
            bgcolor="#ffffff",
            border=ft.Border.all(1, BORDER),
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