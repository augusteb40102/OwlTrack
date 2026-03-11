import flet as ft
from ui.themes.themes import *
from database import save_avatar as db_save_avatar

RADIUS_LG = 20
SPACE_LG = 24

PROFILE_AVATARS = [
    {"id": 1, "src": "greenpele.png",  "name": "Green"},
    {"id": 2, "src": "pinkpele.png",   "name": "Pink"},
    {"id": 3, "src": "greypele.png",   "name": "Grey"},
    {"id": 4, "src": "bluepele.png",   "name": "Blue"},
    {"id": 5, "src": "rudaspele.png",  "name": "Brown"},
    {"id": 6, "src": "purplepele.png", "name": "Purple"},
]

def dashboard_view(page: ft.Page):
    username  = "User"
    avatar_src = None
    user_email = "user@example.com"

    if hasattr(page, "data") and page.data:
        username   = page.data.get("register_name", "User")
        avatar_src = page.data.get("avatar_src", None)
        user_email = page.data.get("register_email", "user@example.com")

    selected_id  = [None]
    avatar_refs  = {}

    # pre-select current avatar
    for av in PROFILE_AVATARS:
        if av["src"] == avatar_src:
            selected_id[0] = av["id"]
            break

    # ── LOGOUT OVERLAY ───────────────────────────────────────────────
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
                    ft.Text("Are you sure you want to log out?", size=13, color=TEXT_SECONDARY),
                    ft.Container(height=24),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Cancel", size=13, color=TEXT_SECONDARY, weight="w600"),
                                on_click=lambda e: hide_logout(),
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

    def hide_logout():
        logout_overlay.visible = False
        page.update()

    def logout(e):
        logout_overlay.visible = True
        page.update()

    # ── SETTINGS WINDOW ──────────────────────────────────────────────
    settings_maximized = [False]
    maximize_icon = ft.Icon(icon=ft.Icons.FULLSCREEN, color=TEXT_ON_PRIMARY, size=18)

    def on_avatar_select(avatar_id):
        for aid, container in avatar_refs.items():
            container.border = ft.border.all(3, TRANSPARENT)
            container.scale  = 1.0
        if avatar_id in avatar_refs:
            avatar_refs[avatar_id].border = ft.border.all(3, SECONDARY)
            avatar_refs[avatar_id].scale  = 1.08
        selected_id[0] = avatar_id
        page.update()

    def close_settings(e):
        settings_overlay.visible = False
        page.update()

    def toggle_maximize(e):
        settings_maximized[0] = not settings_maximized[0]
        if settings_maximized[0]:
            settings_window.width  = page.width  or 900
            settings_window.height = page.height or 650
            settings_window.border_radius = 0
            maximize_icon.icon = ft.Icons.FULLSCREEN_EXIT
        else:
            settings_window.width  = 520
            settings_window.height = 480
            settings_window.border_radius = 16
            maximize_icon.icon = ft.Icons.FULLSCREEN
        page.update()

    def save_settings(e):
        if selected_id[0] is None:
            close_settings(e)
            return
        chosen = next((a for a in PROFILE_AVATARS if a["id"] == selected_id[0]), None)
        if chosen:
            if not hasattr(page, "data") or page.data is None:
                page.data = {}
            page.data["avatar_src"] = chosen["src"]
            if user_email:
                db_save_avatar(user_email, chosen["src"])
            avatar_slot.content = build_avatar_content(chosen["src"])
        settings_overlay.visible = False
        page.update()

    # Build avatar grid – same style as profile_photo_view
    avatar_items = []
    for avatar in PROFILE_AVATARS:
        is_selected = avatar["id"] == selected_id[0]
        img = ft.Image(src=avatar["src"], width=90, height=90, fit="contain")
        name_text = ft.Text(
            avatar["name"],
            size=11,
            color=TEXT_SECONDARY,
            text_align=ft.TextAlign.CENTER,
            weight="w500",
        )
        container = ft.Container(
            content=ft.Column(
                [img, name_text],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            width=115,
            height=130,
            border_radius=12,
            bgcolor=OVERLAY_SURFACE,
            border=ft.border.all(3, SECONDARY if is_selected else TRANSPARENT),
            scale=1.08 if is_selected else 1.0,
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, aid=avatar["id"]: on_avatar_select(aid),
            ink=True,
        )
        avatar_refs[avatar["id"]] = container
        avatar_items.append(container)

    avatar_grid = ft.GridView(
        controls=avatar_items,
        runs_count=3,
        max_extent=130,
        spacing=16,
        run_spacing=16,
        expand=False,
    )

    settings_window = ft.Container(
        width=520,
        height=480,
        border_radius=16,
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            [
                # Title bar
                ft.Container(
                    bgcolor=PRIMARY,
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    content=ft.Row(
                        [
                            ft.Text("Settings", size=15, weight="bold", color=TEXT_ON_PRIMARY),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=maximize_icon,
                                        on_click=toggle_maximize,
                                        ink=True,
                                        border_radius=4,
                                        padding=4,
                                        tooltip="Expand",
                                    ),
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.CLOSE, color=TEXT_ON_PRIMARY, size=18),
                                        on_click=close_settings,
                                        ink=True,
                                        border_radius=4,
                                        padding=4,
                                        tooltip="Close",
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                # Body
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(28),
                    content=ft.Column(
                        [
                            ft.Text("Change Profile Photo", size=15, weight="bold", color=TEXT_PRIMARY),
                            ft.Container(height=4),
                            ft.Text("Select an avatar below", size=12, color=TEXT_SECONDARY),
                            ft.Container(height=20),
                            ft.Container(
                                content=avatar_grid,
                                width=420,
                                height=300,
                            ),
                            ft.Container(expand=True),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text("Cancel", size=13, color=TEXT_SECONDARY, weight="w600"),
                                        on_click=close_settings,
                                        ink=True,
                                        border_radius=8,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        border=ft.border.all(1, BORDER),
                                    ),
                                    ft.Container(
                                        content=ft.Text("Save", size=13, color=TEXT_ON_PRIMARY, weight="w600"),
                                        on_click=save_settings,
                                        ink=True,
                                        border_radius=8,
                                        padding=ft.padding.symmetric(horizontal=28, vertical=10),
                                        gradient=ft.LinearGradient(
                                            begin=ft.Alignment(-1, 0),
                                            end=ft.Alignment(1, 0),
                                            colors=[SECONDARY, PRIMARY],
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                spacing=10,
                            ),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )

    settings_overlay = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=settings_window,
    )

    def open_settings(e):
        settings_maximized[0] = False
        settings_window.width  = 520
        settings_window.height = 480
        settings_window.border_radius = 16
        maximize_icon.icon = ft.Icons.FULLSCREEN
        settings_overlay.visible = True
        page.update()

    # ── AVATAR WIDGET (dinamiškas) ───────────────────────────────────
    def build_avatar_content(src):
        if src:
            return ft.Image(src=src, width=90, height=90, fit="contain")
        return ft.Container(
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

    avatar_slot = ft.Container(
        content=build_avatar_content(avatar_src),
        width=90,
        height=90,
        alignment=ft.Alignment(0, 0),
    )

    # ── EMAIL EXPAND ─────────────────────────────────────────────────
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

    arrow_icon = ft.Icon(icon=ft.Icons.KEYBOARD_ARROW_DOWN, color=TEXT_ON_PRIMARY, size=16, opacity=0.7)
    expanded = [False]

    def toggle_email(e):
        expanded[0] = not expanded[0]
        if expanded[0]:
            email_container.height  = 22
            email_container.opacity = 1
            arrow_icon.icon = ft.Icons.KEYBOARD_ARROW_UP
        else:
            email_container.height  = 0
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

    # Settings mygtukas – mažesnis, šalia vardo
    settings_inline_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SETTINGS, color=TEXT_ON_PRIMARY, size=14),
                ft.Text("Settings", size=12, color=TEXT_ON_PRIMARY, weight="w500"),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=open_settings,
        ink=True,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, TEXT_ON_PRIMARY)),
    )

    top = ft.Column(
        [
            ft.Container(
                content=ft.Text("OwlTrack", size=24, weight="bold", color=TEXT_ON_PRIMARY),
                padding=ft.padding.only(top=20, bottom=20),
                alignment=ft.Alignment(0, 0),
            ),
            avatar_slot,
            ft.Container(height=8),
            username_row,
            email_container,
            ft.Container(height=10),
            settings_inline_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # ── LOG OUT BUTTON (bottom) ───────────────────────────────────────
    logout_btn = ft.Container(
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
                logout_btn,
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
                    ft.Row([sidebar, main_content], spacing=0, expand=True),
                    logout_overlay,
                    settings_overlay,
                ],
                expand=True,
            )
        ],
        expand=True,
        padding=0,
    )