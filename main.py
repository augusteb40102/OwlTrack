import flet as ft
from ui.auth.start_view import start_view
from ui.auth.login_view import login_view

def main(page: ft.Page):

    page.title = "OwlTrack"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(start_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        page.update()

    page.on_route_change = route_change
    route_change(page.route)
    page.update()

ft.app(target=main)
