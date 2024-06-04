import flet as ft
from collections.abc import Callable
import flet_core


class GuardedTextField(ft.TextField):
    def __init__(self, guard: Callable[[str], bool], **kwargs):
        super().__init__(**kwargs)
        self.guard = guard
        self.__closed = True
        self.data = self.value

        self.redo_button = ft.IconButton(ft.icons.REDO_ROUNDED)
        self.redo_button.on_click = self.redo_click
        self.save_button = ft.IconButton(ft.icons.SAVE_SHARP)
        self.save_button.on_click = self.save_click

        GuardedTextField.on_blur.fset(self, self.__on_blur)
        GuardedTextField.on_change.fset(self, self.__on_change)

        self.helper_style = self.text_style
        self.edit_helper_hint = "Write full name here"

        # for editing
        self.opened_style = flet_core.TextStyle(size=30, color="yellow")
        self.opened_border_color = "yellow"
        # default
        self.default_style = self.text_style
        self.default_border_color = self.border_color
        # for closed
        self.closed_style = flet_core.TextStyle(size=20, color="green")
        self.closed_border_color = "green"

        self.buttons = ft.Row(
            [self.redo_button, self.save_button],
            alignment=ft.MainAxisAlignment.END,
            tight=True
        )

    def __on_blur(self, _event):
        print("tries to blur")
        if not self.__closed:
            self.focus()
        else:
            self.set_default_style()
            self.update()

    def __on_change(self, _event):
        # closed
        if self.__closed:
            self.__closed = False
            self.open()
        # wrong input
        if not self.guard(self.value):
            self.prefix = self.redo_button
            self.update()
        # correct input
        else:
            self.error_text = ""
            self.save_button.disabled = False
            self.prefix = self.buttons
            self.update()

    def close(self):
        print("closed")
        self.helper_text = ""
        self.set_closed_style()
        self.__closed = True
        self.error_text = ""
        self.prefix = None
        self.update()

    def set_default_style(self):
        self.text_style = self.default_style
        self.border_color = self.default_border_color

    def set_closed_style(self):
        self.text_style = self.closed_style
        self.border_color = self.closed_border_color

    def set_opened_style(self):
        self.text_style = self.opened_style
        self.border_color = self.opened_border_color

    def open(self):
        print("opened")
        self.set_opened_style()
        self.helper_text = self.edit_helper_hint
        self.__closed = False
        self.value = self.data
        self.update()

    def redo_click(self, _event):
        self.value = self.data
        self.close()
        self.update()

    def save_click(self, _event):
        print("Save clicked")
        self.data = self.value
        self.close()

