import flet as ft

def owl_logo(size=120):
    return ft.Stack(
        width=size,
        height=size,
        controls=[
            # Kūnas
            ft.Container(
                width=size,
                height=size,
                border_radius=size / 2,
                gradient=ft.RadialGradient(
                    colors=["#7C3AED", "#4C1D95"],
                    radius=1.2,
                ),
            ),
            # Kairysis sparnas
            ft.Container(
                width=size * 0.35,
                height=size * 0.55,
                left=size * 0.02,
                top=size * 0.38,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.4,
                    top_right=size * 0.1,
                    bottom_left=size * 0.3,
                    bottom_right=size * 0.1,
                ),
                gradient=ft.LinearGradient(
                    colors=["#6D28D9", "#3B0764"],
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                ),
            ),
            # Dešinysis sparnas
            ft.Container(
                width=size * 0.35,
                height=size * 0.55,
                right=size * 0.02,
                top=size * 0.38,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.1,
                    top_right=size * 0.4,
                    bottom_left=size * 0.1,
                    bottom_right=size * 0.3,
                ),
                gradient=ft.LinearGradient(
                    colors=["#6D28D9", "#3B0764"],
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                ),
            ),
            # Kairysis ausynas
            ft.Container(
                width=size * 0.18,
                height=size * 0.22,
                left=size * 0.18,
                top=size * 0.01,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.15,
                    top_right=size * 0.05,
                    bottom_left=size * 0.05,
                    bottom_right=size * 0.05,
                ),
                bgcolor="#5B21B6",
            ),
            # Dešinysis ausynas
            ft.Container(
                width=size * 0.18,
                height=size * 0.22,
                right=size * 0.18,
                top=size * 0.01,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.05,
                    top_right=size * 0.15,
                    bottom_left=size * 0.05,
                    bottom_right=size * 0.05,
                ),
                bgcolor="#5B21B6",
            ),
            # Kairysis akis
            ft.Container(
                width=size * 0.28,
                height=size * 0.28,
                left=size * 0.14,
                top=size * 0.28,
                border_radius=size * 0.14,
                bgcolor="white",
            ),
            # Dešinysis akis
            ft.Container(
                width=size * 0.28,
                height=size * 0.28,
                right=size * 0.14,
                top=size * 0.28,
                border_radius=size * 0.14,
                bgcolor="white",
            ),
            # Kairysis vyzdys
            ft.Container(
                width=size * 0.14,
                height=size * 0.14,
                left=size * 0.21,
                top=size * 0.35,
                border_radius=size * 0.07,
                bgcolor="#1E0A3C",
            ),
            # Dešinysis vyzdys
            ft.Container(
                width=size * 0.14,
                height=size * 0.14,
                right=size * 0.21,
                top=size * 0.35,
                border_radius=size * 0.07,
                bgcolor="#1E0A3C",
            ),
            # Snapas
            ft.Container(
                width=size * 0.18,
                height=size * 0.12,
                left=size * 0.41,
                top=size * 0.50,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.02,
                    top_right=size * 0.02,
                    bottom_left=size * 0.06,
                    bottom_right=size * 0.06,
                ),
                bgcolor="#F59E0B",
            ),
        ],
    )