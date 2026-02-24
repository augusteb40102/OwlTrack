import flet as ft

def auth_background(content: ft.Control) -> ft.Stack:
    """
    Apgaubia turinį fonu.
    Norėdami pakeisti foną – tiesiog pakeiskite šią funkciją.
    """
    return ft.Stack(
        [
            
            # Vienspalvis fonas (dabar aktyvus)
            ft.Container(
                expand=True,
                bgcolor="#FFFFFF",
            ),

            # Variantas 2: Gradientas (atkomentiruok kai reikia)
            # ft.Container(
            #     expand=True,
            #     gradient=ft.LinearGradient(
            #         begin=ft.Alignment(-1, -1),
            #         end=ft.Alignment(1, 1),
            #         colors=["#0f172a", "#1e293b"],
            #     ),
            # ),

            # Variantas 3: GIF / paveikslėlis (atkomentiruok kai reikia)
            # ft.Image(
            #     src="bg.gif",
            #     fit="cover",
            #     expand=True,
            # ),

            # ─── TURINYS VIRŠUJE ────────────────────────────
            ft.Container(
                content=content,
                expand=True,
                alignment=ft.Alignment(0, 0),
            ),
        ],
        expand=True,
    )


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