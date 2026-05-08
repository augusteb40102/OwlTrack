import flet as ft
from ui.themes.themes import *

def owl_logo(size=120):
    return ft.Stack(
        width=size,
        height=size,
        controls=[
            # Kūnas
            ft.Container(
                width=size * 0.85,
                height=size * 0.85,
                left=size * 0.075,
                top=size * 0.15,
                border_radius=size * 0.42,
                bgcolor=OWL_BODY,
            ),
            # Galva
            ft.Container(
                width=size * 0.75,
                height=size * 0.65,
                left=size * 0.125,
                top=size * 0.05,
                border_radius=size * 0.35,
                bgcolor=OWL_HEAD,
            ),
            # Kairysis ausynas
            ft.Container(
                width=size * 0.18,
                height=size * 0.25,
                left=size * 0.18,
                top=size * 0.0,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.12,
                    top_right=size * 0.04,
                    bottom_left=size * 0.04,
                    bottom_right=size * 0.04,
                ),
                bgcolor=OWL_WING,
            ),
            # Dešinysis ausynas
            ft.Container(
                width=size * 0.18,
                height=size * 0.25,
                right=size * 0.18,
                top=size * 0.0,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.04,
                    top_right=size * 0.12,
                    bottom_left=size * 0.04,
                    bottom_right=size * 0.04,
                ),
                bgcolor=OWL_WING,
            ),
            # Kairysis sparnas
            ft.Container(
                width=size * 0.22,
                height=size * 0.45,
                left=size * 0.02,
                top=size * 0.45,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.15,
                    top_right=size * 0.05,
                    bottom_left=size * 0.15,
                    bottom_right=size * 0.05,
                ),
                bgcolor=OWL_WING,
            ),
            # Dešinysis sparnas
            ft.Container(
                width=size * 0.22,
                height=size * 0.45,
                right=size * 0.02,
                top=size * 0.45,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.05,
                    top_right=size * 0.15,
                    bottom_left=size * 0.05,
                    bottom_right=size * 0.15,
                ),
                bgcolor=OWL_WING,
            ),
            # Pilvas
            ft.Container(
                width=size * 0.5,
                height=size * 0.4,
                left=size * 0.25,
                top=size * 0.52,
                border_radius=size * 0.25,
                bgcolor=OWL_BELLY,
            ),
            # Kairysis akis (geltona)
            ft.Container(
                width=size * 0.3,
                height=size * 0.3,
                left=size * 0.1,
                top=size * 0.2,
                border_radius=size * 0.15,
                bgcolor=OWL_EYE,
            ),
            # Dešinysis akis (geltona)
            ft.Container(
                width=size * 0.3,
                height=size * 0.3,
                right=size * 0.1,
                top=size * 0.2,
                border_radius=size * 0.15,
                bgcolor=OWL_EYE,
            ),
            # Kairysis vyzdys
            ft.Container(
                width=size * 0.17,
                height=size * 0.17,
                left=size * 0.165,
                top=size * 0.265,
                border_radius=size * 0.085,
                bgcolor=OWL_PUPIL,
            ),
            # Dešinysis vyzdys
            ft.Container(
                width=size * 0.17,
                height=size * 0.17,
                right=size * 0.165,
                top=size * 0.265,
                border_radius=size * 0.085,
                bgcolor=OWL_PUPIL,
            ),
            # Kairysis blizgesys
            ft.Container(
                width=size * 0.07,
                height=size * 0.07,
                left=size * 0.17,
                top=size * 0.27,
                border_radius=size * 0.035,
                bgcolor="white",
            ),
            # Dešinysis blizgesys
            ft.Container(
                width=size * 0.07,
                height=size * 0.07,
                right=size * 0.17,
                top=size * 0.27,
                border_radius=size * 0.035,
                bgcolor="white",
            ),
            # Snapas
            ft.Container(
                width=size * 0.16,
                height=size * 0.12,
                left=size * 0.42,
                top=size * 0.45,
                border_radius=ft.BorderRadius(
                    top_left=size * 0.02,
                    top_right=size * 0.02,
                    bottom_left=size * 0.06,
                    bottom_right=size * 0.06,
                ),
                bgcolor=OWL_BEAK,
            ),
            # Kairysis koja
            ft.Container(
                width=size * 0.12,
                height=size * 0.08,
                left=size * 0.28,
                top=size * 0.88,
                border_radius=size * 0.04,
                bgcolor=OWL_BEAK,
            ),
            # Dešinysis koja
            ft.Container(
                width=size * 0.12,
                height=size * 0.08,
                right=size * 0.28,
                top=size * 0.88,
                border_radius=size * 0.04,
                bgcolor=OWL_BEAK,
            ),
        ],
    )