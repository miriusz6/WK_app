import flet as ft
import flet_core.types
import os
CURR_DIR = os.getcwd()

import utils_mix.utils as utils
from custom_controls.guarded_text_field import GuardedTextField

window_name = "counter"
#window_name = "Chrome"

overlay_mouse_menus = []

def add_overlay_menu(menu):
    overlay_mouse_menus.append(menu)

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.scroll = flet_core.types.ScrollMode.ALWAYS




    name_txt = GuardedTextField(label="Name", value="Krzysztof", guard=lambda x: len(x) > 3)
    # name_txt = ft.TextField(label="Name", prefix=ft.Row(
    #             [ft.IconButton(ft.icons.SAVE_SHARP), ft.IconButton(ft.icons.REDO_ROUNDED)],
    #             alignment=ft.MainAxisAlignment.END,
    #             tight=True))
    # name_txt, lambda x: len(x) > 3,page

    personal_info_column = ft.Column(
        [
            name_txt,
            ft.TextField(label="CPR number"),
            ft.TextField(label="SKAT code"),
            ft.TextField(label="Email"),
            ft.TextField(label="Phone number"),
        ],
        spacing=10)
    #page.add(personal_info_column)



    # page.add(ft.Icon(name=ft.icons.SMART_BUTTON, size=100))
    # page.add(ft.Icon(name=ft.icons.SMART_BUTTON, size=100))
    # page.add(ft.Icon(name=ft.icons.SMART_BUTTON, size=100))


    #page.add(explorer)







    #page.theme.primary_color.
    #page.bgcolor = ft.colors.BROWN_900
    page.theme = ft.Theme(color_scheme_seed='green')
    page.platform = ft.PagePlatform.WINDOWS
    page.theme_mode = ft.ThemeMode.LIGHT
    print(page.theme)
    # page.add(ft.Text("Hello world", size=20, color=ft.colors.WHITE))


    grid = ft.Column( controls = [
        ft.Row(controls = [
            ft.Text("JELLO",size = 30),
            ft.Text("JELLO1",size = 30),
            ft.Text("JELLO2",size = 30),
            ft.Icon(ft.icons.FAVORITE, size=30),
            ft.TextButton(icon=ft.icons.FAVORITE, text=""),

        ],
        spacing = 100,
        #width= 300,
        ),
        ft.Row(controls = [
            ft.Text("JELLO",size = 30),
            ft.Text("JELLO1",size = 30),
            ft.Text("JELLO2",size = 30),
            ft.Text("JELLO3",size = 30),
            ft.IconButton(ft.icons.FAVORITE, icon_size=30),
        ],
        spacing = 100,
        #width= 300,
        #height= 600
            #run_spacing=250,
        )]
        )

    stack = ft.Stack(clip_behavior=ft.ClipBehavior.NONE)

    gesture = ft.GestureDetector(on_double_tap= lambda x: print("2xtap"), on_pan_start=lambda x: print("pan_star"))
    #flet_core.control_event.ControlEvent
    def print_event_info(event):
        #(self, target: str, name: str, data: str, control, page):
        # print(event.target)
        # print(event.name)
        # print(event.data)
        # print(event.control)
        print("area chaned")

    gesture.content = grid
    selectable = ft.SelectionArea(content=grid, on_change= print_event_info)

    #stack.controls=[gesture]
    stack.controls=[gesture,selectable]
    stack.controls = [gesture, selectable]

    from custom_controls.explorer.explorer import Explorer
    explorer = Explorer(root_path="C:/felt_WK_app")  # (utils.CURR_DIR + "/mockup_files")

    page.add(explorer)

    from custom_controls.buttons.text_highlightable import TextHighlightable
    high_txt = TextHighlightable(value="Hello world", size=20)
    page.add(high_txt)
    high_txt.highlight("h")

    # for name in os.listdir("C:/"):
    #     print(name)


    for menu in explorer.overlay:
        page.overlay.append(menu)

    page.update()

    #print(os.path.split(CURR_DIR))




# poetry run flet run -d -r [script]
#
class myApp(ft.FletApp):
    def __init__(self):
        # super().__init__(main)
        # print(self.cursor_position )
        print("Hello")

app = ft.app(main)


#ft.app(target=main)


