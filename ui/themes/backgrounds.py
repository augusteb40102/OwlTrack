import flet as ft

def auth_background(content, page=None):
    return ft.Stack(
        expand=True,
        width=float("inf"),
        controls=[
            ft.Image(
                src="cosmos_purple.gif",
                width=float("inf"),
                height=float("inf"),
                expand=True,
                fit="fill",
            ),
            ft.Container(
                content=content,
                expand=True,
                alignment=ft.Alignment(0, 0),
            ),
        ]
    )