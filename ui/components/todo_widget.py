import flet as ft
import ui.themes.themes as th
from datetime import datetime, timedelta

RADIUS_LG = 20


def build_todo(page: ft.Page, c, grad, main_panel: ft.Container, user_email: str = ""):
    home_panel_ref = [None]
    dashboard_widget_ref = [None]

    def set_home_panel(home):
        home_panel_ref[0] = home

    def set_dashboard_widget(widget_fn):
        dashboard_widget_ref[0] = widget_fn

    tasks = [
        {"id": 1, "title": "Finish weekly report", "type": "Assignment", "due_date": "2026-04-10", "completed": True, "completed_at": "2026-04-08"},
        {"id": 2, "title": "Exam preparation", "type": "Exam", "due_date": "2026-04-15", "completed": False, "completed_at": None},
        {"id": 3, "title": "Team meeting", "type": "Appointment", "due_date": "2026-04-05", "completed": True, "completed_at": "2026-04-05"},
        {"id": 4, "title": "Read chapter 4", "type": "Other", "due_date": "2026-04-12", "completed": True, "completed_at": "2026-04-10"},
    ]

    WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_month = [datetime.now().replace(day=1)]

    filter_types = {
        "All": {"color": c("BORDER"), "display_name": "All"},
        "Completed": {"color": "#4CAF50", "display_name": "Completed"},
        "Assignment": {"color": "#2196F3", "display_name": "Assignment"},
        "Appointment": {"color": "#E91E63", "display_name": "Appointment"},
        "Exam": {"color": "#9C27B0", "display_name": "Exam"},
        "Other": {"color": "#BDBDBD", "display_name": "Other"},
    }
    type_colors = {"assignment": "#2196F3", "appointment": "#E91E63", "exam": "#9C27B0", "other": "#BDBDBD"}
    selected_filter = ["All"]

    def get_type_color(task_type: str):
        return type_colors.get((task_type or "").strip().lower(), c("BORDER"))

    def build_type_option(task_type: str):
        return ft.dropdown.Option(key=task_type, text=task_type,
            leading_icon=ft.Icon(ft.Icons.CIRCLE, color=get_type_color(task_type), size=10))

    def auto_complete_overdue():
        today = datetime.now().date()
        changed = False
        for task in tasks:
            if not task["completed"]:
                try:
                    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    if due < today:
                        task["completed"] = True
                        task["completed_at"] = today.strftime("%Y-%m-%d")
                        changed = True
                except ValueError:
                    pass
        return changed

    def get_upcoming_tasks():
        auto_complete_overdue()
        today = datetime.now().date()
        upcoming = []
        for task in tasks:
            if not task["completed"]:
                try:
                    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    upcoming.append((due, task))
                except ValueError:
                    upcoming.append((today, task))
        upcoming.sort(key=lambda x: x[0])
        return [t for _, t in upcoming]

    def toggle_task_done(task_id: int):
        today = datetime.now().date()
        for task in tasks:
            if task["id"] == task_id and not task["completed"]:
                task["completed"] = True
                task["completed_at"] = today.strftime("%Y-%m-%d")
                break
        refresh_filter_ui()
        refresh_tasks_list()
        refresh_statistics_ui()
        if dashboard_widget_ref[0]:
            dashboard_widget_ref[0]()
        page.update()

    tasks_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    dialog_title = ft.Text("", size=16, weight="bold", color=c("TEXT_PRIMARY"))
    title_field = ft.TextField(label="Task title", bgcolor=c("SURFACE"), border_color=c("BORDER"), focused_border_color=c("PRIMARY"))
    type_field = ft.Dropdown(
        label="Type", value="Assignment", width=420,
        options=[build_type_option(t) for t in ["Assignment", "Appointment", "Exam", "Other"]],
        bgcolor=c("SURFACE"), border_color=c("BORDER"), focused_border_color=c("PRIMARY"),
    )

    def refresh_type_field_icon():
        type_field.leading_icon = ft.Icon(ft.Icons.CIRCLE, color=get_type_color(type_field.value), size=10)

    def on_type_select(e):
        refresh_type_field_icon()
        page.update()

    type_field.on_select = on_type_select
    refresh_type_field_icon()

    due_date_field = ft.TextField(
        label="Due date (YYYY-MM-DD)", expand=True, read_only=True,
        bgcolor=c("SURFACE"), border_color=c("BORDER"), focused_border_color=c("PRIMARY"),
    )

    # ── DatePicker: fix timezone off-by-one ──────────────────────────
    # Flet DatePicker grąžina datetime su tzinfo=UTC.
    # Lietuva (UTC+3 vasarą) → pvz. "2026-04-15 00:00 UTC" = "2026-04-14 21:00 local"
    # .replace(tzinfo=None) pašalina timezone prieš skaitant year/month/day,
    # todėl visada gaunama ta pati diena kurią vartotojas pasirinko ekrane.
    date_picker = ft.DatePicker(
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2100, 12, 31),
    )

    def on_date_change(e):
        if e.control.value:
            v = e.control.value.replace(tzinfo=None)
            due_date_field.value = f"{v.year:04d}-{v.month:02d}-{v.day:02d}"
            page.update()

    date_picker.on_change = on_date_change

    def open_date_picker(e):
        ensure_overlay(date_picker)
        date_picker.open = True
        page.update()

    date_picker_btn = ft.Container(
        content=ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=c("TEXT_ON_PRIMARY")),
        on_click=open_date_picker, ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=12),
        gradient=grad(), tooltip="Pick date",
    )
    form_error_text = ft.Text("", size=12, color=th.ERROR, visible=False)

    task_form_dialog = ft.AlertDialog(
        modal=True, bgcolor=c("SURFACE"), title=dialog_title,
        content=ft.Container(width=380, content=ft.Column(
            [title_field, ft.Container(height=8), type_field, ft.Container(height=8),
             ft.Row([due_date_field, date_picker_btn], spacing=8), ft.Container(height=8), form_error_text],
            spacing=0, tight=True,
        )),
    )

    delete_title = ft.Text("Delete task", size=16, weight="bold", color=c("TEXT_PRIMARY"))
    delete_text = ft.Text("", size=13, color=c("TEXT_PRIMARY"))
    delete_dialog = ft.AlertDialog(modal=True, bgcolor=c("SURFACE"), title=delete_title, content=delete_text)

    def ensure_overlay(dialog):
        if dialog not in page.overlay:
            page.overlay.append(dialog)

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def parse_date(date_value):
        if not date_value:
            return None
        try:
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        except ValueError:
            return None

    def same_month(date_obj, month_anchor):
        return date_obj and date_obj.year == month_anchor.year and date_obj.month == month_anchor.month

    def shift_selected_month(delta: int):
        anchor = selected_month[0]
        month = anchor.month + delta
        year = anchor.year
        if month < 1:
            month = 12; year -= 1
        elif month > 12:
            month = 1; year += 1
        selected_month[0] = anchor.replace(year=year, month=month, day=1)
        refresh_statistics_ui()
        page.update()

    def compute_monthly_stats():
        anchor = selected_month[0]
        today = datetime.now().date()
        month_tasks = [(task, parse_date(task.get("due_date"))) for task in tasks
                       if same_month(parse_date(task.get("due_date")), anchor)]
        total = len(month_tasks)
        completed = len([1 for t, _ in month_tasks if t.get("completed")])
        progress = (completed / total) if total else 0.0
        overdue = len([1 for t, d in month_tasks if d and not t.get("completed") and d < today])
        upcoming = len([1 for t, d in month_tasks if d and not t.get("completed") and d >= today])
        weekday_counts = [0] * 7
        completed_days = set()
        for task in tasks:
            completed_at = parse_date(task.get("completed_at"))
            if task.get("completed") and completed_at:
                completed_days.add(completed_at)
            if task.get("completed") and same_month(completed_at, anchor):
                weekday_counts[completed_at.weekday()] += 1
        max_count = max(weekday_counts) if weekday_counts else 0
        if max_count > 0:
            best_idx = weekday_counts.index(max_count)
            most_productive = f"Most productive day: {WEEKDAY_LABELS[best_idx]} ({max_count} tasks)"
        else:
            most_productive = "Most productive day: No completed tasks this month"
        streak = 0
        cursor = today
        while cursor in completed_days:
            streak += 1; cursor -= timedelta(days=1)
        return {"total": total, "completed": completed, "progress": progress, "overdue": overdue,
                "upcoming": upcoming, "weekday_counts": weekday_counts, "most_productive": most_productive, "streak": streak}

    def make_stat_card(label, value_control):
        return ft.Container(expand=True, bgcolor=c("SURFACE"), border=ft.border.all(1, c("BORDER")),
            border_radius=12, padding=ft.padding.all(10),
            content=ft.Column([ft.Text(label, size=11, color=c("TEXT_SECONDARY")), value_control], spacing=4, tight=True))

    month_label = ft.Text("", size=14, weight="bold", color=c("TEXT_PRIMARY"))
    completion_bar = ft.ProgressBar(value=0.0, height=12, color=c("PRIMARY"), bgcolor=ft.Colors.with_opacity(0.14, c("PRIMARY")))
    completion_percent_text = ft.Text("0%", size=30, weight="bold", color=c("TEXT_PRIMARY"))
    completion_done_text = ft.Text("Completed", size=16, weight="w600", color=c("TEXT_PRIMARY"))
    completion_ratio_text = ft.Text("0 of 0 tasks", size=12, color=c("TEXT_SECONDARY"))
    completion_bubble_text = ft.Text("", size=11, weight="w600", color=c("TEXT_ON_PRIMARY"))
    completion_bubble = ft.Container(visible=False, border_radius=999,
        padding=ft.padding.symmetric(horizontal=10, vertical=5), bgcolor=c("SECONDARY"), content=completion_bubble_text)
    overdue_value = ft.Text("0", size=20, weight="bold", color=th.ERROR)
    upcoming_value = ft.Text("0", size=20, weight="bold", color=c("TEXT_PRIMARY"))
    streak_value = ft.Text("0 days", size=20, weight="bold", color=c("TEXT_PRIMARY"))
    most_productive_text = ft.Text("", size=12, color=c("TEXT_PRIMARY"), weight="w500")
    chart_bars_row = ft.Row(spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def milestone_message(progress):
        p = int(round(progress * 100))
        if p >= 100: return "Amazing work! You completed everything!"
        if p >= 75: return "Keep going, you're almost there!"
        if p >= 50: return "You're halfway there!"
        if p >= 25: return "Good start!"
        return ""

    def refresh_statistics_ui():
        stats = compute_monthly_stats()
        month_label.value = selected_month[0].strftime("%B %Y")
        overdue_value.value = str(stats["overdue"])
        upcoming_value.value = str(stats["upcoming"])
        streak_value.value = f"{stats['streak']} days"
        completion_bar.value = stats["progress"]
        completion_bar.color = c("PRIMARY")
        completion_bar.bgcolor = ft.Colors.with_opacity(0.14, c("PRIMARY"))
        completion_percent_text.value = f"{round(stats['progress'] * 100)}%"
        completion_ratio_text.value = f"{stats['completed']} of {stats['total']} tasks"
        completion_bubble.bgcolor = c("SECONDARY")
        bubble_message = milestone_message(stats["progress"])
        completion_bubble.visible = bool(bubble_message)
        completion_bubble_text.value = bubble_message
        max_count = max(stats["weekday_counts"]) if stats["weekday_counts"] else 0
        bars = []
        for idx, count in enumerate(stats["weekday_counts"]):
            height = 10 if count == 0 else int(10 + (count / max_count) * 62)
            bar_color = c("SECONDARY") if count == max_count and max_count > 0 else c("PRIMARY")
            bars.append(ft.Column([
                ft.Text(str(count), size=10, color=c("TEXT_SECONDARY"), text_align=ft.TextAlign.CENTER),
                ft.Container(width=24, height=height, border_radius=6, bgcolor=bar_color, border=ft.border.all(1, c("BORDER"))),
                ft.Text(WEEKDAY_LABELS[idx], size=10, color=c("TEXT_SECONDARY")),
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.END))
        chart_bars_row.controls = bars
        most_productive_text.value = stats["most_productive"]

    def open_task_form(mode: str, task_id: int = None):
        form_error_text.visible = False
        form_error_text.value = ""
        if mode == "add":
            dialog_title.value = "Add new task"
            title_field.value = ""
            type_field.value = "Assignment"
            refresh_type_field_icon()
            due_date_field.value = datetime.now().strftime("%Y-%m-%d")
            confirm_label = "Add"
        else:
            task = next((t for t in tasks if t["id"] == task_id), None)
            if not task: return
            dialog_title.value = "Edit task"
            title_field.value = task["title"]
            type_field.value = task["type"] if task["type"] in ["Assignment", "Appointment", "Exam", "Other"] else "Other"
            refresh_type_field_icon()
            due_date_field.value = task["due_date"]
            confirm_label = "Save"

        def on_confirm(e):
            title_value = (title_field.value or "").strip()
            type_value = (type_field.value or "Assignment")
            due_value = (due_date_field.value or "").strip()
            if not title_value:
                form_error_text.value = "Task title is required"; form_error_text.visible = True; page.update(); return
            try:
                datetime.strptime(due_value, "%Y-%m-%d")
            except ValueError:
                form_error_text.value = "Date format must be YYYY-MM-DD"; form_error_text.visible = True; page.update(); return
            if mode == "add":
                new_id = max([t["id"] for t in tasks], default=0) + 1
                tasks.append({"id": new_id, "title": title_value, "type": type_value, "due_date": due_value, "completed": False, "completed_at": None})
            else:
                for task in tasks:
                    if task["id"] == task_id:
                        task["title"] = title_value; task["type"] = type_value; task["due_date"] = due_value; break
            close_dialog(task_form_dialog)
            refresh_filter_ui(); refresh_tasks_list(); refresh_statistics_ui()
            if dashboard_widget_ref[0]: dashboard_widget_ref[0]()
            page.update()

        task_form_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(task_form_dialog), style=ft.ButtonStyle(color=c("TEXT_SECONDARY"))),
            ft.Container(content=ft.Text(confirm_label, size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
                on_click=on_confirm, ink=True, border_radius=8, padding=ft.padding.symmetric(horizontal=20, vertical=8), gradient=grad()),
        ]
        task_form_dialog.actions_alignment = ft.MainAxisAlignment.END
        ensure_overlay(task_form_dialog)
        task_form_dialog.open = True
        page.update()

    def get_days_label_style(due_date: str):
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            delta = (due - today).days
            if delta < 0: return f"{abs(delta)}d overdue", c("TEXT_SECONDARY"), "w400"
            if delta == 0: return "Today", th.ERROR, "bold"
            if delta == 1: return "Tomorrow", c("PRIMARY"), "bold"
            return f"{delta}d left", c("TEXT_SECONDARY"), "w400"
        except ValueError:
            return "No date", c("TEXT_SECONDARY"), "w400"

    def _sort_key(task):
        try:
            return datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return datetime.max.date()

    def refresh_tasks_list():
        rows = []
        current_filter = selected_filter[0]
        filtered_tasks = []
        for task in tasks:
            if current_filter == "All":
                # "All" rodo TIK neatliktas
                if not task["completed"]: filtered_tasks.append(task)
            elif current_filter == "Completed":
                if task["completed"]: filtered_tasks.append(task)
            else:
                if not task["completed"] and task["type"] == current_filter: filtered_tasks.append(task)

        # Rikiuojame: artimiausia data viršuje
        filtered_tasks.sort(key=_sort_key)

        for task in filtered_tasks:
            days_text, days_color, days_weight = get_days_label_style(task["due_date"])
            is_done = task["completed"]
            checkbox = ft.Container(
                width=22, height=22, border_radius=11,
                border=ft.border.all(2, c("PRIMARY") if is_done else c("BORDER")),
                bgcolor=c("PRIMARY") if is_done else ft.Colors.TRANSPARENT,
                content=ft.Container(width=8, height=8, border_radius=4, bgcolor=c("TEXT_ON_PRIMARY"),
                    visible=is_done, alignment=ft.Alignment(0, 0)),
                alignment=ft.Alignment(0, 0),
                animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
                tooltip="Mark as done" if not is_done else "Completed",
                **({"on_click": lambda e, tid=task["id"]: toggle_task_done(tid), "ink": True} if not is_done else {}),
            )
            task_row = ft.Container(
                border=ft.border.all(1, c("BORDER")), border_radius=12, bgcolor=th.TEXT_ON_PRIMARY,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=ft.Row([
                    checkbox,
                    ft.Column([
                        ft.Text(task["title"], expand=True, style=ft.TextStyle(
                            color=c("TEXT_SECONDARY") if is_done else c("TEXT_PRIMARY"),
                            decoration=ft.TextDecoration.LINE_THROUGH if is_done else None, weight="w500")),
                        ft.Row([
                            ft.Container(width=8, height=8, border_radius=4, bgcolor=get_type_color(task["type"])),
                            ft.Text(task["type"], size=11, color=c("TEXT_SECONDARY")),
                            ft.Text("•", size=11, color=c("TEXT_SECONDARY")),
                            ft.Text(days_text, size=11,
                                color=days_color if not is_done else c("TEXT_SECONDARY"),
                                weight=days_weight if not is_done else "w400"),
                        ], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=4, expand=True),
                    ft.Row([
                        ft.Container(content=ft.Icon(ft.Icons.EDIT, size=16, color=c("PRIMARY")),
                            on_click=lambda e, tid=task["id"]: edit_task(tid), ink=True, border_radius=6, padding=4, tooltip="Edit"),
                        ft.Container(content=ft.Icon(ft.Icons.DELETE, size=16, color=th.ERROR),
                            on_click=lambda e, tid=task["id"]: delete_task_confirm(tid), ink=True, border_radius=6, padding=4, tooltip="Delete"),
                    ], spacing=4),
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            rows.append(task_row)
        tasks_list_column.controls = rows

    def edit_task(task_id: int):
        open_task_form("edit", task_id)

    def delete_task_confirm(task_id: int):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task: return
        delete_text.value = f"Are you sure you want to delete '{task['title']}'?"
        delete_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(delete_dialog), style=ft.ButtonStyle(color=c("TEXT_SECONDARY"))),
            ft.Container(content=ft.Text("Delete", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
                on_click=lambda e: confirm_delete(task_id), ink=True, border_radius=8,
                padding=ft.padding.symmetric(horizontal=20, vertical=8), bgcolor=th.ERROR),
        ]
        delete_dialog.actions_alignment = ft.MainAxisAlignment.END
        ensure_overlay(delete_dialog)
        delete_dialog.open = True
        page.update()

    def confirm_delete(task_id: int):
        nonlocal tasks
        tasks = [task for task in tasks if task["id"] != task_id]
        close_dialog(delete_dialog)
        refresh_filter_ui(); refresh_tasks_list(); refresh_statistics_ui()
        if dashboard_widget_ref[0]: dashboard_widget_ref[0]()
        page.update()

    def add_new_task(e=None):
        open_task_form("add")

    def get_filter_count(filter_type: str):
        if filter_type == "All": return len([t for t in tasks if not t["completed"]])
        elif filter_type == "Completed": return len([t for t in tasks if t["completed"]])
        else: return len([t for t in tasks if not t["completed"] and t["type"] == filter_type])

    def select_filter(filter_type: str):
        selected_filter[0] = filter_type
        refresh_filter_ui(); refresh_tasks_list(); page.update()

    def build_filter_tab(filter_type: str):
        is_selected = selected_filter[0] == filter_type
        count = get_filter_count(filter_type)
        color = filter_types[filter_type]["color"]
        return ft.Container(
            content=ft.Text(f"{filter_type} ({count})", size=12, color=ft.Colors.WHITE if is_selected else color, weight="w600"),
            bgcolor=color if is_selected else ft.Colors.TRANSPARENT,
            border=ft.border.all(2, color), border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            on_click=lambda e: select_filter(filter_type), ink=True,
        )

    def refresh_filter_ui():
        filter_tabs = [build_filter_tab(ft_type) for ft_type in filter_types.keys()]
        filter_tabs.append(ft.Container(
            content=ft.Icon(ft.Icons.ADD, size=18, color=c("TEXT_ON_PRIMARY")),
            bgcolor=c("PRIMARY"), border_radius=8, padding=ft.padding.all(6),
            on_click=add_new_task, ink=True, tooltip="Add new task",
        ))
        todo_filter_area.content = ft.Row(filter_tabs, spacing=8, wrap=True, scroll=ft.ScrollMode.AUTO)

    todo_tasks_panel = ft.Container(
        expand=True, bgcolor=th.TEXT_ON_PRIMARY, border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")), padding=ft.padding.all(16),
        content=ft.Column([
            ft.Row([
                ft.Text("Tasks", size=14, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.ADD, size=16, color=c("TEXT_ON_PRIMARY")),
                                    ft.Text("Add new task", size=12, color=c("TEXT_ON_PRIMARY"), weight="w600")], spacing=4),
                    on_click=add_new_task, ink=True, border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=6), tooltip="Add new task", gradient=grad()),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=8),
            tasks_list_column,
        ], spacing=0, expand=True),
    )

    todo_stats_panel = ft.Container(
        expand=True, bgcolor=th.TEXT_ON_PRIMARY, border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")), padding=ft.padding.all(16),
        content=ft.Column([
            ft.Row([
                ft.Text("Monthly statistics", size=14, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Container(expand=True),
                ft.Container(content=ft.Icon(ft.Icons.CHEVRON_LEFT, size=16, color=c("TEXT_PRIMARY")),
                    padding=ft.padding.all(4), border_radius=8, on_click=lambda e: shift_selected_month(-1), ink=True),
                month_label,
                ft.Container(content=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=c("TEXT_PRIMARY")),
                    padding=ft.padding.all(4), border_radius=8, on_click=lambda e: shift_selected_month(1), ink=True),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=8),
            ft.Container(border=ft.border.all(1, c("BORDER")), border_radius=12, bgcolor=c("SURFACE"), padding=ft.padding.all(12),
                content=ft.Column([
                    ft.Row([ft.Text("Completed tasks", size=12, weight="w600", color=c("TEXT_PRIMARY")),
                            ft.Container(expand=True), ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color=th.SUCCESS)]),
                    ft.Container(height=6), completion_bar, ft.Container(height=8), completion_bubble, ft.Container(height=8),
                    ft.Column([completion_percent_text, completion_done_text, completion_ratio_text],
                              spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
            ft.Container(height=10),
            ft.Row([make_stat_card("Overdue", overdue_value), make_stat_card("Upcoming deadlines", upcoming_value), make_stat_card("Streak", streak_value)], spacing=10),
            ft.Container(height=10),
            ft.Container(border=ft.border.all(1, c("BORDER")), border_radius=12, bgcolor=c("SURFACE"), padding=ft.padding.all(10),
                content=ft.Column([
                    ft.Text("Productivity by weekday", size=12, weight="w600", color=c("TEXT_PRIMARY")),
                    ft.Container(height=4), ft.Container(content=chart_bars_row, height=110),
                    ft.Container(height=4), most_productive_text,
                ], spacing=0)),
        ], spacing=0, expand=True),
    )

    todo_filter_area = ft.Container(
        height=60, bgcolor=th.TEXT_ON_PRIMARY, border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")), padding=ft.padding.all(12),
    )

    refresh_tasks_list()
    refresh_filter_ui()
    refresh_statistics_ui()

    todo_back_btn = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.ARROW_BACK, size=14, color=c("TEXT_ON_PRIMARY")),
                        ft.Text("Back", size=12, color=c("TEXT_ON_PRIMARY"), weight="w600")], spacing=4),
        on_click=lambda e: (setattr(main_panel, "content", home_panel_ref[0]), main_panel.update()),
        ink=True, border_radius=8, padding=ft.padding.symmetric(horizontal=12, vertical=8), gradient=grad(),
    )

    todo_detail_panel = ft.Container(
        expand=True, bgcolor=th.TEXT_ON_PRIMARY, border_radius=RADIUS_LG, padding=ft.padding.all(24),
        content=ft.Column([
            ft.Row([ft.Text("To-Do List", size=20, weight="bold", color=c("TEXT_PRIMARY")),
                    ft.Container(expand=True), todo_back_btn], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=16), todo_filter_area, ft.Container(height=16),
            ft.Row([todo_tasks_panel, todo_stats_panel], spacing=16, expand=True),
        ], spacing=0, expand=True),
    )

    def get_todo_refs():
        return {"todo_detail_panel": todo_detail_panel, "todo_tasks_panel": todo_tasks_panel,
                "todo_stats_panel": todo_stats_panel, "todo_filter_area": todo_filter_area, "todo_back_btn": todo_back_btn}

    def refresh_todo_theme():
        refs = get_todo_refs()
        refs["todo_detail_panel"].bgcolor = th.TEXT_ON_PRIMARY
        refs["todo_tasks_panel"].border = ft.border.all(2, c("BORDER"))
        refs["todo_tasks_panel"].bgcolor = th.TEXT_ON_PRIMARY
        refs["todo_stats_panel"].border = ft.border.all(2, c("BORDER"))
        refs["todo_stats_panel"].bgcolor = th.TEXT_ON_PRIMARY
        refs["todo_filter_area"].border = ft.border.all(2, c("BORDER"))
        refs["todo_filter_area"].bgcolor = th.TEXT_ON_PRIMARY
        refs["todo_back_btn"].gradient = grad()
        refresh_tasks_list()
        refresh_statistics_ui()

    return (todo_detail_panel, get_todo_refs, refresh_todo_theme, set_home_panel,
            get_upcoming_tasks, toggle_task_done, set_dashboard_widget)