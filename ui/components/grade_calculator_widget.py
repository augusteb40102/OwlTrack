import flet as ft
from database import list_modules, create_module, update_module, delete_module

RADIUS_LG = 20

ASSESSMENT_TYPES = [
    "Midterm", "Final Exam", "Project", "Lab Work",
    "Assignment", "Presentation", "Quiz", "Other",
]

_SAMPLE_MODULES = [
    {
        "name": "Data Bases",
        "ects": 6,
        "assessments": [
            {"type": "Midterm 1",  "grade": 8.5, "weight": 30},
            {"type": "Midterm 2",  "grade": 9.0, "weight": 30},
            {"type": "Final Exam", "grade": 9.0, "weight": 40},
        ],
    },
    {
        "name": "Mathematics",
        "ects": 9,
        "assessments": [
            {"type": "Midterm",    "grade": 8.7, "weight": 40},
            {"type": "Final Exam", "grade": 7.5, "weight": 60},
        ],
    },
]

SCHOLARSHIP_THRESHOLD = 8.5


def _module_avg(module: dict) -> float | None:
    assessments = [a for a in module["assessments"] if a.get("grade") is not None]
    if not assessments:
        return None
    total_w = sum(a.get("weight", 100) for a in assessments)
    if not total_w:
        return None
    return sum(a["grade"] * a.get("weight", 100) for a in assessments) / total_w


def _semester_avg(modules: list[dict]) -> float | None:
    weighted, total_ects = 0.0, 0
    for m in modules:
        avg = _module_avg(m)
        if avg is not None:
            weighted   += avg * m["ects"]
            total_ects += m["ects"]
    if not total_ects:
        return None
    return weighted / total_ects


def _total_ects(modules: list[dict]) -> int:
    return sum(m["ects"] for m in modules)


def _is_complete(module: dict) -> bool:
    """Module is complete when total weight of graded assessments reaches 100%."""
    weights = [a.get("weight", 0) for a in module["assessments"] if a.get("grade") is not None]
    return bool(weights) and round(sum(weights)) >= 100


def _score_at_total(module: dict) -> str:
    avg = _module_avg(module)
    if not _is_complete(module) or avg is None:
        return f"0 / {module['ects']:.0f}"
    if avg >= 4.5:
        return f"{module['ects']:.0f} / {module['ects']:.0f}"
    else:
        return f"0 / {module['ects']:.0f}"


# ---------------------------------------------------------------------------
def build_grade_calculator(page: ft.Page, c, grad, main_panel, user_email: str = ""):
    # Load modules from DB for the given user_email. Fallback to sample when no user.
    modules: list[dict] = []
    def load_modules():
        modules.clear()
        if user_email:
            mods = list_modules(user_email)
            for m in mods:
                # Ensure assessments list is mutable
                m["assessments"] = list(m.get("assessments") or [])
                modules.append(m)
        else:
            for m in _SAMPLE_MODULES:
                nm = dict(m)
                nm["assessments"] = list(nm["assessments"]) if nm.get("assessments") else []
                modules.append(nm)

    load_modules()

    home_panel_ref: list = [None]
    editing_index: list  = [None]   # None = add mode, int = edit mode

    # ── shared display refs ──────────────────────────────────────────────
    dash_avg_text  = ft.Text("—", size=26, weight="bold", color=c("TEXT_PRIMARY"))
    dash_ects_text = ft.Text("0", size=13, weight="w500", color=c("TEXT_SECONDARY"))
    dash_rows_col  = ft.Column(spacing=4)
    goal_value: list[float] = [8.5]

    # ── GOAL RING ────────────────────────────────────────────────────────
    RING_SIZE = 54

    def build_goal_ring(current: float | None, goal: float) -> ft.Stack:
        pct = min(max((current or 0) / 10, 0), 1)
        return ft.Stack(
            [
                ft.Container(
                    width=RING_SIZE, height=RING_SIZE,
                    border_radius=RING_SIZE / 2,
                    border=ft.border.all(5, c("BORDER")),
                ),
                ft.Container(
                    width=RING_SIZE, height=RING_SIZE,
                    content=ft.ProgressRing(
                        value=pct,
                        width=RING_SIZE - 4, height=RING_SIZE - 4,
                        stroke_width=5,
                        color=c("PRIMARY"),
                        bgcolor=ft.Colors.TRANSPARENT,
                    ),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(
                    width=RING_SIZE, height=RING_SIZE,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        [
                            ft.Text("GOAL", size=7, color=c("TEXT_SECONDARY"),
                                    weight="w600", text_align=ft.TextAlign.CENTER),
                            ft.Text(f"{goal:.1f}", size=13, weight="bold",
                                    color=c("TEXT_PRIMARY"), text_align=ft.TextAlign.CENTER),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            ],
            width=RING_SIZE, height=RING_SIZE,
        )

    goal_ring_slot = ft.Container(
        width=RING_SIZE, height=RING_SIZE,
        content=build_goal_ring(None, goal_value[0]),
    )

    # ── render compact ───────────────────────────────────────────────────
    def render_dash():
        avg  = _semester_avg(modules)
        ects = _total_ects(modules)
        dash_avg_text.value    = f"{avg:.1f} / 10" if avg is not None else "— / 10"
        dash_ects_text.value   = f"{ects} ECTS total"
        goal_ring_slot.content = build_goal_ring(avg, goal_value[0])
        rows = []
        for m in modules:
            avg_m = _module_avg(m)
            rows.append(
                ft.Row(
                    [
                        ft.Text(m["name"], size=11, color=c("TEXT_PRIMARY"),
                                expand=True, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                        ft.Text(f"{avg_m:.1f}" if avg_m is not None else "—",
                                size=11, weight="bold", color=c("TEXT_PRIMARY"), width=28),
                        ft.Text(f"{m['ects']} cr", size=10, color=c("TEXT_SECONDARY"),
                                width=34, text_align=ft.TextAlign.RIGHT),
                    ],
                    spacing=4,
                )
            )
        if not rows:
            rows.append(ft.Text("No modules yet", size=11, color=c("TEXT_SECONDARY")))
        dash_rows_col.controls = rows

    # ────────────────────────────────────────────────────────────────────
    # ADD / EDIT DIALOG
    # ────────────────────────────────────────────────────────────────────
    dialog_title_text = ft.Text("Add New Module", size=18, weight="bold",
                                 color=c("TEXT_PRIMARY"))
    save_btn_text     = ft.Text("Save Module", size=13, color=c("TEXT_ON_PRIMARY"),
                                 weight="w600")

    new_name_field = ft.TextField(
        label="Module Name", expand=True,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    new_ects_field = ft.TextField(
        label="Credits (ECTS)", width=110, value="6",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(size=13, color=c("TEXT_PRIMARY")),
        label_style=ft.TextStyle(color=c("TEXT_SECONDARY")),
        bgcolor=c("SURFACE"), border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )

    live_rows: list[dict]   = []
    assessment_rows_col     = ft.Column(spacing=8)
    dialog_error_text       = ft.Text("", color="#E53935", size=12, visible=False)

    def _make_row_widget(dd_value: str, grade_value: str, weight_value: str = "") -> tuple:
        dd = ft.Dropdown(
            options=[ft.dropdown.Option(t) for t in ASSESSMENT_TYPES],
            value=dd_value if dd_value in ASSESSMENT_TYPES else ASSESSMENT_TYPES[0],
            width=190,
            text_style=ft.TextStyle(size=12, color=c("TEXT_PRIMARY")),
            bgcolor=c("SURFACE"), border_color=c("BORDER"),
            focused_border_color=c("PRIMARY"),
            label="Assessment Type",
            label_style=ft.TextStyle(color=c("TEXT_SECONDARY"), size=11),
        )
        tf = ft.TextField(
            label="Grade (1–10)", width=95, value=grade_value,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_style=ft.TextStyle(size=12, color=c("TEXT_PRIMARY")),
            label_style=ft.TextStyle(color=c("TEXT_SECONDARY"), size=11),
            bgcolor=c("SURFACE"), border_color=c("BORDER"),
            focused_border_color=c("PRIMARY"),
        )
        wf = ft.TextField(
            label="Weight %", width=85, value=weight_value,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_style=ft.TextStyle(size=12, color=c("TEXT_PRIMARY")),
            label_style=ft.TextStyle(color=c("TEXT_SECONDARY"), size=11),
            bgcolor=c("SURFACE"), border_color=c("BORDER"),
            focused_border_color=c("PRIMARY"),
        )
        entry = {"dd": dd, "tf": tf, "wf": wf}

        def remove_this(e, en=entry):
            if en in live_rows:
                live_rows.remove(en)
            _rebuild_row_widgets()
            page.update()

        row_widget = ft.Row(
            [dd, tf, wf,
             ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                           icon_size=18, icon_color="#E53935",
                           on_click=remove_this, tooltip="Remove")],
            spacing=8, vertical_alignment=ft.CrossAxisAlignment.END,
        )
        return row_widget, entry

    def _rebuild_row_widgets():
        widgets = []
        for en in live_rows:
            def remove_this(e, entry=en):
                if entry in live_rows:
                    live_rows.remove(entry)
                _rebuild_row_widgets()
                page.update()
            widgets.append(
                ft.Row(
                    [en["dd"], en["tf"], en["wf"],
                     ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                   icon_size=18, icon_color="#E53935",
                                   on_click=remove_this, tooltip="Remove")],
                    spacing=8, vertical_alignment=ft.CrossAxisAlignment.END,
                )
            )
        assessment_rows_col.controls = widgets

    def add_blank_row(e=None):
        rw, entry = _make_row_widget(ASSESSMENT_TYPES[0], "")
        live_rows.append(entry)
        assessment_rows_col.controls.append(rw)
        page.update()

    def _seed_rows(assessments: list[dict]):
        live_rows.clear()
        assessment_rows_col.controls = []
        for a in assessments:
            grade_str  = f"{a['grade']:.1f}" if a.get("grade") is not None else ""
            weight_str = str(int(a["weight"])) if a.get("weight") is not None else ""
            rw, entry = _make_row_widget(a["type"], grade_str, weight_str)
            entry["wf"].on_change = lambda _: update_weight_total()
            live_rows.append(entry)
            assessment_rows_col.controls.append(rw)
        if not live_rows:
            add_blank_row_with_update()
        update_weight_total()

    def open_add_dialog(e):
        editing_index[0]          = None
        dialog_title_text.value   = "Add New Module"
        save_btn_text.value       = "Save Module"
        new_name_field.value      = ""
        new_ects_field.value      = "6"
        dialog_error_text.visible = False
        _seed_rows([])
        dialog_overlay.visible = True
        page.update()

    def open_edit_dialog(idx: int):
        editing_index[0]          = idx
        m                         = modules[idx]
        dialog_title_text.value   = "Edit Module"
        save_btn_text.value       = "Save Changes"
        new_name_field.value      = m["name"]
        new_ects_field.value      = str(int(m["ects"]) if m["ects"] == int(m["ects"]) else m["ects"])
        dialog_error_text.visible = False
        _seed_rows(m["assessments"])
        dialog_overlay.visible = True
        page.update()

    def close_dialog(e=None):
        dialog_overlay.visible = False
        page.update()

    def save_module(e):
        dialog_error_text.visible = False
        name = (new_name_field.value or "").strip()
        if not name:
            dialog_error_text.value   = "Module name is required"
            dialog_error_text.visible = True
            page.update()
            return
        try:
            ects = float((new_ects_field.value or "6").replace(",", "."))
        except ValueError:
            dialog_error_text.value   = "ECTS must be a number"
            dialog_error_text.visible = True
            page.update()
            return

        assessments = []
        for entry in live_rows:
            dd = entry.get("dd")
            tf = entry.get("tf")
            wf = entry.get("wf")
            if dd is None or tf is None:
                continue
            grade_str  = (tf.value or "").strip()
            weight_str = (wf.value if wf else "").strip()
            if grade_str:
                try:
                    g = float(grade_str.replace(",", "."))
                    if not (1 <= g <= 10):
                        dialog_error_text.value   = "Grades must be between 1 and 10"
                        dialog_error_text.visible = True
                        page.update()
                        return
                except ValueError:
                    dialog_error_text.value   = "All grades must be valid numbers"
                    dialog_error_text.visible = True
                    page.update()
                    return
                try:
                    w = float(weight_str.replace(",", ".")) if weight_str else None
                    if w is not None and not (0 < w <= 100):
                        dialog_error_text.value   = "Each weight must be between 1 and 100"
                        dialog_error_text.visible = True
                        page.update()
                        return
                except ValueError:
                    dialog_error_text.value   = "Weight must be a valid number"
                    dialog_error_text.visible = True
                    page.update()
                    return
                assessments.append({"type": dd.value, "grade": g, "weight": w})

        # Check total weight — allow < 100 (pending grades), block > 100
        weights_set = [a["weight"] for a in assessments if a["weight"] is not None]
        if weights_set:
            total_w = sum(weights_set)
            if total_w > 100.0 + 0.01:
                dialog_error_text.value   = f"Total weight exceeds 100% ({total_w:.0f}%). Please fix."
                dialog_error_text.visible = True
                page.update()
                return
        else:
            for a in assessments:
                a["weight"] = round(100 / len(assessments), 4) if assessments else 100

        new_data = {"name": name, "ects": ects, "assessments": assessments}
        if editing_index[0] is None:
            # create in DB
            if user_email:
                res = create_module(user_email, name, ects, assessments)
                if res.get("success"):
                    new_data["id"] = res.get("module_id")
                    modules.append(new_data)
                else:
                    dialog_error_text.value = f"Unable to save module: {res.get('error') or 'unknown'}"
                    dialog_error_text.visible = True
                    page.update()
                    return
            else:
                # local-only
                modules.append(new_data)
        else:
            if user_email and modules[editing_index[0]].get("id"):
                module_id = modules[editing_index[0]]["id"]
                res = update_module(module_id, user_email, name, ects, assessments)
                if not res.get("success"):
                    dialog_error_text.value = f"Unable to update module: {res.get('error') or 'unknown'}"
                    dialog_error_text.visible = True
                    page.update()
                    return
                modules[editing_index[0]] = {**modules[editing_index[0]], **new_data}
            else:
                modules[editing_index[0]] = new_data

        close_dialog()
        refresh_all()

    # Dialog layout
    add_assessment_btn = ft.TextButton(
        "+ Add Assessment",
        on_click=add_blank_row,
        style=ft.ButtonStyle(color=c("PRIMARY")),
    )

    weight_total_text = ft.Text("Total weight: 0%", size=11, color=c("TEXT_SECONDARY"))

    def update_weight_total():
        total = 0.0
        for en in live_rows:
            wf = en.get("wf")
            if wf:
                try:
                    total += float((wf.value or "0").replace(",", "."))
                except ValueError:
                    pass
        if total > 100:
            color = "#E53935"
            label = f"Total weight: {total:.0f}% ⚠ over 100%"
        elif round(total) == 100:
            color = "#22c55e"
            label = f"Total weight: {total:.0f}% ✓"
        else:
            color = "#F59E0B"
            label = f"Total weight: {total:.0f}% (incomplete)"
        weight_total_text.value = label
        weight_total_text.color = color
        page.update()

    # Patch add_blank_row to also trigger weight update
    _orig_add_blank = add_blank_row

    def add_blank_row_with_update(e=None):
        rw, entry = _make_row_widget(ASSESSMENT_TYPES[0], "")
        # attach on_change to wf
        entry["wf"].on_change = lambda _: update_weight_total()
        live_rows.append(entry)
        assessment_rows_col.controls.append(rw)
        update_weight_total()
        page.update()

    add_assessment_btn.on_click = add_blank_row_with_update

    dialog_box = ft.Container(
        width=540,
        border_radius=16,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, c("BORDER")),
        shadow=ft.BoxShadow(blur_radius=32,
                            color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK)),
        padding=ft.padding.all(28),
        content=ft.Column(
            [
                dialog_title_text,
                ft.Container(height=16),
                ft.Row([new_name_field, new_ects_field], spacing=12,
                       vertical_alignment=ft.CrossAxisAlignment.END),
                ft.Container(height=14),
                ft.Row(
                    [ft.Text("Assessments", size=13, weight="w600", color=c("TEXT_SECONDARY")),
                     ft.Container(expand=True),
                     weight_total_text],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                assessment_rows_col,
                ft.Container(height=4),
                add_assessment_btn,
                ft.Container(height=4),
                dialog_error_text,
                ft.Container(height=16),
                ft.Row(
                    [
                        ft.Container(
                            content=save_btn_text,
                            on_click=save_module, ink=True, border_radius=8,
                            padding=ft.padding.symmetric(horizontal=24, vertical=10),
                            gradient=grad(), alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(
                            content=ft.Text("Cancel", size=13,
                                            color=c("TEXT_SECONDARY"), weight="w600"),
                            on_click=close_dialog, ink=True, border_radius=8,
                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            border=ft.border.all(1, c("BORDER")),
                        ),
                    ],
                    spacing=10, alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=0, scroll=ft.ScrollMode.AUTO,
        ),
    )

    dialog_overlay = ft.Container(
        visible=False, expand=True,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.BLACK),
        alignment=ft.Alignment(0, 0),
        content=dialog_box,
    )

    # ────────────────────────────────────────────────────────────────────
    # DETAIL PANEL
    # ────────────────────────────────────────────────────────────────────
    det_avg_text   = ft.Text("—",      size=30, weight="bold", color=c("TEXT_PRIMARY"))
    det_ects_text  = ft.Text("0 ECTS", size=22, weight="bold", color=c("TEXT_PRIMARY"))
    det_schol_text = ft.Text("Eligible for Scholarship", size=13,
                              weight="w500", color="#22c55e")
    det_schol_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color="#22c55e", size=16)
    det_table_col  = ft.Column(spacing=0)

    def render_detail():
        avg  = _semester_avg(modules)
        ects = _total_ects(modules)
        det_avg_text.value  = f"{avg:.1f} / 10" if avg is not None else "— / 10"
        det_ects_text.value = f"{ects} ECTS"

        eligible = avg is not None and avg >= SCHOLARSHIP_THRESHOLD
        if eligible:
            det_schol_text.value = "Eligible for Scholarship"
            det_schol_text.color = "#22c55e"
            det_schol_icon.name  = ft.Icons.CHECK_CIRCLE
            det_schol_icon.color = "#22c55e"
        else:
            det_schol_text.value = "Not Eligible"
            det_schol_text.color = "#E53935"
            det_schol_icon.name  = ft.Icons.CANCEL
            det_schol_icon.color = "#E53935"

        def hdr(label, w=None, expand=False):
            return ft.Container(
                width=w, expand=expand,
                content=ft.Text(label, size=11, weight="w600", color=c("TEXT_SECONDARY")),
            )

        header = ft.Container(
            padding=ft.padding.symmetric(vertical=10, horizontal=16),
            border=ft.border.only(bottom=ft.BorderSide(1, c("BORDER"))),
            bgcolor=ft.Colors.WHITE,
            content=ft.Row(
                [hdr("Module Name", expand=True),
                 hdr("Credits", w=70),
                 hdr("Assessments", w=180),
                 hdr("Module Average", w=120),
                 hdr("Score at total", w=110),
                 hdr("Status", w=100),
                 ft.Container(width=76)],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        rows = [header]
        for i, m in enumerate(modules):
            avg_m     = _module_avg(m)
            avg_str   = f"{avg_m:.1f} / 10" if avg_m is not None else "—"
            score_str = _score_at_total(m)

            a_lines = ft.Column(
                [ft.Text(
                    f"{a['type']}: {a['grade']:.1f}" +
                    (f"  ({int(a['weight'])}%)" if a.get("weight") is not None else "")
                    if a.get("grade") is not None else a["type"],
                    size=12, color=c("TEXT_PRIMARY"))
                 for a in m["assessments"]]
                or [ft.Text("—", size=12, color=c("TEXT_SECONDARY"))],
                spacing=2,
            )

            complete = _is_complete(m)
            status_dot = ft.Container(
                width=10, height=10, border_radius=5,
                bgcolor="#BDBDBD" if avg_m is None else
                        ("#22c55e" if complete else c("PRIMARY")),
            )
            status_text = ft.Text(
                "—" if avg_m is None else
                ("Complete" if complete else "In Progress"),
                size=12, color=c("TEXT_SECONDARY"),
            )

            row = ft.Container(
                padding=ft.padding.symmetric(vertical=12, horizontal=16),
                border=ft.border.only(bottom=ft.BorderSide(1, c("BORDER"))),
                content=ft.Row(
                    [
                        ft.Text(m["name"], size=13, color=c("TEXT_PRIMARY"),
                                expand=True, weight="w500"),
                        ft.Text(f"{m['ects']:.0f} ECTS", size=12,
                                color=c("TEXT_SECONDARY"), width=70),
                        ft.Container(content=a_lines, width=180),
                        ft.Text(avg_str, size=13, weight="bold",
                                color=c("TEXT_PRIMARY"), width=120),
                        ft.Text(score_str, size=12, color=c("TEXT_SECONDARY"), width=110),
                        ft.Row([status_dot, status_text], spacing=6, width=100),
                        # Edit + Delete buttons
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_size=16, icon_color=c("PRIMARY"),
                                    width=36, height=36,
                                    on_click=lambda e, ii=i: open_edit_dialog(ii),
                                    tooltip="Edit",
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_size=16, icon_color=c("TEXT_SECONDARY"),
                                    width=36, height=36,
                                    on_click=lambda e, ii=i: remove_module(ii),
                                    tooltip="Remove",
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
            rows.append(row)

        if len(rows) == 1:
            rows.append(
                ft.Container(
                    padding=ft.padding.all(24),
                    content=ft.Text("No modules added yet", size=13,
                                    color=c("TEXT_SECONDARY"),
                                    text_align=ft.TextAlign.CENTER),
                    alignment=ft.Alignment(0, 0),
                )
            )

        det_table_col.controls = rows

    def remove_module(idx: int):
        if 0 <= idx < len(modules):
            mod = modules[idx]
            if user_email and mod.get("id"):
                delete_module(mod.get("id"), user_email)
            modules.pop(idx)
            refresh_all()

    def refresh_all():
        render_dash()
        render_detail()
        page.update()

    # ── Detail panel layout ──────────────────────────────────────────────
    detail_header = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        gradient=grad(),
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_size=16, icon_color=c("TEXT_ON_PRIMARY"),
                    on_click=lambda e: go_home(),
                    tooltip="Back",
                ),
                ft.Text("Grades & Scholarship Dashboard", size=16,
                        weight="bold", color=c("TEXT_ON_PRIMARY"), expand=True),
            ],
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    add_module_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color=c("TEXT_ON_PRIMARY"), size=16),
             ft.Text("Add New Module", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600")],
            spacing=6, tight=True,
        ),
        on_click=open_add_dialog, ink=True, border_radius=10,
        padding=ft.padding.symmetric(horizontal=18, vertical=11),
        gradient=grad(), alignment=ft.Alignment(0, 0),
    )

    avg_card = ft.Container(
        expand=True, border_radius=14,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, c("BORDER")),
        padding=ft.padding.symmetric(horizontal=18, vertical=14),
        content=ft.Row(
            [
                ft.Container(
                    width=46, height=46, border_radius=23,
                    border=ft.border.all(3, c("PRIMARY")),
                    content=ft.Icon(ft.Icons.SCHOOL_OUTLINED, size=22, color=c("PRIMARY")),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(width=12),
                ft.Column(
                    [ft.Text("Current Sem. Average", size=11,
                              color=c("TEXT_SECONDARY"), weight="w500"),
                     det_avg_text],
                    spacing=2,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    ects_card = ft.Container(
        expand=True, border_radius=14,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, c("BORDER")),
        padding=ft.padding.symmetric(horizontal=18, vertical=14),
        content=ft.Row(
            [
                ft.Container(
                    width=46, height=46, border_radius=23,
                    border=ft.border.all(3, c("PRIMARY")),
                    content=ft.Icon(ft.Icons.LAYERS_OUTLINED, size=22, color=c("PRIMARY")),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(width=12),
                ft.Column(
                    [ft.Text("Total Credits", size=11,
                              color=c("TEXT_SECONDARY"), weight="w500"),
                     det_ects_text],
                    spacing=2,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    schol_card = ft.Container(
        width=220, border_radius=14,
        bgcolor=ft.Colors.with_opacity(0.08, "#22c55e"),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, "#22c55e")),
        padding=ft.padding.symmetric(horizontal=18, vertical=14),
        content=ft.Column(
            [
                ft.Text("Scholarship Eligibility", size=11,
                         weight="w600", color=c("TEXT_PRIMARY")),
                ft.Container(height=4),
                ft.Row([det_schol_icon, det_schol_text], spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=0,
        ),
    )

    detail_panel = ft.Stack(
        [
            ft.Container(
                expand=True,
                border=ft.border.all(1, c("BORDER")),
                border_radius=RADIUS_LG,
                bgcolor=ft.Colors.WHITE,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column(
                    [
                        detail_header,
                        ft.Container(
                            expand=True,
                            padding=ft.padding.all(20),
                            content=ft.Column(
                                [
                                    ft.Row([add_module_btn],
                                           alignment=ft.MainAxisAlignment.START),
                                    ft.Container(height=16),
                                    ft.Row([avg_card, ects_card, schol_card], spacing=12),
                                    ft.Container(height=20),
                                    ft.Container(
                                        expand=True,
                                        border_radius=12,
                                        border=ft.border.all(1, c("BORDER")),
                                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                        content=ft.Column(
                                            [det_table_col],
                                            scroll=ft.ScrollMode.AUTO,
                                            expand=True,
                                        ),
                                    ),
                                ],
                                spacing=0, expand=True,
                            ),
                        ),
                    ],
                    spacing=0, expand=True,
                ),
            ),
            dialog_overlay,
        ],
        expand=True,
    )

    # ── navigation ───────────────────────────────────────────────────────
    def go_home():
        if home_panel_ref[0] is not None:
            main_panel.content = home_panel_ref[0]
            main_panel.update()

    def set_home_panel(panel):
        home_panel_ref[0] = panel

    def open_detail():
        render_detail()
        main_panel.content = detail_panel
        main_panel.update()

    # ── COMPACT WIDGET ───────────────────────────────────────────────────
    compact_widget = ft.Container(
        expand=True,
        border_radius=RADIUS_LG,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(2, c("BORDER")),
        padding=ft.padding.all(14),
        on_click=lambda e: open_detail(),
        ink=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL_OUTLINED, size=14, color=c("TEXT_SECONDARY")),
                        ft.Text("Grade Calculator", size=13, weight="bold",
                                color=c("TEXT_PRIMARY"), expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=12, color=c("TEXT_SECONDARY")),
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [dash_rows_col],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True, spacing=0,
                    ),
                ),
                ft.Container(height=8),
                ft.Divider(height=1, color=c("BORDER")),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("CURRENT AVERAGE GRADE", size=8,
                                        color=c("TEXT_SECONDARY"), weight="w600"),
                                ft.Container(height=2),
                                dash_avg_text,
                                ft.Container(height=2),
                                dash_ects_text,
                            ],
                            spacing=0, expand=True,
                        ),
                        goal_ring_slot,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0, expand=True,
        ),
    )

    # ── theme refresh ────────────────────────────────────────────────────
    def refresh_grade_theme():
        compact_widget.border  = ft.border.all(2, c("BORDER"))
        compact_widget.bgcolor = ft.Colors.WHITE
        dash_avg_text.color    = c("TEXT_PRIMARY")
        dash_ects_text.color   = c("TEXT_SECONDARY")
        det_avg_text.color     = c("TEXT_PRIMARY")
        det_ects_text.color    = c("TEXT_PRIMARY")
        detail_header.gradient  = grad()
        add_module_btn.gradient = grad()
        avg_card.border  = ft.border.all(1, c("BORDER"))
        ects_card.border = ft.border.all(1, c("BORDER"))
        for field in [new_name_field, new_ects_field]:
            field.bgcolor              = c("SURFACE")
            field.border_color         = c("BORDER")
            field.focused_border_color = c("PRIMARY")
            field.text_style           = ft.TextStyle(color=c("TEXT_PRIMARY"))
            field.label_style          = ft.TextStyle(color=c("TEXT_SECONDARY"))
        render_dash()
        render_detail()

    # Initial render
    render_dash()
    render_detail()

    return compact_widget, detail_panel, refresh_grade_theme, set_home_panel