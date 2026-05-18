import flet as ft

# Šiame faile yra įgyvendinamas fonas, naudojamas autentifikacijos ekranuose (prisijungimo, registracijos, profilio nuotraukos pasirinkimo). 
# Foną sudaro animuotas kosmoso vaizdas, kuris užpildo visą ekraną, o virš jo yra dedamas perduodamas turinys (pvz., formos, mygtukai). 
# Tai suteikia vizualiai patrauklų ir tematiškai tinkamą foną visiems autentifikacijos susijusiems ekranams.
def auth_background(content, page=None):
    return ft.Stack(
        expand=True,
        width=float("inf"),
        controls=[
            ft.Image(
                src="cosmos_purple.gif",
                width=float("inf"),
                height=float("inf"),
                expand=True,
                fit="fill",
            ),
            ft.Container(
                content=content,
                expand=True,
                alignment=ft.Alignment(0, 0),
            ),
        ]
    )