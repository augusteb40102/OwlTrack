import flet as ft
import ui.themes.themes as th
from ui.themes.themes import apply_theme, THEMES
from ui.components.calendar_widget import build_calendar
from ui.components.todo_widget import build_todo
from ui.components.grade_calculator_widget import build_grade_calculator

from database import save_avatar as db_save_avatar
from database import change_user_password as db_change_user_password
from database import save_theme as db_save_theme
from database import get_theme as db_get_theme

RADIUS_LG = 20
SPACE_LG  = 24

PROFILE_AVATARS = [
    {"id": 1, "src": "greenpele.png",  "name": "Green"},
    {"id": 2, "src": "pinkpele.png",   "name": "Pink"},
    {"id": 3, "src": "greypele.png",   "name": "Grey"},
    {"id": 4, "src": "bluepele.png",   "name": "Blue"},
    {"id": 5, "src": "rudaspele.png",  "name": "Brown"},
    {"id": 6, "src": "purplepele.png", "name": "Purple"},
]

THEME_OPTIONS = [
    {"id": "purple", "label": "Purple (default)", "dot": "#7C3AED"},
    {"id": "blue",   "label": "Blue",              "dot": "#3A7AED"},
    {"id": "grey",   "label": "Grey",              "dot": "#5A5A5A"},
    {"id": "green",  "label": "Green",             "dot": "#22c55e"},
]

# ---------------------------------------------------------------------------
# Grade calculator duomenys (vėliau pakeisti DB)
# ---------------------------------------------------------------------------
_SAMPLE_MODULES = [
    {"name": "Matematika", "grade": 8.7, "weight": 9.0},
    {"name": "Istorija",   "grade": 7.0, "weight": 9.0},
]
_GOAL = 9.0


def dashboard_view(page: ft.Page):
    username   = "User"
    avatar_src = None
    user_email = "user@example.com"

    if hasattr(page, "data") and page.data:
        username   = page.data.get("register_name", "User")
        avatar_src = page.data.get("avatar_src", None)
        user_email = page.data.get("register_email", "user@example.com")

    current_theme = "purple"
    if hasattr(page, "data") and page.data and page.data.get("theme"):
        current_theme = page.data["theme"]
    else:
        current_theme = db_get_theme(user_email) if user_email else "purple"

    apply_theme(current_theme)
    if hasattr(page, "data") and page.data is not None:
        page.data["theme"] = current_theme

    def c(name):
        return getattr(th, name)

    def grad():
        return ft.LinearGradient(
            begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
            colors=[c("SECONDARY"), c("PRIMARY")],
        )

    selected_id    = [None]
    avatar_refs    = {}
    selected_theme = [current_theme]
    theme_btns     = {}

    for av in PROFILE_AVATARS:
        if av["src"] == avatar_src:
            selected_id[0] = av["id"]
            break

    # ── MAIN PANEL ────────────────────────────────────────────────────
    main_panel = ft.Container(expand=True)

    # ── TO-DO LIST ───────────────────────────────────────────────────
    (
        todo_detail_panel,
        get_todo_refs,
        refresh_todo_theme,
        set_todo_home_panel,
        get_upcoming_tasks,
        get_todo_tasks,
        toggle_task_done,
        set_dashboard_widget,
    ) = build_todo(page, c, grad, main_panel, user_email)

    # ── CALENDAR ─────────────────────────────────────────────────────
    compact_calendar, detail_view_panel, get_cal_refs, refresh_cal_theme, set_home_panel = \
        build_calendar(page, c, grad, main_panel, user_email, get_tasks_fn=get_todo_tasks)

    # ── UPCOMING TASKS MINI-WIDGET ────────────────────────────────────
    upcoming_tasks_column = ft.Column(
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def build_task_circle(task):
        is_done = task["completed"]
        inner_dot = ft.Container(
            width=8, height=8, border_radius=4,
            bgcolor=c("TEXT_ON_PRIMARY"),
            visible=is_done,
            alignment=ft.Alignment(0, 0),
        )
        circle = ft.Container(
            width=20, height=20, border_radius=10,
            border=ft.border.all(2, c("PRIMARY") if is_done else c("BORDER")),
            bgcolor=c("PRIMARY") if is_done else ft.Colors.TRANSPARENT,
            content=inner_dot,
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            tooltip="Mark as done" if not is_done else "Completed",
        )
        if not is_done:
            circle.on_click = lambda e, tid=task["id"]: toggle_task_done(tid)
            circle.ink = True
        return circle

    def refresh_upcoming_widget():
        upcoming = get_upcoming_tasks()
        rows = []

        if not upcoming:
            rows.append(
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=32, color=c("BORDER")),
                            ft.Text(
                                "All tasks done!",
                                size=13, color=c("TEXT_SECONDARY"),
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=ft.padding.symmetric(vertical=16),
                )
            )
        else:
            for task in upcoming:
                try:
                    from datetime import datetime as _dt
                    due   = _dt.strptime(task["due_date"], "%Y-%m-%d").date()
                    today = _dt.now().date()
                    delta = (due - today).days
                    if delta == 0:
                        days_label, days_color, days_weight = "Today",    th.ERROR,          "bold"
                    elif delta == 1:
                        days_label, days_color, days_weight = "Tomorrow", c("PRIMARY"),       "bold"
                    elif delta < 0:
                        days_label, days_color, days_weight = f"{abs(delta)}d overdue", th.ERROR, "w400"
                    else:
                        days_label, days_color, days_weight = f"{delta}d left", c("TEXT_SECONDARY"), "w400"
                except ValueError:
                    days_label, days_color, days_weight = "No date", c("TEXT_SECONDARY"), "w400"

                type_colors_map = {
                    "assignment": "#2196F3",
                    "appointment": "#E91E63",
                    "exam": "#9C27B0",
                    "other": "#BDBDBD",
                }
                dot_color = type_colors_map.get((task.get("type") or "").lower(), c("BORDER"))

                row = ft.Container(
                    border_radius=10,
                    border=ft.border.all(1, c("BORDER")),
                    bgcolor=th.TEXT_ON_PRIMARY,
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
                    content=ft.Row(
                        [
                            build_task_circle(task),
                            ft.Column(
                                [
                                    ft.Text(
                                        task["title"], size=12, weight="w600",
                                        color=c("TEXT_PRIMARY"), max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(width=7, height=7, border_radius=4, bgcolor=dot_color),
                                            ft.Text(task.get("type", "Other"), size=10, color=c("TEXT_SECONDARY")),
                                            ft.Text("·", size=10, color=c("TEXT_SECONDARY")),
                                            ft.Text(days_label, size=10, color=days_color, weight=days_weight),
                                        ],
                                        spacing=4,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=2, expand=True,
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
                rows.append(row)

        upcoming_tasks_column.controls = rows

    refresh_upcoming_widget()

    def refresh_dashboard_widgets():
        refresh_upcoming_widget()
        refresh_cal_theme()

    set_dashboard_widget(refresh_dashboard_widgets)

    # ── TO-DO WIDGET (placeholder 1) ──────────────────────────────────
    widget_placeholder_1 = ft.Container(
        expand=True,
        border_radius=RADIUS_LG,
        bgcolor=th.TEXT_ON_PRIMARY,
        border=ft.border.all(2, c("BORDER")),
        padding=ft.padding.all(14),
        on_click=lambda e: (
            setattr(main_panel, "content", todo_detail_panel),
            main_panel.update()
        ),
        ink=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("✔ To Do List", size=13, weight="bold", color=c("TEXT_PRIMARY")),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=12, color=c("TEXT_SECONDARY")),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                upcoming_tasks_column,
            ],
            spacing=0, expand=True,
        ),
    )

    # ── GRADE CALCULATOR ─────────────────────────────────────────────
    gc_modules: list[dict] = list(_SAMPLE_MODULES)
    gc_goal:    list[float] = [_GOAL]

    subj_options = [
        "Matematika", "Istorija", "Fizika", "Chemija",
        "Biologija", "Anglų k.", "Lietuvių k.", "Geografija", "Informatika",
    ]

    def _weighted_avg(mods):
        total_w = sum(m["weight"] for m in mods)
        if not total_w:
            return None
        return sum(m["grade"] * m["weight"] for m in mods) / total_w

    # Shared text refs
    gc_dash_avg   = ft.Text("—", size=28, weight="bold", color=c("TEXT_PRIMARY"))
    gc_dash_goal  = ft.Text(f"{gc_goal[0]:.1f}", size=18, weight="bold", color=c("TEXT_ON_PRIMARY"))
    gc_dash_mods  = ft.Column(spacing=4)

    gc_det_avg    = ft.Text("—", size=22, weight="bold", color=c("TEXT_PRIMARY"))
    gc_det_count  = ft.Text("0",  size=22, weight="bold", color=c("TEXT_PRIMARY"))
    gc_det_status = ft.Text("",  size=12, weight="w500")
    gc_det_table  = ft.Column(spacing=0)

    gc_error_text = ft.Text("", color="#E53935", size=12, visible=False)

    # Detail fields
    gc_subj_dd = ft.Dropdown(
        options=[ft.dropdown.Option(s) for s in subj_options],
        value=subj_options[0], width=160,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    gc_grade_f = ft.TextField(
        label="Pažymys", width=90,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    gc_weight_f = ft.TextField(
        label="Svoris", width=80, value="9",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    gc_goal_f = ft.TextField(
        label="Tikslas", width=80, value=str(gc_goal[0]),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )

    def gc_render_dash():
        avg = _weighted_avg(gc_modules)
        gc_dash_avg.value  = f"{avg:.1f}" if avg is not None else "—"
        gc_dash_goal.value = f"{gc_goal[0]:.1f}"
        rows = []
        for m in gc_modules:
            rows.append(ft.Row([
                ft.Text(m["name"],           size=12, color=c("TEXT_PRIMARY"), expand=True),
                ft.Text(f"{m['grade']:.1f}", size=12, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Text(f"×{m['weight']:.0f}", size=11, color=c("TEXT_SECONDARY"),
                        width=28, text_align=ft.TextAlign.RIGHT),
            ], spacing=6))
        gc_dash_mods.controls = rows if rows else [
            ft.Text("Nėra modulių", size=12, color=c("TEXT_SECONDARY"))
        ]

    def gc_render_detail():
        avg = _weighted_avg(gc_modules)
        gc_det_avg.value   = f"{avg:.1f}" if avg is not None else "—"
        gc_det_count.value = str(len(gc_modules))

        if avg is None:
            gc_det_status.value = ""
        elif avg >= gc_goal[0]:
            gc_det_status.value = "✓ Tikslas pasiektas"
            gc_det_status.color = c("PRIMARY")
        else:
            gc_det_status.value = f"Trūksta {gc_goal[0] - avg:.1f} balo"
            gc_det_status.color = "#E53935"

        rows = [
            ft.Container(
                padding=ft.padding.symmetric(vertical=6),
                border=ft.border.only(bottom=ft.BorderSide(1, c("BORDER"))),
                content=ft.Row([
                    ft.Text("Dalykas",  size=11, color=c("TEXT_SECONDARY"), weight="w500", expand=True),
                    ft.Text("Pažymys", size=11, color=c("TEXT_SECONDARY"), weight="w500",
                            width=60, text_align=ft.TextAlign.CENTER),
                    ft.Text("Svoris",  size=11, color=c("TEXT_SECONDARY"), weight="w500",
                            width=50, text_align=ft.TextAlign.CENTER),
                    ft.Container(width=28),
                ], spacing=4),
            )
        ]
        for i, m in enumerate(gc_modules):
            rows.append(
                ft.Container(
                    padding=ft.padding.symmetric(vertical=8),
                    border=ft.border.only(bottom=ft.BorderSide(1, c("BORDER"))),
                    content=ft.Row([
                        ft.Text(m["name"], size=13, color=c("TEXT_PRIMARY"), expand=True),
                        ft.Text(f"{m['grade']:.1f}", size=13, weight="bold",
                                color=c("TEXT_PRIMARY"), width=60, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"{m['weight']:.0f}", size=12, color=c("TEXT_SECONDARY"),
                                width=50, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE, icon_size=14,
                            icon_color=c("TEXT_SECONDARY"),
                            width=28, height=28,
                            on_click=lambda e, ii=i: gc_remove(ii),
                            tooltip="Pašalinti",
                        ),
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                )
            )
        gc_det_table.controls = rows

    def gc_refresh():
        gc_render_dash()
        gc_render_detail()
        page.update()

    def gc_add(e):
        gc_error_text.visible = False
        try:
            g = float((gc_grade_f.value or "").replace(",", "."))
            w = float((gc_weight_f.value or "9").replace(",", "."))
        except ValueError:
            gc_error_text.value   = "Pažymys ir svoris turi būti skaičiai"
            gc_error_text.visible = True
            page.update()
            return
        if not (1 <= g <= 10):
            gc_error_text.value   = "Pažymys turi būti tarp 1 ir 10"
            gc_error_text.visible = True
            page.update()
            return
        gc_modules.append({"name": gc_subj_dd.value, "grade": g, "weight": w})
        gc_grade_f.value = ""
        gc_refresh()

    def gc_remove(idx: int):
        if 0 <= idx < len(gc_modules):
            gc_modules.pop(idx)
            gc_refresh()

    def gc_goal_changed(e):
        try:
            gc_goal[0] = float((gc_goal_f.value or "9").replace(",", "."))
        except ValueError:
            pass
        gc_refresh()

    gc_goal_f.on_change = gc_goal_changed

    # ── Grade calculator: detail panel ───────────────────────────────
    gc_add_btn = ft.Container(
        content=ft.Text("Pridėti", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
        on_click=gc_add, ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=18, vertical=9),
        gradient=grad(), alignment=ft.Alignment(0, 0),
    )

    gc_detail_header = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        gradient=grad(),
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_size=16, icon_color=c("TEXT_ON_PRIMARY"),
                    on_click=lambda e: _gc_go_home(),
                    tooltip="Grįžti",
                ),
                ft.Text("Pažymių skaičiuoklė", size=15, weight="bold",
                        color=c("TEXT_ON_PRIMARY"), expand=True),
            ],
            spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    gc_summary_row = ft.Row(
        [
            ft.Container(
                expand=True, border_radius=12,
                bgcolor=c("SURFACE"), border=ft.border.all(1, c("BORDER")),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=ft.Column(
                    [ft.Text("Svertinis vidurkis", size=11, color=c("TEXT_SECONDARY"), weight="w500"), gc_det_avg],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                expand=True, border_radius=12,
                bgcolor=c("SURFACE"), border=ft.border.all(1, c("BORDER")),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=ft.Column(
                    [ft.Text("Dalykų skaičius", size=11, color=c("TEXT_SECONDARY"), weight="w500"), gc_det_count],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ],
        spacing=10,
    )

    gc_detail_panel = ft.Container(
        expand=True,
        border=ft.border.all(1, c("BORDER")),
        border_radius=RADIUS_LG,
        bgcolor=c("SURFACE"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            [
                gc_detail_header,
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(16),
                    content=ft.Column(
                        [
                            ft.Row(
                                [gc_subj_dd, gc_grade_f, gc_weight_f, gc_add_btn],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                wrap=True,
                            ),
                            gc_error_text,
                            ft.Container(height=8),
                            ft.Container(
                                expand=True,
                                content=ft.Column(
                                    [gc_det_table],
                                    scroll=ft.ScrollMode.AUTO,
                                    expand=True,
                                ),
                            ),
                            ft.Container(height=12),
                            gc_summary_row,
                            ft.Container(height=8),
                            ft.Row(
                                [
                                    ft.Text("Tikslas:", size=13, color=c("TEXT_SECONDARY")),
                                    gc_goal_f,
                                    gc_det_status,
                                ],
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=4, expand=True,
                    ),
                ),
            ],
            spacing=0, expand=True,
        ),
    )

    def _gc_go_home():
        main_panel.content = home_panel
        main_panel.update()

    def _gc_open_detail():
        gc_render_detail()
        main_panel.content = gc_detail_panel
        main_panel.update()

    # ── Grade calculator: compact dashboard widget ────────────────────
    gc_goal_badge = ft.Container(
        content=ft.Column(
            [
                ft.Text("TIKSLAS", size=9, color=c("TEXT_ON_PRIMARY"), weight="w500",
                        text_align=ft.TextAlign.CENTER),
                gc_dash_goal,
            ],
            spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        border_radius=10, gradient=grad(), alignment=ft.Alignment(0, 0),
    )

    (
        widget_placeholder_2,
        gc_detail_panel,
        refresh_grade_theme,
        set_gc_home_panel,
    ) = build_grade_calculator(page, c, grad, main_panel, user_email)

    # Pradinis render
    gc_render_dash()
    gc_render_detail()

    # ── RIGHT COLUMN ──────────────────────────────────────────────────
    right_column = ft.Column(
        [widget_placeholder_1, widget_placeholder_2],
        spacing=12, expand=False, width=280,
    )

    home_panel = ft.Container(
        expand=True,
        content=ft.Row(
            [compact_calendar, ft.Container(width=12), right_column],
            spacing=0, expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    main_panel.content = home_panel
    set_home_panel(home_panel)
    set_gc_home_panel(home_panel)
    set_todo_home_panel(home_panel)

    # ── AVATAR WIDGET ─────────────────────────────────────────────────
    def build_avatar_content(src):
        if src:
            return ft.Image(src=src, width=90, height=90, fit="contain")
        return ft.Container(
            content=ft.Text(
                username[0].upper() if username else "U",
                size=28, weight="bold", color=c("TEXT_ON_PRIMARY"),
                text_align=ft.TextAlign.CENTER,
            ),
            width=72, height=72,
            border_radius=ft.border_radius.all(36),
            bgcolor=c("SECONDARY"),
            alignment=ft.Alignment(0, 0),
        )

    avatar_slot = ft.Container(
        content=build_avatar_content(avatar_src),
        width=90, height=90, alignment=ft.Alignment(0, 0),
    )

    # ── LOGOUT OVERLAY ────────────────────────────────────────────────
    logout_title      = ft.Text("Log Out", size=18, weight="bold", color=c("TEXT_PRIMARY"))
    logout_subtitle   = ft.Text("Are you sure you want to log out?", size=13, color=c("TEXT_SECONDARY"))
    logout_cancel_btn = ft.Container(
        content=ft.Text("Cancel", size=13, color=c("TEXT_SECONDARY"), weight="w600"),
        on_click=lambda e: hide_logout(),
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border=ft.border.all(1, c("BORDER")),
    )
    logout_confirm_btn = ft.Container(
        content=ft.Text("Log Out", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
        on_click=lambda e: (
            page.clear_session() if hasattr(page, "clear_session") else None,
            setattr(page, "data", {}),
            page.go("/login")
        )[2],
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=c("PRIMARY"),
    )
    logout_dialog_box = ft.Container(
        width=300, padding=ft.padding.all(28),
        border_radius=16, bgcolor=c("SURFACE"),
        border=ft.border.all(1, c("BORDER")),
        content=ft.Column(
            [
                logout_title, ft.Container(height=8), logout_subtitle,
                ft.Container(height=24),
                ft.Row([logout_cancel_btn, logout_confirm_btn],
                       alignment=ft.MainAxisAlignment.END, spacing=10),
            ],
            spacing=0, tight=True,
        ),
    )
    logout_overlay = ft.Container(
        visible=False, expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=logout_dialog_box,
    )

    def hide_logout():
        logout_overlay.visible = False
        page.update()

    def logout(e):
        logout_overlay.visible = True
        page.update()

    # ── HELP OVERLAY ─────────────────────────────────────────────────
    def hide_help():
        help_overlay.visible = False
        page.update()

    def open_help(e):
        help_overlay.visible = True
        page.update()

    help_dialog_box = ft.Container(
        width=340, padding=ft.padding.all(28),
        border_radius=16, bgcolor=c("SURFACE"),
        border=ft.border.all(1, c("BORDER")),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("About us & Help", size=18, weight="bold", color=c("TEXT_PRIMARY")),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLOSE, color=c("TEXT_SECONDARY"), size=18),
                            on_click=lambda e: hide_help(),
                            ink=True, border_radius=4, padding=4, tooltip="Close",
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                ft.Divider(height=1, color=c("BORDER")),
                ft.Container(height=16),
                ft.Text("Meet the team", size=13, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Container(height=10),
                ft.Text("We are three informatics students on a mission to simplify student life. We built OwlTrack to help you stay on top of your academic goals and track your progress effortlessly.", size=12, color=c("TEXT_SECONDARY")),
                ft.Container(height=16),
                ft.Text("Contacts", size=13, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.EMAIL, size=14, color=c("PRIMARY")),
                    ft.Text("owltrackteam@gmail.com", size=12, color=c("TEXT_SECONDARY")),
                ], spacing=6),
                ft.Container(height=8),
               
            ],
            spacing=4, tight=True,
        ),
    )

    help_overlay = ft.Container(
        visible=False, expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=help_dialog_box,
    )

    # ── SETTINGS ─────────────────────────────────────────────────────
    settings_maximized = [False]
    maximize_icon = ft.Icon(icon=ft.Icons.FULLSCREEN, color=c("TEXT_ON_PRIMARY"), size=18)

    def on_avatar_select(avatar_id):
        for aid, container in avatar_refs.items():
            container.border = ft.border.all(3, ft.Colors.TRANSPARENT)
            container.scale  = 1.0
        if avatar_id in avatar_refs:
            avatar_refs[avatar_id].border = ft.border.all(3, c("SECONDARY"))
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
            settings_window.height = 680
            settings_window.border_radius = 16
            maximize_icon.icon = ft.Icons.FULLSCREEN
        page.update()

    def on_theme_select(theme_id: str):
        selected_theme[0] = theme_id
        for tid, row in theme_btns.items():
            label    = row.controls[1]
            border_c = c("SECONDARY") if tid == theme_id else ft.Colors.with_opacity(0.15, c("TEXT_PRIMARY"))
            row.parent.border = ft.border.all(2, border_c)
            label.weight = "bold" if tid == theme_id else "w400"
        page.update()

    def build_theme_picker() -> ft.Row:
        items = []
        for opt in THEME_OPTIONS:
            is_active = opt["id"] == selected_theme[0]
            dot   = ft.Container(width=14, height=14, border_radius=7, bgcolor=opt["dot"])
            label = ft.Text(opt["label"], size=12, color=c("TEXT_PRIMARY"),
                            weight="bold" if is_active else "w400")
            row   = ft.Row([dot, label], spacing=6, alignment=ft.MainAxisAlignment.CENTER)
            theme_btns[opt["id"]] = row
            btn = ft.Container(
                content=row,
                border=ft.border.all(2, c("SECONDARY") if is_active else ft.Colors.with_opacity(0.15, c("TEXT_PRIMARY"))),
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                on_click=lambda e, tid=opt["id"]: on_theme_select(tid),
                ink=True,
            )
            items.append(btn)
        return ft.Row(items, spacing=8, wrap=True)

    old_password_field = ft.TextField(
        label="Enter current password", width=420,
        password=True, can_reveal_password=True,
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
        text_style=ft.TextStyle(color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
    )
    new_password_field = ft.TextField(
        label="Enter new password", width=420,
        password=True, can_reveal_password=True,
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
        text_style=ft.TextStyle(color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
    )
    repeat_new_password_field = ft.TextField(
        label="Repeat new password", width=420,
        password=True, can_reveal_password=True,
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
        text_style=ft.TextStyle(color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
    )
    password_error_text   = ft.Text("", color=th.ERROR,     size=12, visible=False)
    password_success_text = ft.Text("", color=c("PRIMARY"), size=12, visible=False)

    confirm_pw_btn = ft.Container(
        content=ft.Text("Confirm", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
        on_click=lambda e: submit_password_change(e),
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        gradient=grad(), alignment=ft.Alignment(0, 0), width=150,
    )
    settings_cancel_btn = ft.Container(
        content=ft.Text("Cancel", size=13, color=c("TEXT_SECONDARY"), weight="w600"),
        on_click=close_settings,
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border=ft.border.all(1, c("BORDER")),
    )
    settings_save_btn = ft.Container(
        content=ft.Text("Save", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
        on_click=lambda e: save_settings(e),
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=28, vertical=10),
        gradient=grad(),
    )

    # ── SAVE SETTINGS ────────────────────────────────────────────────
    def save_settings(e):
        if selected_id[0] is not None:
            chosen = next((a for a in PROFILE_AVATARS if a["id"] == selected_id[0]), None)
            if chosen:
                if not hasattr(page, "data") or page.data is None:
                    page.data = {}
                page.data["avatar_src"] = chosen["src"]
                if user_email:
                    db_save_avatar(user_email, chosen["src"])
                avatar_slot.content = build_avatar_content(chosen["src"])

        new_theme = selected_theme[0]
        if user_email:
            db_save_theme(user_email, new_theme)
        if hasattr(page, "data") and page.data is not None:
            page.data["theme"] = new_theme

        apply_theme(new_theme)

        # Sidebar
        sidebar.bgcolor                     = c("PRIMARY")
        sidebar.content.controls[0].bgcolor = c("PRIMARY")
        logout_btn.gradient                 = grad()
        main_content.bgcolor                = c("SURFACE")

        # Settings
        settings_title_bar.bgcolor        = c("PRIMARY")
        settings_window.bgcolor           = c("SURFACE")
        settings_window.border            = ft.border.all(1, c("BORDER"))
        confirm_pw_btn.gradient           = grad()
        settings_save_btn.gradient        = grad()
        settings_cancel_btn.border        = ft.border.all(1, c("BORDER"))
        settings_cancel_btn.content.color = c("TEXT_SECONDARY")

        # Logout
        logout_dialog_box.bgcolor        = c("SURFACE")
        logout_dialog_box.border         = ft.border.all(1, c("BORDER"))
        logout_title.color               = c("TEXT_PRIMARY")
        logout_subtitle.color            = c("TEXT_SECONDARY")
        logout_cancel_btn.border         = ft.border.all(1, c("BORDER"))
        logout_cancel_btn.content.color  = c("TEXT_SECONDARY")
        logout_confirm_btn.bgcolor       = c("PRIMARY")

        # Help
        help_dialog_box.bgcolor = c("SURFACE")
        help_dialog_box.border  = ft.border.all(1, c("BORDER"))

        # Password fields
        for field in [old_password_field, new_password_field, repeat_new_password_field]:
            field.bgcolor              = c("SURFACE")
            field.border_color         = c("BORDER")
            field.focused_border_color = c("PRIMARY")
            field.text_style           = ft.TextStyle(color=c("TEXT_PRIMARY"))
            field.label_style          = ft.TextStyle(color=c("TEXT_SECONDARY"))
        password_success_text.color = c("PRIMARY")

        # Avatar grid
        for aid, container in avatar_refs.items():
            container.border  = ft.border.all(3, c("SECONDARY") if aid == selected_id[0] else ft.Colors.TRANSPARENT)
            container.bgcolor = c("SURFACE")

        # Theme picker
        for tid, row in theme_btns.items():
            is_active = tid == selected_theme[0]
            row.parent.border      = ft.border.all(2, c("SECONDARY") if is_active else ft.Colors.with_opacity(0.15, c("TEXT_PRIMARY")))
            row.controls[1].weight = "bold" if is_active else "w400"

        # Placeholders
        widget_placeholder_1.border = ft.border.all(2, c("BORDER"))
        widget_placeholder_2.border = ft.border.all(2, c("BORDER"))

        # To-do
        refresh_todo_theme()
        refresh_upcoming_widget()

        # Grade calculator
        refresh_grade_theme()

        # Kalendorius
        cal_refs = get_cal_refs()
        cal_refs["compact_calendar"].border      = ft.border.all(2, c("BORDER"))
        cal_refs["compact_month_label"].color    = c("TEXT_PRIMARY")
        cal_refs["compact_year_label"].color     = c("TEXT_PRIMARY")
        cal_refs["cal_prev_icon"].color          = c("TEXT_PRIMARY")
        cal_refs["cal_next_icon"].color          = c("TEXT_PRIMARY")
        cal_refs["yr_prev_icon"].color           = c("TEXT_PRIMARY")
        cal_refs["yr_next_icon"].color           = c("TEXT_PRIMARY")
        cal_refs["detail_view_panel"].border     = ft.border.all(1, c("BORDER"))
        cal_refs["detail_header_box"].gradient   = grad()
        cal_refs["detail_back_btn"].gradient     = grad()
        cal_refs["detail_prev_btn"].content.color = c("TEXT_PRIMARY")
        cal_refs["detail_next_btn"].content.color = c("TEXT_PRIMARY")
        cal_refs["detail_month_label"].color     = c("TEXT_PRIMARY")
        refresh_cal_theme()

        settings_overlay.visible = False
        page.update()

    def validate_new_password(password: str, old_password: str):
        if len(password) < 7:
            return "New password must be at least 7 characters"
        if not any(ch.isupper() for ch in password):
            return "New password must contain at least one uppercase letter"
        if not any(ch.isdigit() for ch in password):
            return "New password must contain at least one number"
        if password == old_password:
            return "New password must be different from current password"
        return None

    def submit_password_change(e):
        password_error_text.visible   = False
        password_success_text.visible = False
        old_password_field.border_color        = c("BORDER")
        new_password_field.border_color        = c("BORDER")
        repeat_new_password_field.border_color = c("BORDER")

        old_pw = (old_password_field.value or "").strip()
        new_pw = (new_password_field.value or "").strip()
        rep_pw = (repeat_new_password_field.value or "").strip()

        if not old_pw or not new_pw or not rep_pw:
            password_error_text.value   = "All password fields are required"
            password_error_text.visible = True
            if not old_pw: old_password_field.border_color        = th.ERROR
            if not new_pw: new_password_field.border_color        = th.ERROR
            if not rep_pw: repeat_new_password_field.border_color = th.ERROR
            page.update()
            return

        err = validate_new_password(new_pw, old_pw)
        if err:
            new_password_field.border_color = th.ERROR
            password_error_text.value       = err
            password_error_text.visible     = True
            page.update()
            return

        if new_pw != rep_pw:
            new_password_field.border_color        = th.ERROR
            repeat_new_password_field.border_color = th.ERROR
            password_error_text.value              = "New passwords do not match"
            password_error_text.visible            = True
            page.update()
            return

        if not user_email:
            password_error_text.value   = "Unable to identify user account"
            password_error_text.visible = True
            page.update()
            return

        result = db_change_user_password(user_email, old_pw, new_pw)
        if not result["success"]:
            password_error_text.value       = result["error"]
            password_error_text.visible     = True
            old_password_field.border_color = th.ERROR
            page.update()
            return

        password_success_text.value   = "Password changed successfully"
        password_success_text.visible = True
        old_password_field.value = ""
        new_password_field.value = ""
        repeat_new_password_field.value = ""
        page.update()

    # ── AVATAR GRID ───────────────────────────────────────────────────
    avatar_items = []
    for avatar in PROFILE_AVATARS:
        is_selected = avatar["id"] == selected_id[0]
        img       = ft.Image(src=avatar["src"], width=90, height=90, fit="contain")
        name_text = ft.Text(avatar["name"], size=11, color=c("TEXT_SECONDARY"),
                            text_align=ft.TextAlign.CENTER, weight="w500")
        container = ft.Container(
            content=ft.Column([img, name_text],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            width=115, height=130, border_radius=12,
            bgcolor=c("SURFACE"),
            border=ft.border.all(3, c("SECONDARY") if is_selected else ft.Colors.TRANSPARENT),
            scale=1.08 if is_selected else 1.0,
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, aid=avatar["id"]: on_avatar_select(aid),
            ink=True,
        )
        avatar_refs[avatar["id"]] = container
        avatar_items.append(container)

    avatar_grid  = ft.GridView(controls=avatar_items, runs_count=3,
                               max_extent=130, spacing=16, run_spacing=16, expand=False)
    theme_picker = build_theme_picker()

    settings_title_bar = ft.Container(
        bgcolor=c("PRIMARY"),
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Row(
            [
                ft.Text("Settings", size=15, weight="bold", color=c("TEXT_ON_PRIMARY")),
                ft.Row(
                    [
                        ft.Container(content=maximize_icon, on_click=toggle_maximize,
                                     ink=True, border_radius=4, padding=4, tooltip="Expand"),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLOSE, color=c("TEXT_ON_PRIMARY"), size=18),
                            on_click=close_settings, ink=True, border_radius=4, padding=4, tooltip="Close"),
                    ],
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    settings_window = ft.Container(
        width=520, height=680, border_radius=16,
        bgcolor=c("SURFACE"), border=ft.border.all(1, c("BORDER")),
        animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            [
                settings_title_bar,
                ft.Container(
                    expand=True, padding=ft.padding.all(28),
                    content=ft.Column(
                        [
                            ft.Text("App Theme", size=15, weight="bold", color=c("TEXT_PRIMARY")),
                            ft.Container(height=4),
                            ft.Text("Choose a colour scheme", size=12, color=c("TEXT_SECONDARY")),
                            ft.Container(height=12),
                            theme_picker,
                            ft.Container(height=20),
                            ft.Divider(height=1, color=c("BORDER")),
                            ft.Container(height=16),
                            ft.Text("Change Profile Photo", size=15, weight="bold", color=c("TEXT_PRIMARY")),
                            ft.Container(height=4),
                            ft.Text("Select an avatar below", size=12, color=c("TEXT_SECONDARY")),
                            ft.Container(height=20),
                            ft.Container(content=avatar_grid, width=420, height=300),
                            ft.Container(height=20),
                            ft.Divider(height=1, color=c("BORDER")),
                            ft.Container(height=16),
                            ft.Text("Change Password", size=15, weight="bold", color=c("TEXT_PRIMARY")),
                            ft.Container(height=6),
                            old_password_field,
                            ft.Container(height=8),
                            new_password_field,
                            ft.Container(height=8),
                            repeat_new_password_field,
                            ft.Container(height=8),
                            password_error_text,
                            password_success_text,
                            ft.Container(height=10),
                            confirm_pw_btn,
                            ft.Container(expand=True),
                            ft.Row([settings_cancel_btn, settings_save_btn],
                                   alignment=ft.MainAxisAlignment.END, spacing=10),
                        ],
                        spacing=0, expand=True, scroll=ft.ScrollMode.AUTO,
                    ),
                ),
            ],
            spacing=0, expand=True,
        ),
    )

    settings_overlay = ft.Container(
        visible=False, expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=settings_window,
    )

    def open_settings(e):
        settings_maximized[0]  = False
        settings_window.width  = 520
        settings_window.height = 680
        settings_window.border_radius = 16
        maximize_icon.icon = ft.Icons.FULLSCREEN
        settings_overlay.visible = True
        page.update()

    email_container = ft.Container(
        content=ft.Text(user_email, size=11, color=c("TEXT_ON_PRIMARY"), opacity=0.75,
                        text_align=ft.TextAlign.CENTER),
        height=0, opacity=0,
        animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        alignment=ft.Alignment(0, 0),
    )

    arrow_icon = ft.Icon(icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                         color=c("TEXT_ON_PRIMARY"), size=16, opacity=0.7)
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
            [ft.Text(username, size=15, weight="bold", color=c("TEXT_ON_PRIMARY")), arrow_icon],
            spacing=2, alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=toggle_email, ink=True, border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    settings_inline_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.SETTINGS, color=c("TEXT_ON_PRIMARY"), size=14),
             ft.Text("Settings", size=12, color=c("TEXT_ON_PRIMARY"), weight="w500")],
            spacing=6, alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=open_settings, ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, c("TEXT_ON_PRIMARY"))),
    )

    help_inline_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.HELP_OUTLINE, color=c("TEXT_ON_PRIMARY"), size=14),
             ft.Text("Help", size=12, color=c("TEXT_ON_PRIMARY"), weight="w500")],
            spacing=6, alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=open_help, ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, c("TEXT_ON_PRIMARY"))),
    )

    dashboard_inline_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.DASHBOARD, color=c("TEXT_ON_PRIMARY"), size=14),
             ft.Text("Dashboard", size=12, color=c("TEXT_ON_PRIMARY"), weight="w500")],
            spacing=6, alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=lambda e: (
            setattr(main_panel, "content", home_panel),
            main_panel.update()
        ),
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, c("TEXT_ON_PRIMARY"))),
    )

    top = ft.Column(
        [
            ft.Container(
                content=ft.Text("OwlTrack", size=24, weight="bold", color=c("TEXT_ON_PRIMARY")),
                padding=ft.padding.only(top=20, bottom=20),
                alignment=ft.Alignment(0, 0),
            ),
            avatar_slot,
            ft.Container(height=8),
            username_row,
            email_container,
            ft.Container(height=10),
            dashboard_inline_btn,
            ft.Container(height=6),
            settings_inline_btn,
            ft.Container(height=6),
            help_inline_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    logout_btn = ft.Container(
        content=ft.Row(
            [ft.Image(src="logout_icon.png", width=20, height=20, fit="contain"),
             ft.Text("Log Out", size=14, color=c("TEXT_ON_PRIMARY"), weight="w600")],
            spacing=10, alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=180, height=44, border_radius=10,
        gradient=grad(),
        alignment=ft.Alignment(0, 0),
        bottom=24, left=20,
        on_click=logout, ink=True,
    )

    sidebar = ft.Container(
        width=220, bgcolor=c("PRIMARY"),
        content=ft.Stack(
            [
                ft.Container(expand=True, bgcolor=c("PRIMARY")),
                ft.Container(content=top, top=0, left=0, right=0),
                logout_btn,
            ],
            expand=True,
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=c("SURFACE"),
        padding=SPACE_LG,
        content=main_panel,
    )

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Stack(
                [
                    ft.Row([sidebar, main_content], spacing=0, expand=True),
                    logout_overlay,
                    settings_overlay,
                    help_overlay,
                ],
                expand=True,
            )
        ],
        expand=True,
        padding=0,
    )