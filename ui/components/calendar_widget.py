import flet as ft
import calendar
from datetime import date
import ui.themes.themes as th

DAYS_SHORT  = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
MONTH_NAMES = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

RADIUS_LG = 20


def build_calendar(page: ft.Page, c, grad, main_panel: ft.Container):
    """
    Sukuria kompaktinį ir detalų kalendorių.

    Grąžina:
        compact_calendar  — widget rodomas home_panel
        detail_view_panel — widget rodomas paspaudus dieną
        get_theme_refs()  — funkcija grąžinanti dict su visais
                            theme-priklausomais ref'ais (save_settings naudoja)
    """

    today        = date.today()
    cal_year     = [today.year]
    cal_month    = [today.month]
    selected_day = [None]

    def _month_str():
        return MONTH_NAMES[cal_month[0] - 1].upper()

    # ── SHARED GRID BUILDER ───────────────────────────────────────────
    def _build_grid(cell_h, num_size, num_dim, spacing, on_click_fn):
        year  = cal_year[0]
        month = cal_month[0]

        first_weekday, days_in_month = calendar.monthrange(year, month)
        start_offset = (first_weekday + 1) % 7
        all_days = [0] * start_offset + list(range(1, days_in_month + 1))
        while len(all_days) % 7 != 0:
            all_days.append(0)

        header_cells = [
            ft.Container(
                content=ft.Text(d, size=num_size - 2, color=c("TEXT_SECONDARY"),
                                weight="bold", text_align=ft.TextAlign.CENTER),
                expand=True, height=num_dim,
                alignment=ft.Alignment(0, 0),
            )
            for d in DAYS_SHORT
        ]

        rows = [ft.Row(header_cells, spacing=spacing)]
        for week_start in range(0, len(all_days), 7):
            week = all_days[week_start:week_start + 7]
            cells = []
            for day in week:
                if day == 0:
                    cells.append(ft.Container(expand=True, height=cell_h))
                else:
                    is_today = (day == today.day and month == today.month and year == today.year)
                    is_sel   = selected_day[0] == day

                    if is_today:
                        nb, tc, fw = c("PRIMARY"), c("TEXT_ON_PRIMARY"), "bold"
                    elif is_sel:
                        nb, tc, fw = c("SECONDARY"), c("TEXT_ON_PRIMARY"), "bold"
                    else:
                        nb, tc, fw = ft.Colors.TRANSPARENT, c("TEXT_PRIMARY"), "normal"

                    num_box = ft.Container(
                        content=ft.Text(str(day), size=num_size, color=tc,
                                        weight=fw, text_align=ft.TextAlign.CENTER),
                        width=num_dim, height=num_dim,
                        bgcolor=nb, border_radius=num_dim // 2,
                        alignment=ft.Alignment(0, 0),
                    )
                    cell = ft.Container(
                        content=ft.Column(
                            [num_box],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True, height=cell_h,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.12, c("SECONDARY"))),
                        bgcolor=ft.Colors.with_opacity(0.07, c("SECONDARY")),
                        alignment=ft.Alignment(0, -0.7),
                        on_click=lambda e, d=day: on_click_fn(d),
                        ink=True,
                    )
                    cells.append(cell)
            rows.append(ft.Row(cells, spacing=spacing))

        return ft.Column(rows, spacing=spacing, tight=True)

    # ── COMPACT CALENDAR ──────────────────────────────────────────────
    compact_month_label = ft.Text(_month_str(), size=14, weight="bold", color=c("TEXT_PRIMARY"))
    compact_year_label  = ft.Text(str(cal_year[0]), size=14, weight="bold", color=c("TEXT_PRIMARY"))
    compact_grid_slot   = ft.Container()

    cal_prev_icon = ft.Icon(ft.Icons.CHEVRON_LEFT,  size=18, color=c("TEXT_PRIMARY"))
    cal_next_icon = ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color=c("TEXT_PRIMARY"))
    yr_prev_icon  = ft.Icon(ft.Icons.CHEVRON_LEFT,  size=18, color=c("TEXT_PRIMARY"))
    yr_next_icon  = ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color=c("TEXT_PRIMARY"))

    cal_prev_btn = ft.Container(content=cal_prev_icon, on_click=lambda e: _nav_cal(-1),
                                ink=True, border_radius=16, padding=4)
    cal_next_btn = ft.Container(content=cal_next_icon, on_click=lambda e: _nav_cal(1),
                                ink=True, border_radius=16, padding=4)
    yr_prev_btn  = ft.Container(content=yr_prev_icon,  on_click=lambda e: _nav_year(-1),
                                ink=True, border_radius=16, padding=4)
    yr_next_btn  = ft.Container(content=yr_next_icon,  on_click=lambda e: _nav_year(1),
                                ink=True, border_radius=16, padding=4)

    def _refresh_compact():
        compact_month_label.value = _month_str()
        compact_year_label.value  = str(cal_year[0])
        compact_grid_slot.content = _build_grid(
            cell_h=95, num_size=13, num_dim=34, spacing=2,
            on_click_fn=_on_compact_day_click,
        )

    def _nav_cal(delta):
        cal_month[0] += delta
        if cal_month[0] > 12: cal_month[0] = 1;  cal_year[0] += 1
        if cal_month[0] < 1:  cal_month[0] = 12; cal_year[0] -= 1
        _refresh_compact()
        page.update()

    def _nav_year(delta):
        cal_year[0] += delta
        _refresh_compact()
        page.update()

    day_popup = ft.AlertDialog(
        modal=True,
        bgcolor=c("SURFACE"),
        title=ft.Text("", size=16, weight="bold", color=c("TEXT_PRIMARY")),
        content=ft.Container(
            width=300,
            height=100,
            content=ft.Text("", size=13, color=c("TEXT_SECONDARY")),
        ),
        actions=[
            ft.TextButton(
                "Close",
                on_click=lambda e: close_popup(),
                style=ft.ButtonStyle(color=c("PRIMARY")),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_popup():
        day_popup.open = False
        page.update()

    def _on_compact_day_click(day):
        selected_day[0] = day
        _refresh_compact()
        _open_detail()
        page.update()

    compact_calendar = ft.Container(
        expand=True,
        padding=ft.padding.all(14),
        border_radius=RADIUS_LG,
        bgcolor=th.TEXT_ON_PRIMARY,
        border=ft.border.all(2, c("BORDER")),
        on_click=lambda e: _open_detail(),  
        ink=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row([cal_prev_btn, compact_month_label, cal_next_btn],
                               spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(expand=True),
                        ft.Row([yr_prev_btn, compact_year_label, yr_next_btn],
                               spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                ),
                ft.Container(height=8),
                compact_grid_slot,
            ],
            spacing=0, tight=True,
        ),
    )

    _refresh_compact()

    # ── DETAIL CALENDAR ───────────────────────────────────────────────
    detail_month_label    = ft.Text("", size=20, weight="bold", color=c("TEXT_PRIMARY"))
    detail_schedule_month = ft.Text("", size=13,
                                    color=ft.Colors.with_opacity(0.85, "#FFFFFF"))
    detail_grid_slot = ft.Container(expand=True)

    detail_header_box = ft.Container(
        padding=ft.padding.all(16),
        border_radius=RADIUS_LG,
        gradient=grad(),
        content=ft.Column(
            [
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_MONTH, color="#FFFFFF", size=16),
                    ft.Text("My Calendar", size=14, weight="bold", color="#FFFFFF"),
                ], spacing=8),
                ft.Container(height=6),
                detail_schedule_month,
            ],
            spacing=0,
        ),
    )

    detail_back_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ARROW_BACK, size=14, color=c("TEXT_ON_PRIMARY")),
             ft.Text("Back", size=12, color=c("TEXT_ON_PRIMARY"), weight="w600")],
            spacing=4,
        ),
        on_click=lambda e: _close_detail(),
        ink=True, border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        gradient=grad(),
    )

    detail_prev_btn = ft.Container(
        content=ft.Icon(ft.Icons.CHEVRON_LEFT, size=22, color=c("TEXT_PRIMARY")),
        on_click=lambda e: _detail_nav(-1), ink=True, border_radius=20, padding=6,
    )
    detail_next_btn = ft.Container(
        content=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=22, color=c("TEXT_PRIMARY")),
        on_click=lambda e: _detail_nav(1), ink=True, border_radius=20, padding=6,
    )

    def _on_detail_day_click(day):
        selected_day[0] = day
        _refresh_detail()
        _refresh_compact()
        day_popup.title.value = f"{MONTH_NAMES[cal_month[0]-1]} {day}, {cal_year[0]}"
        day_popup.content.content.value = "No events for this day yet."
        day_popup.open = True
        if day_popup not in page.overlay:
            page.overlay.append(day_popup)
        page.update()

    def _detail_nav(delta):
        cal_month[0] += delta
        if cal_month[0] > 12: cal_month[0] = 1;  cal_year[0] += 1
        if cal_month[0] < 1:  cal_month[0] = 12; cal_year[0] -= 1
        _refresh_detail()
        _refresh_compact()
        page.update()

    def _refresh_detail():
        detail_schedule_month.value = f"{MONTH_NAMES[cal_month[0]-1]} {cal_year[0]}"
        detail_month_label.value    = f"{MONTH_NAMES[cal_month[0]-1]} {cal_year[0]}"
        detail_grid_slot.content    = _build_grid(
            cell_h=80, num_size=13, num_dim=32, spacing=4,
            on_click_fn=_on_detail_day_click,
        )

    detail_view_panel = ft.Container(
        expand=True,
        bgcolor=th.TEXT_ON_PRIMARY,
        border_radius=RADIUS_LG,
        border=ft.border.all(1, c("BORDER")),
        padding=ft.padding.all(24),
        content=ft.Column(
            [
                detail_header_box,
                ft.Container(height=16),
                ft.Row(
                    [
                        detail_prev_btn,
                        detail_month_label,
                        detail_next_btn,
                        ft.Container(expand=True),
                        detail_back_btn,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Container(height=12),
                detail_grid_slot,
            ],
            spacing=0, expand=True, scroll=ft.ScrollMode.AUTO,
        ),
    )

    def _open_detail():
        _refresh_detail()
        main_panel.content = detail_view_panel
        main_panel.update()

    def _close_detail():
        selected_day[0] = None
        _refresh_compact()
        main_panel.content = None   # home_panel priskiriamas dashboard_view
        main_panel.update()

    # ── THEME REFS (grąžinami save_settings naudojimui) ───────────────
    def get_theme_refs() -> dict:
        return {
            "compact_calendar":    compact_calendar,
            "compact_month_label": compact_month_label,
            "compact_year_label":  compact_year_label,
            "cal_prev_icon":       cal_prev_icon,
            "cal_next_icon":       cal_next_icon,
            "yr_prev_icon":        yr_prev_icon,
            "yr_next_icon":        yr_next_icon,
            "detail_view_panel":   detail_view_panel,
            "detail_header_box":   detail_header_box,
            "detail_back_btn":     detail_back_btn,
            "detail_prev_btn":     detail_prev_btn,
            "detail_next_btn":     detail_next_btn,
            "detail_month_label":  detail_month_label,
        }

    def refresh_after_theme():
        """Iškviečiama po apply_theme() kad perkurtų grid'us naujomis spalvomis."""
        _refresh_compact()
        if main_panel.content is detail_view_panel:
            _refresh_detail()

    def set_home_panel(home):
        """Dashboard priskiria home_panel kad close_detail žinotų kur grįžti."""
        def _close():
            selected_day[0] = None
            _refresh_compact()
            main_panel.content = home
            main_panel.update()
        # Pakeičiame _close_detail closure
        detail_back_btn.on_click = lambda e: _close()

    return compact_calendar, detail_view_panel, get_theme_refs, refresh_after_theme, set_home_panel