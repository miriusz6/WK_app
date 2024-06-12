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
    #page.scroll = flet_core.types.ScrollMode.ALWAYS




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
    #print(page.theme)
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



    from custom_controls.buttons.text_highlightable import TextHighlightable
    high_txt = TextHighlightable(value="Hello world", size=20)
    #page.add(high_txt)
    high_txt.highlight("h")

    # for name in os.listdir("C:/"):
    #     print(name)




    txt = ft.Text(str(page.controls), size=40)


    gest = ft.GestureDetector(txt)
    a = lambda _e: print("A")
    b = lambda _e: print("B")



    gest.on_tap = a

    def sm(_e, a = gest.on_tap):

        a(_e)
        print("B")
    gest.on_tap = lambda  _e: sm(_e)
    #gest.on_tap = lambda _e: print("C")
    #page.add(gest)


    # from utils_mix.DirectoryTree import DirectoryTreeElement
    # from utils_mix.DirectoryTree import ExplorerElement
    # from utils_mix.DirectoryTree import FileTypes
    # f = DirectoryTreeElement(name="C:/felt_WK_app", file_type=FileTypes.DIRECTORY,
    #                          path  = "path",
    #                         depth= 0,
    #                         extension = None,
    #                          explorer_element= None
    #                          )
    #


    main_col = ft.Column(width=500,height = 500)#, wrap= True)
    sub_col = ft.Column(wrap= True)#,expand=True, expand_loose=True, spacing=10)
    card1 = ft.Card(ft.Text("Hello world", size=25),color =ft.colors.BROWN_900, width=100, height=150)
    card2 = ft.Card(ft.Text("Hello world", size=20),color =ft.colors.BLUE_GREY_50,width=200, height=150)
    sub_col.controls = [card1, card2,card1, card2,card1, card2,card1, card2]
    main_col.controls = [ft.Container(sub_col, bgcolor=ft.colors.BLUE_ACCENT,
                                      expand=True,
                                      clip_behavior=ft.ClipBehavior.HARD_EDGE)]


    def enlarge(_e):
        main_col.height = main_col.height  + 100
        main_col.update()

    def shrink(_e):
        main_col.height = main_col.height  - 100
        main_col.update()

    #page.add(ft.IconButton(ft.icons.FAVORITE, icon_size=30, on_click= enlarge ))
    #page.add(ft.IconButton(ft.icons.START, icon_size=30, on_click= shrink ))

    #page.add(main_col)

    top_txt = ft.Text("Top", size=20, expand=True)
    bottom_txt = ft.Text("Bottom", size=20, expand=True)

    top = ft.Row([ft.Container(content=top_txt,bgcolor=ft.colors.BROWN_400,
                               expand=True, alignment=ft.alignment.top_center
                               )], #height=100,
                                expand=True,
                                alignment=ft.MainAxisAlignment.START
                      )

    bottom = ft.Row([ft.Container(content=bottom_txt,bgcolor=ft.colors.BLUE_200,
                                  expand=True
                                  )],
                      expand=True,
                      )



    col = ft.Column([top,bottom], alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.START

                    )


    m = ft.Container(bgcolor=ft.colors.RED_ACCENT_400, content=col,
                     expand=True
                     # height= 300,
                     # width= 300
                     )

    #page.add(m)

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.AMBER,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.RED,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )




    page.add(explorer)
    #explorer.expand = True
    for menu in explorer.overlay:
        page.overlay.append(menu)

    #
    # def print_e_info(e):
    #     #target: str, name: str, data: str, control, page#
    #     print(e.target)
    #     print(e.name)
    #     print(e.data)
    #     print(e.control)
    #
    #
    # page.on_resize = print_e_info


    page.update()

    #print(os.path.split(CURR_DIR))




def main_(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


#ft.app(target=main)#, view=ft.AppView.WEB_BROWSER)










# poetry run flet run -d -r [script]
#
class myApp(ft.FletApp):
    def __init__(self):
        # super().__init__(main)
        # print(self.cursor_position )
        print("Hello")





app = ft.app(main)#,view=ft.AppView.WEB_BROWSER)

# app.routes = [
#     ft.Route("/", main),
#     ft.Route("/hello", hello)
# ]
# #ft.app(target=main)
#
# import webbrowser
#
#
# #your staff
# #@app.route("/")
# def hello():
#     return("Hello World!")
#
# def open_browser():
#     webbrowser.open_new('http://127.0.0.1:5000/')
#
# if __name__ == "__main__":
#     # the command you want
#     open_browser()
#     app.run(port=5000)

