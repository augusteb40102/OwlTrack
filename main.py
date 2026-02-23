import flet as ft
from ui.auth.start_view import start_view
from ui.auth.login_view import login_view
from ui.auth.register_view import register_view
from ui.auth.forgot_password import forgot_password_view

def main(page: ft.Page):
    page.title = "OwlTrack"
    page.padding = 0
    page.spacing = 0

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(start_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        elif page.route == "/forgot-password":
             page.views.append(forgot_password_view(page))
             page.update()

    page.on_route_change = route_change
    route_change(page.route)
    page.update()
    
ft.app(target=main, assets_dir="assets")