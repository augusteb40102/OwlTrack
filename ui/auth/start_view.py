import flet as ft
import asyncio
from ui.themes.backgrounds import auth_background

# ── Fiksuotos purple spalvos – nesikeičia su tema ─────────────────────────────
_PRIMARY    = "#2D1B69"
_SECONDARY  = "#7C3AED"
_SURFACE    = "#F3EEFF"
_BORDER     = "#2D1B69"
_TEXT_ON_PRIMARY = "#FFFFFF"
_TEXT_ON_SURFACE = "#2D1B69"

_PRIMARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_PRIMARY,
    bgcolor=_PRIMARY,
    shape=ft.RoundedRectangleBorder(radius=10),
)
_SECONDARY_BTN_STYLE = ft.ButtonStyle(
    color=_TEXT_ON_SURFACE,
    bgcolor=_SURFACE,
    shape=ft.RoundedRectangleBorder(radius=10),
    side=ft.BorderSide(width=2, color=_PRIMARY),
)

FONT_XL  = 42
FONT_LG  = 32
SPACE_SM = 8

def start_view(page: ft.Page):

    if not hasattr(page, "data") or page.data is None:
        page.data = {}

    def go_login(e):
        page.go("/login")

    def go_register(e):
        page.go("/register")

    owl = ft.Container(
        content=ft.Image(
            src="owl_clean.png",
            width=110, height=110, fit="contain",
        ),
        opacity=0,
        animate_opacity=800,
    )

    title_text = ft.Text(
        "OwlTrack",
        size=FONT_XL,
        weight="bold",
        color=_TEXT_ON_PRIMARY,
        opacity=0,
        animate_opacity=800,
    )

    buttons = ft.Column(
        [
            ft.ElevatedButton(
                "Log in",
                width=220, height=45,
                opacity=0, animate_opacity=600,
                style=_PRIMARY_BTN_STYLE,
                on_click=go_login,
            ),
            ft.ElevatedButton(
                "Register",
                width=220, height=45,
                opacity=0, animate_opacity=600,
                style=_SECONDARY_BTN_STYLE,
                on_click=go_register,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SPACE_SM,
    )

    content = ft.Column(
        [owl, title_text, buttons],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    async def animate_logo():
        owl.opacity = 1
        title_text.opacity = 1
        page.update()
        await asyncio.sleep(3)

        owl.opacity = 0
        title_text.opacity = 0
        page.update()
        await asyncio.sleep(0.8)

        title_text.size = FONT_LG
        owl.opacity = 1
        title_text.opacity = 1
        buttons.controls[0].opacity = 1
        buttons.controls[1].opacity = 1
        page.update()

    animation_seen = page.data.get("start_animation_seen", False)

    if animation_seen:
        title_text.size = FONT_LG
        owl.opacity = 1
        title_text.opacity = 1
        buttons.controls[0].opacity = 1
        buttons.controls[1].opacity = 1
    else:
        page.data["start_animation_seen"] = True
        page.run_task(animate_logo)

    return ft.View(
        route="/",
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    ft.Image(
                        src="cosmos_purple.gif",
                        width=page.window.width,
                        height=page.window.height,
                        fit="fill",
                    ),
                    ft.Container(
                        content=content,
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                    ),
                ]
            )
        ],
        expand=True,
        padding=0,
    )