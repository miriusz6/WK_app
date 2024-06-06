import flet as ft
import flet_core.types


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.scroll = flet_core.types.ScrollMode.ALWAYS

    page.add(ft.Text("Hello World !"))


    def change_site(_e):
        page.add(ft.Text("Hello World 2 !"))
        page.update()

    page.add(ft.IconButton(icon=ft.icons.SMART_BUTTON, icon_size=100,
                           on_click= change_site))


    page.update()




ft.app(target=main)