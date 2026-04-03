import flet as ft
import ui.themes.themes as th
from datetime import datetime

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

    home_panel_ref = [None]  # Placeholder atsiskaityti home_panel iš dashboard_view

    def set_home_panel(home):
        """Nustato home_panel referencą"""
        home_panel_ref[0] = home

    tasks = [
        {"id": 1, "title": "Finish weekly report", "type": "type", "due_date": "2026-04-10", "completed": False},
        {"id": 2, "title": "Exam preparation", "type": "type", "due_date": "2026-04-15", "completed": False},
        {"id": 3, "title": "Team meeting", "type": "type", "due_date": "2026-04-05", "completed": False},
    ]

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
        value="type",
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

    def open_task_form(mode: str, task_id: int = None):
        form_error_text.visible = False
        form_error_text.value = ""

        if mode == "add":
            dialog_title.value = "Add new task"
            title_field.value = ""
            type_field.value = "type"
            due_date_field.value = datetime.now().strftime("%Y-%m-%d")
            confirm_label = "Add"
        else:
            task = next((t for t in tasks if t["id"] == task_id), None)
            if not task:
                return
            dialog_title.value = "Edit task"
            title_field.value = task["title"]
            type_field.value = task["type"] or "type"
            due_date_field.value = task["due_date"]
            confirm_label = "Save"

        def on_confirm(e):
            title_value = (title_field.value or "").strip()
            type_value = (type_field.value or "type").strip() or "type"
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
        for task in tasks:
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
                                    f"type • {days_text}",
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
                break
        refresh_tasks_list()
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
        page.update()

    def add_new_task(e=None):
        open_task_form("add")

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
                ft.Text("Statistics", size=14, weight="bold", color=c("TEXT_PRIMARY")),
                ft.Container(height=8),
                ft.Text("(Coming soon ;PPPP 676767696969)", size=12, color=c("TEXT_SECONDARY")),
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

    refresh_tasks_list()

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

    return todo_detail_panel, get_todo_refs, refresh_todo_theme, set_home_panel
