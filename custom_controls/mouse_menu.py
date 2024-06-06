from utils_mix.MouseEvents import subscribe_click_events, Button
import flet as ft


class MouseMenu(ft.Container):
    def __init__(self,menu_buttons: list[ft.TextButton], **kwargs):
        super().__init__(**kwargs)
        self.controls = []

        self.button_height = 50
        self.button_width = 100
        self.column = ft.Column(menu_buttons)
        self.column.height = len(menu_buttons)*self.button_height
        self.column.spacing = 5
        self.column.height += self.column.spacing*(len(menu_buttons)-1)
        self.padding = ft.Padding(0, 0, 0, 0)

        self.content = self.column
        self.border_radius = 5
        self.border = ft.border.all(1, "black")

        self.buttons_style = ft.ButtonStyle(color=ft.colors.BLACK,
                                            shape=ft.RoundedRectangleBorder(radius=5),
                                            side=ft.border.all(1, ft.colors.BLACK),
                                            bgcolor=ft.colors.GREY
                                            )

        for button in menu_buttons:
            button.padding = ft.Padding(0, 0, 0, 0)
            button.width = self.button_width
            button.height = self.button_height
            button.style = self.buttons_style

        #subscribe_click_events(Button.left,self.__on_click_outside)


    def show_at(self, x, y):
        self.visible = True
        self.left = x
        self.top = y
        #self.data = assigned_file
        self.update()

    def hide(self):
        self.visible = False
        self.update()


    def __on_click_outside(self, _x, _y):
        self.visible = False
        self.update()

    def wrap_event_call_add_menu_data(self, f):
        def wrapper(e):
            #e.control.file = self.data
            e.data = self.data
            f(e)
            self.hide()
        return wrapper
class MouseMenuExplorerElement(MouseMenu):
    def __init__(self, **kwargs):
        self.open_button = ft.TextButton("Open")
        self.delete_button = ft.TextButton("Delete")
        self.rename_button = ft.TextButton("Rename")
        self.cut_button = ft.TextButton("Cut")
        self.copy_button = ft.TextButton("Copy")
        self.paste_button = ft.TextButton("Paste")


        super().__init__(menu_buttons = [
            self.paste_button,
            self.open_button,
             self.delete_button,
             self.rename_button,
             self.cut_button,
             self.copy_button,
             ],
                         **kwargs)
        self.visible = False

    def set_on_open(self, on_open):
        pass
        self.open_button.on_click = self.wrap_event_call_add_menu_data(on_open)

    def set_on_delete(self, on_delete):
        self.delete_button.on_click = self.wrap_event_call_add_menu_data(on_delete)

    def set_on_rename_enable(self, on_rename):
        self.rename_button.on_click = self.wrap_event_call_add_menu_data(on_rename)

    def set_on_rename_submit(self, on_rename_submit):
        pass
        self.rename_button.on_click = self.wrap_event_call_add_menu_data(on_rename_submit)

    def set_on_new_folder(self, on_new_folder):
        self.cut_button.on_click = self.wrap_event_call_add_menu_data(on_new_folder)

    def set_on_copy(self, on_copy):
        self.copy_button.on_click = self.wrap_event_call_add_menu_data(on_copy)

    def set_on_cut(self, on_cut):
        self.cut_button.on_click = self.wrap_event_call_add_menu_data(on_cut)

    def set_on_paste(self, on_paste):
        self.paste_button.on_click = self.wrap_event_call_add_menu_data(on_paste)

class MouseMenuExplorerBackground(MouseMenu):
    def __init__(self, **kwargs):
        self.new_folder_button = ft.TextButton("New Folder")
        self.paste_button = ft.TextButton("Paste")
        super().__init__(menu_buttons = [
            self.new_folder_button,
            self.paste_button,
        ],
                         **kwargs)
        self.visible = False

    def set_on_new_folder(self, on_new_folder):
        self.new_folder_button.on_click = self.wrap_event_call_add_menu_data(on_new_folder)

    def set_on_paste(self, on_paste):
        self.paste_button.on_click = self.wrap_event_call_add_menu_data(on_paste)


#class MouseMenuEvent(ft.):