# UI komponentas vartotojo profilio nuotraukos pasirinkimui.
import flet as ft
from ui.themes.backgrounds import auth_background
from database import save_avatar

# ── Fiksuotos purple spalvos – nesikeičia su tema ─────────────────────────────
_SECONDARY       = "#7C3AED"
_TEXT_ON_PRIMARY = "#FFFFFF"
_TEXT_SECONDARY  = "#6B5A9E"
_TRANSPARENT     = ft.Colors.TRANSPARENT
_OVERLAY_SURFACE = "#1A1A2E80"
_BACKGROUND_DARK = "#0D0D1A"

PROFILE_AVATARS = [
    {"id": 1, "src": "greenpele.png",  "name": "Green"},
    {"id": 2, "src": "pinkpele.png",   "name": "Pink"},
    {"id": 3, "src": "greypele.png",   "name": "Grey"},
    {"id": 4, "src": "bluepele.png",   "name": "Blue"},
    {"id": 5, "src": "rudaspele.png",  "name": "Brown"},
    {"id": 6, "src": "purplepele.png", "name": "Purple"},
]

def profile_photo_view(page: ft.Page):
    selected_id = [None]
    avatar_refs = {}

    username = ""
    email    = ""
    if hasattr(page, "data") and page.data:
        username = page.data.get("register_name", "")
        email    = page.data.get("register_email", "")

    def on_avatar_select(avatar_id):
        for aid, (container, _) in avatar_refs.items():
            container.border = ft.border.all(3, _TRANSPARENT)
            container.scale  = 1.0
        if avatar_id in avatar_refs:
            container, _ = avatar_refs[avatar_id]
            container.border = ft.border.all(3, _SECONDARY)
            container.scale  = 1.08
        selected_id[0] = avatar_id
        confirm_btn.disabled = False
        confirm_btn.opacity  = 1.0
        page.update()

    def confirm_selection(e):
        if selected_id[0] is None:
            return
        chosen = next((a for a in PROFILE_AVATARS if a["id"] == selected_id[0]), None)
        if chosen:
            if not hasattr(page, "data") or page.data is None:
                page.data = {}
            page.data["avatar_src"] = chosen["src"]
            if email:
                save_avatar(email, chosen["src"])
        page.go("/dashboard")

    avatar_grid_items = []
    for avatar in PROFILE_AVATARS:
        img = ft.Image(src=avatar["src"], width=90, height=90, fit="contain")
        name_text = ft.Text(
            avatar["name"], size=11, color=_TEXT_SECONDARY,
            text_align=ft.TextAlign.CENTER, weight="w500",
        )
        container = ft.Container(
            content=ft.Column(
                [img, name_text],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6,
            ),
            width=115, height=130, border_radius=12,
            bgcolor=_OVERLAY_SURFACE,
            border=ft.border.all(3, _TRANSPARENT),
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, aid=avatar["id"]: on_avatar_select(aid),
            ink=True,
        )
        avatar_refs[avatar["id"]] = (container, avatar)
        avatar_grid_items.append(container)

    confirm_btn = ft.ElevatedButton(
        "Confirm Selection",
        width=320, height=48,
        disabled=True, opacity=0.4,
        on_click=confirm_selection,
        style=ft.ButtonStyle(
            bgcolor={"": _SECONDARY},
            color={"": _TEXT_ON_PRIMARY},
            shape=ft.RoundedRectangleBorder(radius=8),
            text_style=ft.TextStyle(size=15, weight="bold"),
            elevation={"": 0},
            animation_duration=200,
        ),
    )

    grid = ft.GridView(
        controls=avatar_grid_items,
        runs_count=3, max_extent=130,
        spacing=16, run_spacing=16, expand=False,
    )

    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=30),
                ft.Text(
                    f"Hello, {username}!" if username else "Hello!",
                    size=38, weight="bold",
                    color=_TEXT_ON_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Choose your profile avatar",
                    size=14, color=_TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=24),
                ft.Container(content=grid, width=420, bgcolor=_TRANSPARENT),
                ft.Container(height=28),
                confirm_btn,
                ft.TextButton(
                    "Skip",
                    on_click=lambda e: page.go("/dashboard"),
                    style=ft.ButtonStyle(color={"": _TEXT_SECONDARY}),
                ),
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        alignment=ft.Alignment(0, -1),
    )

    return ft.View(
        route="/profile-photo",
        controls=[auth_background(content)],
        expand=True,
        padding=0,
        bgcolor=_BACKGROUND_DARK,
    )