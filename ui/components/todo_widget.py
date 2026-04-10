import flet as ft
import ui.themes.themes as th
from datetime import datetime, timedelta

RADIUS_LG = 20


def build_todo(page: ft.Page, c, grad, main_panel: ft.Container, user_email: str = ""):
    """
    Sukuria To-Do list widgetą.

    Grąžina:
        todo_detail_panel — widget rodomas paspaudus To-Do kvadratą
        get_todo_refs() — funkcija grąžinanti dict su visais theme-priklausomais ref'ais
        refresh_todo_theme() — funkcija atnaujinanti To-Do panelių temą
        set_home_panel() — funkcija nustatanti home_panel referenciją grįžimui
    """

    home_panel_ref = [None]  

    def set_home_panel(home):
        """Nustato home_panel referencą"""
        home_panel_ref[0] = home

    tasks = [
        {
            "id": 1,
            "title": "Finish weekly report",
            "type": "Assignment",
            "due_date": "2026-04-10",
            "completed": True,
            "completed_at": "2026-04-08",
        },
        {
            "id": 2,
            "title": "Exam preparation",
            "type": "Exam",
            "due_date": "2026-04-15",
            "completed": False,
            "completed_at": None,
        },
        {
            "id": 3,
            "title": "Team meeting",
            "type": "Appointment",
            "due_date": "2026-04-05",
            "completed": True,
            "completed_at": "2026-04-05",
        },
        {
            "id": 4,
            "title": "Read chapter 4",
            "type": "Other",
            "due_date": "2026-04-12",
            "completed": True,
            "completed_at": "2026-04-10",
        },
    ]

    WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_month = [datetime.now().replace(day=1)]

    # Filter state - track which filter type is selected
    filter_types = {
        "All": {"color": c("BORDER"), "display_name": "All"},
        "Completed": {"color": "#4CAF50", "display_name": "Completed"},
        "Assignment": {"color": "#2196F3", "display_name": "Assignment"},
        "Appointment": {"color": "#E91E63", "display_name": "Appointment"},
        "Exam": {"color": "#9C27B0", "display_name": "Exam"},
        "Other": {"color": "#BDBDBD", "display_name": "Other"},
    }
    
    selected_filter = ["All"]  # Use list to allow modification in nested functions

    tasks_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    dialog_title = ft.Text("", size=16, weight="bold", color=c("TEXT_PRIMARY"))
    title_field = ft.TextField(
        label="Task title",
        bgcolor=c("SURFACE"),
        border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    type_field = ft.TextField(
        label="Type",
        value="Assignment",
        bgcolor=c("SURFACE"),
        border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    due_date_field = ft.TextField(
        label="Due date (YYYY-MM-DD)",
        expand=True,
        read_only=True,
        bgcolor=c("SURFACE"),
        border_color=c("BORDER"),
        focused_border_color=c("PRIMARY"),
    )
    date_picker = ft.DatePicker()

    def on_date_change(e):
        if e.control.value:
            due_date_field.value = e.control.value.strftime("%Y-%m-%d")
            page.update()

    date_picker.on_change = on_date_change

    def open_date_picker(e):
        ensure_overlay(date_picker)
        date_picker.open = True
        page.update()

    date_picker_btn = ft.Container(
        content=ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=c("TEXT_ON_PRIMARY")),
        on_click=open_date_picker,
        ink=True,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=12),
        gradient=grad(),
        tooltip="Pick date",
    )
    form_error_text = ft.Text("", size=12, color=th.ERROR, visible=False)

    task_form_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=c("SURFACE"),
        title=dialog_title,
        content=ft.Container(
            width=380,
            content=ft.Column(
                [
                    title_field,
                    ft.Container(height=8),
                    type_field,
                    ft.Container(height=8),
                    ft.Row([due_date_field, date_picker_btn], spacing=8),
                    ft.Container(height=8),
                    form_error_text,
                ],
                spacing=0,
                tight=True,
            ),
        ),
    )

    delete_title = ft.Text("Delete task", size=16, weight="bold", color=c("TEXT_PRIMARY"))
    delete_text = ft.Text("", size=13, color=c("TEXT_PRIMARY"))
    delete_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=c("SURFACE"),
        title=delete_title,
        content=delete_text,
    )

    def ensure_overlay(dialog: ft.AlertDialog):
        if dialog not in page.overlay:
            page.overlay.append(dialog)

    def close_dialog(dialog: ft.AlertDialog):
        dialog.open = False
        page.update()

    def parse_days_left(due_date: str):
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            days_left = (due - today).days
            if days_left < 0:
                return f"{abs(days_left)}d overdue"
            if days_left == 0:
                return "Today"
            if days_left == 1:
                return "Tomorrow"
            return f"{days_left}d left"
        except ValueError:
            return "No date"

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
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        selected_month[0] = anchor.replace(year=year, month=month, day=1)
        refresh_statistics_ui()
        page.update()

    def compute_current_streak():
        completed_days = set()
        for task in tasks:
            completed_date = parse_date(task.get("completed_at"))
            if task.get("completed") and completed_date:
                completed_days.add(completed_date)

        if not completed_days:
            return 0

        streak = 0
        cursor = datetime.now().date()
        while cursor in completed_days:
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def compute_monthly_stats():
        anchor = selected_month[0]
        today = datetime.now().date()

        month_tasks = []
        for task in tasks:
            due = parse_date(task.get("due_date"))
            if same_month(due, anchor):
                month_tasks.append((task, due))

        total = len(month_tasks)
        completed = len([1 for task, _ in month_tasks if task.get("completed")])
        progress = (completed / total) if total else 0.0

        overdue = len(
            [
                1
                for task, due in month_tasks
                if due and (not task.get("completed")) and due < today
            ]
        )

        upcoming = len(
            [
                1
                for task, due in month_tasks
                if due and (not task.get("completed")) and due >= today
            ]
        )

        weekday_counts = [0] * 7
        for task in tasks:
            completed_at = parse_date(task.get("completed_at"))
            if task.get("completed") and same_month(completed_at, anchor):
                weekday_counts[completed_at.weekday()] += 1

        max_count = max(weekday_counts) if weekday_counts else 0
        if max_count > 0:
            best_idx = weekday_counts.index(max_count)
            most_productive = f"Most productive day: {WEEKDAY_LABELS[best_idx]} ({max_count} tasks)"
        else:
            most_productive = "Most productive day: No completed tasks this month"

        return {
            "total": total,
            "completed": completed,
            "progress": progress,
            "overdue": overdue,
            "upcoming": upcoming,
            "weekday_counts": weekday_counts,
            "most_productive": most_productive,
            "streak": compute_current_streak(),
        }

    def make_stat_card(label: str, value_control: ft.Control):
        return ft.Container(
            expand=True,
            bgcolor=c("SURFACE"),
            border=ft.border.all(1, c("BORDER")),
            border_radius=12,
            padding=ft.padding.all(10),
            content=ft.Column(
                [
                    ft.Text(label, size=11, color=c("TEXT_SECONDARY")),
                    value_control,
                ],
                spacing=4,
                tight=True,
            ),
        )

    month_label = ft.Text("", size=14, weight="bold", color=c("TEXT_PRIMARY"))
    completion_bar = ft.ProgressBar(
        value=0.0,
        height=12,
        color=c("PRIMARY"),
        bgcolor=ft.Colors.with_opacity(0.14, c("PRIMARY")),
    )
    completion_percent_text = ft.Text("0%", size=30, weight="bold", color=c("TEXT_PRIMARY"))
    completion_done_text = ft.Text("Completed", size=16, weight="w600", color=c("TEXT_PRIMARY"))
    completion_ratio_text = ft.Text("0 of 0 tasks", size=12, color=c("TEXT_SECONDARY"))
    completion_bubble_text = ft.Text("", size=11, weight="w600", color=c("TEXT_ON_PRIMARY"))
    completion_bubble = ft.Container(
        visible=False,
        border_radius=999,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        bgcolor=c("SECONDARY"),
        content=completion_bubble_text,
    )
    overdue_value = ft.Text("0", size=20, weight="bold", color=th.ERROR)
    upcoming_value = ft.Text("0", size=20, weight="bold", color=c("TEXT_PRIMARY"))
    streak_value = ft.Text("0 days", size=20, weight="bold", color=c("TEXT_PRIMARY"))
    most_productive_text = ft.Text("", size=12, color=c("TEXT_PRIMARY"), weight="w500")
    chart_bars_row = ft.Row(spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def milestone_message(progress: float):
        progress_pct = int(round(progress * 100))
        if progress_pct >= 100:
            return "Amazing work! You completed everything!"
        if progress_pct >= 75:
            return "Keep going, you're almost there!"
        if progress_pct >= 50:
            return "You're halfway there!"
        if progress_pct >= 25:
            return "Good start!"
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
            bars.append(
                ft.Column(
                    [
                        ft.Text(str(count), size=10, color=c("TEXT_SECONDARY"), text_align=ft.TextAlign.CENTER),
                        ft.Container(
                            width=24,
                            height=height,
                            border_radius=6,
                            bgcolor=bar_color,
                            border=ft.border.all(1, c("BORDER")),
                        ),
                        ft.Text(WEEKDAY_LABELS[idx], size=10, color=c("TEXT_SECONDARY")),
                    ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                )
            )
        chart_bars_row.controls = bars

        most_productive_text.value = stats["most_productive"]

    def open_task_form(mode: str, task_id: int = None):
        form_error_text.visible = False
        form_error_text.value = ""

        if mode == "add":
            dialog_title.value = "Add new task"
            title_field.value = ""
            type_field.value = "Assignment"
            due_date_field.value = datetime.now().strftime("%Y-%m-%d")
            confirm_label = "Add"
        else:
            task = next((t for t in tasks if t["id"] == task_id), None)
            if not task:
                return
            dialog_title.value = "Edit task"
            title_field.value = task["title"]
            type_field.value = task["type"] if task["type"] and task["type"] != "type" else "Assignment"
            due_date_field.value = task["due_date"]
            confirm_label = "Save"

        def on_confirm(e):
            title_value = (title_field.value or "").strip()
            type_value = (type_field.value or "Assignment").strip() or "Assignment"
            due_value = (due_date_field.value or "").strip()

            if not title_value:
                form_error_text.value = "Task title is required"
                form_error_text.visible = True
                page.update()
                return

            try:
                datetime.strptime(due_value, "%Y-%m-%d")
            except ValueError:
                form_error_text.value = "Date format must be YYYY-MM-DD"
                form_error_text.visible = True
                page.update()
                return

            if mode == "add":
                new_id = max([t["id"] for t in tasks], default=0) + 1
                tasks.append(
                    {
                        "id": new_id,
                        "title": title_value,
                        "type": type_value,
                        "due_date": due_value,
                        "completed": False,
                        "completed_at": None,
                    }
                )
            else:
                for task in tasks:
                    if task["id"] == task_id:
                        task["title"] = title_value
                        task["type"] = type_value
                        task["due_date"] = due_value
                        break

            close_dialog(task_form_dialog)
            refresh_tasks_list()
            refresh_statistics_ui()
            page.update()

        task_form_dialog.actions = [
            ft.TextButton(
                "Cancel",
                on_click=lambda e: close_dialog(task_form_dialog),
                style=ft.ButtonStyle(color=c("TEXT_SECONDARY")),
            ),
            ft.Container(
                content=ft.Text(confirm_label, size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
                on_click=on_confirm,
                ink=True,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=20, vertical=8),
                gradient=grad(),
            ),
        ]
        task_form_dialog.actions_alignment = ft.MainAxisAlignment.END

        ensure_overlay(task_form_dialog)
        task_form_dialog.open = True
        page.update()

    def refresh_tasks_list():
        """Atnaujina užduočių sąrašą"""
        rows = []
        
        # Filter tasks based on selected filter
        filtered_tasks = []
        current_filter = selected_filter[0]
        
        for task in tasks:
            if current_filter == "All":
                filtered_tasks.append(task)
            elif current_filter == "Completed":
                if task["completed"]:
                    filtered_tasks.append(task)
            else:
                # For type-based filters (Assignment, Appointment, Exam, Other)
                if not task["completed"] and task["type"] == current_filter:
                    filtered_tasks.append(task)
        
        for task in filtered_tasks:
            days_text = parse_days_left(task["due_date"])

            # Circular checkbox (rutuliukas)
            checkbox = ft.Container(
                width=22,
                height=22,
                border_radius=11,
                border=ft.border.all(2, c("PRIMARY") if task["completed"] else c("BORDER")),
                bgcolor=c("PRIMARY") if task["completed"] else ft.Colors.TRANSPARENT,
                content=ft.Container(
                    width=8,
                    height=8,
                    border_radius=4,
                    bgcolor=c("TEXT_ON_PRIMARY"),
                    visible=task["completed"],
                    alignment=ft.Alignment(0, 0),
                ),
                alignment=ft.Alignment(0, 0),
                on_click=lambda e, tid=task["id"], current=task["completed"]: toggle_task(tid, not current),
                ink=True,
            )

            # Task item row
            task_row = ft.Container(
                border=ft.border.all(1, c("BORDER")),
                border_radius=12,
                bgcolor=th.TEXT_ON_PRIMARY,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=ft.Row(
                    [
                        checkbox,
                        # Title and details
                        ft.Column(
                            [
                                ft.Text(
                                    task["title"],
                                    expand=True,
                                    style=ft.TextStyle(
                                        color=c("TEXT_SECONDARY") if task["completed"] else c("TEXT_PRIMARY"),
                                        decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None,
                                        weight="w500",
                                    ),
                                ),
                                ft.Text(
                                    f"{task['type']} • {days_text}",
                                    size=11,
                                    color=c("TEXT_SECONDARY"),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        # Action buttons
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.Icons.EDIT, size=16, color=c("PRIMARY")),
                                    on_click=lambda e, tid=task["id"]: edit_task(tid),
                                    ink=True, border_radius=6, padding=4,
                                    tooltip="Edit",
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.DELETE, size=16, color=th.ERROR),
                                    on_click=lambda e, tid=task["id"]: delete_task_confirm(tid),
                                    ink=True, border_radius=6, padding=4,
                                    tooltip="Delete",
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
            rows.append(task_row)

        tasks_list_column.controls = rows

    def toggle_task(task_id: int, is_completed: bool):
        """Pažymi/Atžymi užduotį kaip atliktą"""
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = bool(is_completed)
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d") if is_completed else None
                break
        refresh_tasks_list()
        refresh_statistics_ui()
        page.update()

    def edit_task(task_id: int):
        open_task_form("edit", task_id)

    def delete_task_confirm(task_id: int):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return

        delete_text.value = f"Are you sure you want to delete '{task['title']}'?"
        delete_dialog.actions = [
            ft.TextButton(
                "Cancel",
                on_click=lambda e: close_dialog(delete_dialog),
                style=ft.ButtonStyle(color=c("TEXT_SECONDARY")),
            ),
            ft.Container(
                content=ft.Text("Delete", size=13, color=c("TEXT_ON_PRIMARY"), weight="w600"),
                on_click=lambda e: confirm_delete(task_id),
                ink=True,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=20, vertical=8),
                bgcolor=th.ERROR,
            ),
        ]
        delete_dialog.actions_alignment = ft.MainAxisAlignment.END

        ensure_overlay(delete_dialog)
        delete_dialog.open = True
        page.update()

    def confirm_delete(task_id: int):
        nonlocal tasks
        tasks = [task for task in tasks if task["id"] != task_id]
        close_dialog(delete_dialog)
        refresh_tasks_list()
        refresh_statistics_ui()
        page.update()

    def add_new_task(e=None):
        open_task_form("add")

    def get_filter_count(filter_type: str):
        """Grąžina task'ų skaičių tam filteriui"""
        if filter_type == "All":
            return len(tasks)
        elif filter_type == "Completed":
            return len([t for t in tasks if t["completed"]])
        else:
            return len([t for t in tasks if not t["completed"] and t["type"] == filter_type])

    def select_filter(filter_type: str):
        """Pasirenkamas filterį"""
        selected_filter[0] = filter_type
        refresh_filter_ui()
        refresh_tasks_list()
        page.update()

    def build_filter_tab(filter_type: str):
        """Sukuria filter tab'ą"""
        is_selected = selected_filter[0] == filter_type
        count = get_filter_count(filter_type)
        color = filter_types[filter_type]["color"]
        
        # Darker shade for selected state
        bg_color = color if is_selected else ft.Colors.TRANSPARENT
        text_color = ft.Colors.WHITE if is_selected else color
        border_color = color
        
        return ft.Container(
            content=ft.Text(
                f"{filter_type} ({count})",
                size=12,
                color=text_color,
                weight="w600"
            ),
            bgcolor=bg_color,
            border=ft.border.all(2, border_color),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            on_click=lambda e: select_filter(filter_type),
            ink=True,
        )

    def refresh_filter_ui():
        """Atnaujina filtro UI"""
        filter_tabs = []
        for filter_type in filter_types.keys():
            filter_tabs.append(build_filter_tab(filter_type))
        
        # Add new task button
        add_btn = ft.Container(
            content=ft.Icon(ft.Icons.ADD, size=18, color=c("TEXT_ON_PRIMARY")),
            bgcolor=c("PRIMARY"),
            border_radius=8,
            padding=ft.padding.all(6),
            on_click=add_new_task,
            ink=True,
            tooltip="Add new task",
        )
        
        filter_tabs.append(add_btn)
        
        todo_filter_area.content = ft.Row(
            filter_tabs,
            spacing=8,
            wrap=True,
            scroll=ft.ScrollMode.AUTO,
        )

    # Left panel: Tasks list
    todo_tasks_panel = ft.Container(
        expand=True,
        bgcolor=th.TEXT_ON_PRIMARY,
        border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")),
        padding=ft.padding.all(16),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Tasks", size=14, weight="bold", color=c("TEXT_PRIMARY")),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ADD, size=16, color=c("TEXT_ON_PRIMARY")),
                                    ft.Text("Add new task", size=12, color=c("TEXT_ON_PRIMARY"), weight="w600"),
                                ],
                                spacing=4,
                            ),
                            on_click=add_new_task,
                            ink=True, border_radius=8, padding=ft.padding.symmetric(horizontal=10, vertical=6),
                            tooltip="Add new task",
                            gradient=grad(),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                tasks_list_column,
            ],
            spacing=0,
            expand=True,
        ),
    )

    # Right panel: Statistics
    todo_stats_panel = ft.Container(
        expand=True,
        bgcolor=th.TEXT_ON_PRIMARY,
        border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")),
        padding=ft.padding.all(16),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Monthly statistics", size=14, weight="bold", color=c("TEXT_PRIMARY")),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CHEVRON_LEFT, size=16, color=c("TEXT_PRIMARY")),
                            padding=ft.padding.all(4),
                            border_radius=8,
                            on_click=lambda e: shift_selected_month(-1),
                            ink=True,
                        ),
                        month_label,
                        ft.Container(
                            content=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=c("TEXT_PRIMARY")),
                            padding=ft.padding.all(4),
                            border_radius=8,
                            on_click=lambda e: shift_selected_month(1),
                            ink=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                ft.Container(
                    border=ft.border.all(1, c("BORDER")),
                    border_radius=12,
                    bgcolor=c("SURFACE"),
                    padding=ft.padding.all(12),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Completed tasks", size=12, weight="w600", color=c("TEXT_PRIMARY")),
                                    ft.Container(expand=True),
                                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color=th.SUCCESS),
                                ]
                            ),
                            ft.Container(height=6),
                            completion_bar,
                            ft.Container(height=8),
                            completion_bubble,
                            ft.Container(height=8),
                            ft.Column(
                                [
                                    completion_percent_text,
                                    completion_done_text,
                                    completion_ratio_text,
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(height=10),
                ft.Row(
                    [
                        make_stat_card("Overdue", overdue_value),
                        make_stat_card("Upcoming deadlines", upcoming_value),
                        make_stat_card("Streak", streak_value),
                    ],
                    spacing=10,
                ),
                ft.Container(height=10),
                ft.Container(
                    border=ft.border.all(1, c("BORDER")),
                    border_radius=12,
                    bgcolor=c("SURFACE"),
                    padding=ft.padding.all(10),
                    content=ft.Column(
                        [
                            ft.Text("Productivity by weekday", size=12, weight="w600", color=c("TEXT_PRIMARY")),
                            ft.Container(height=4),
                            ft.Container(content=chart_bars_row, height=110),
                            ft.Container(height=4),
                            most_productive_text,
                        ],
                        spacing=0,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )

    # Filter area (placeholder for now)
    todo_filter_area = ft.Container(
        height=60,
        bgcolor=th.TEXT_ON_PRIMARY,
        border_radius=RADIUS_LG,
        border=ft.border.all(2, c("BORDER")),
        padding=ft.padding.all(12),
    )

    refresh_tasks_list()
    refresh_filter_ui()
    refresh_statistics_ui()

    # Back button
    todo_back_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ARROW_BACK, size=14, color=c("TEXT_ON_PRIMARY")),
             ft.Text("Back", size=12, color=c("TEXT_ON_PRIMARY"), weight="w600")],
            spacing=4,
        ),
        on_click=lambda e: (
            setattr(main_panel, "content", home_panel_ref[0]),
            main_panel.update()
        ),
        ink=True,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        gradient=grad(),
    )

    # Main todo detail panel
    todo_detail_panel = ft.Container(
        expand=True,
        bgcolor=th.TEXT_ON_PRIMARY,
        border_radius=RADIUS_LG,
        padding=ft.padding.all(24),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("To-Do List", size=20, weight="bold", color=c("TEXT_PRIMARY")),
                        ft.Container(expand=True),
                        todo_back_btn,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=16),
                todo_filter_area,
                ft.Container(height=16),
                ft.Row(
                    [todo_tasks_panel, todo_stats_panel],
                    spacing=16,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )

    def get_todo_refs():
        """Grąžina dict su visais theme-priklausomais ref'ais"""
        return {
            "todo_detail_panel": todo_detail_panel,
            "todo_tasks_panel": todo_tasks_panel,
            "todo_stats_panel": todo_stats_panel,
            "todo_filter_area": todo_filter_area,
            "todo_back_btn": todo_back_btn,
        }

    def refresh_todo_theme():
        """Atnaujina To-Do panelių temą"""
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

    return todo_detail_panel, get_todo_refs, refresh_todo_theme, set_home_panel
