import flet as ft
import flet_core.types

import sys


def install(name):
    if sys.platform == "emscripten":  # check if run in Pyodide environment
        import micropip
        micropip.install(name)

async def main_page(page: ft.Page):

    def body():

        print(type(page))
        install("PyAutoGui")
        install("pyautogui")

        import pyautogui
        def get_windows_info():
            windows = []
            for x in pyautogui.getAllWindows():
                print(x.title)
                windows.append(x.title)
            return windows

        page.title = "Flet counter example"
        page.scroll = flet_core.types.ScrollMode.ALWAYS

        page.add(ft.Text("Hello World ! !"))


        def change_site(_e):
            ws = get_windows_info()
            for w in ws:
                page.add(ft.Text(w))

            page.update()

        page.add(ft.IconButton(icon=ft.icons.SMART_BUTTON, icon_size=100,
                               on_click= change_site))


        page.update()

    body()
    #body()



#
# async def main(scope, receive, send):
#     print("Running")
#     print(scope)
#     print(receive)
#     print(send)
#     await ft.app(target=main_page, export_asgi_app=True)
#     #print("Running")
#


FLET_FORCE_WEB_SERVER = True


ft.app(target=main_page)#, export_asgi_app=True)