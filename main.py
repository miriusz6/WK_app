
from collections.abc import Callable
import flet as ft
import flet_core.types
from pymouse import PyMouse
import os
CURR_DIR = os.getcwd()

import utils_mix.utils as utils
from custom_controls.guarded_text_field import GuardedTextField
from custom_controls.icon_button_labeled import IconButtonLabeled

#window_name = "counter"
window_name = "Chrome"

from custom_controls.mouse_menu import MouseMenuExplorerElement

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

    from custom_controls.explorer import Explorer
    explorer = Explorer(utils.CURR_DIR + "/mockup_files")
    #page.add(explorer)


    for menu in explorer.overlay:
        page.overlay.append(menu)




    #page.theme.primary_color.
    page.bgcolor = ft.colors.BROWN_900
    page.platform = ft.PagePlatform.WINDOWS

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



    #page.add(stack)
    # page.add(grid)

    #


    # page.overlay.append(ft.Column([
    #     ft.Row([ft.Text("Nothing")] , expand_loose=True),
    #     ],
    #     height=200,
    # ))

    # img = ft.Image(src="C:/felt_WK_app/blue_square.png",
    #                          fit=ft.ImageFit.FILL,
    #                          #repeat=ft.ImageRepeat.REPEAT,
    #                          #color=ft.colors.BLACK,
    #                          opacity=0.5,
    #                          expand=True,
    #                         #width=100,
    #                         #height=100,
    #                          border_radius=ft.border_radius.all(10),
    #                          #border = None,
    #                          )
    #
    # drag_img = ft.Draggable(
    #         content = ft.Column([
    #             ft.Row([
    #                 img,
    #                 ],
    #                 alignment=ft.MainAxisAlignment.CENTER,
    #             )
    #         ],
    #             expand_loose=True,
    #             alignment=ft.MainAxisAlignment.CENTER,
    #         ),
    #         group="KUPA",
    #         on_drag_start=lambda x: print("DRAG START"),
    #     )
    #
    # drag_img_wrap = ft.Column([
    #     drag_img,
    #     ],
    #     expand_loose=True,
    #     alignment=ft.MainAxisAlignment.CENTER,
    # )
    #
    # def on_drag_start(_e):
    #     print("DRAG START")
    #     #drag_img_wrap.width = 100
    #     #drag_img_wrap.height = 100
    #     drag_img_wrap.left = 300
    #     drag_img_wrap.top = 300
    #     img.expand = False
    #     img.width = 300
    #     img.height = 300
    #     drag_img.update()
    #
    # drag_img.on_drag_start = on_drag_start
    #
    # #page.overlay.append(drag_img_wrap)
    #
    # page.overlay.append(ft.Row([ft.Draggable(ft.Icon(ft.icons.RULE_FOLDER, size=100),
    #                        group="KUPA",
    #                        )],
    #                            left=200
    #                            ,top=200
    #                            )
    #                            )
    #
    # page.add(ft.DragTarget(ft.Icon(ft.icons.RULE_FOLDER, size=100),
    #                        group="KUPA",
    #                        on_accept=lambda x: print("KUPA"),
    #                        on_will_accept=lambda x: print("WILL KUPA"),
    #                        ))
    #
    page.add(explorer)

    page.update()




# poetry run flet run -d -r [script]

class myApp(ft.FletApp):
    def __init__(self):
        # super().__init__(main)
        # print(self.cursor_position )
        print("Hello")

app = ft.app(main)



