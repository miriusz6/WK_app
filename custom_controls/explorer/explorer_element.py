

import flet as ft
#from custom_controls.icon_button_g import IconButtonG
from custom_controls.buttons.icon_button_labeled import IconButtonLabeled, LabelPlacement
from utils_mix.DirectoryTree import FileTypes

from typing import Callable
class ExplorerElement(ft.Column):
    def __init__(self,file, icon_size=50, **kwargs):
        super().__init__(**kwargs)
        self.icon_size = icon_size
        self.file = file

        name = file.name

        if file.file_type == FileTypes.DIRECTORY:
            icon = ft.icons.FOLDER
            if len(file.children) == 0:
                icon = ft.icons.FOLDER_OPEN
        else:
            icon = ft.icons.AUDIO_FILE
            name = name + file.extension

        self.label = ft.Text(name, text_align=ft.TextAlign.CENTER)
        button = ft.IconButton(icon, icon_size=self.icon_size)

        self.button_labeled = IconButtonLabeled(button=button,
                                                gestured=True,
                                                label=self.label,
                                                label_placement=LabelPlacement.BOTTOM)
        self.gesture = self.button_labeled.gesture

        if file.file_type == FileTypes.DIRECTORY:
            self.draggable = ft.Draggable(
                              group="exp",
                              content=self.button_labeled
                              )
            self.drag_target = ft.DragTarget(
                                group="exp",
                                content=self.draggable
                                )
            self.controls = [self.drag_target]
        else:
            self.draggable = ft.Draggable(
                    group="exp",
                    content=self.button_labeled
                )
            self.drag_target = None
            self.controls = [self.draggable]

        self.default_color = self.button_labeled.button.icon_color
        self.cut_color = ft.colors.with_opacity(0.5, ft.colors.PRIMARY)
        self._on_new_name_submit = lambda e: None

    @property
    def name (self):
        return self.label.value

    @property
    def on_new_name_submit(self):
        return self._on_new_name_submit

    @on_new_name_submit.setter
    def on_new_name_submit(self, value):
        self._on_new_name_submit = value
        self.button_labeled.on_new_label_txt_submit = value

    def disable_name_edit(self):
        self.button_labeled.disable_label_edit()

    def enable_name_edit(self):
        self.button_labeled.enable_label_edit()



    def cut(self):
        self.button_labeled.button.icon_color = self.cut_color
        self.update()

    def selected(self):
        self.button_labeled.button.icon_color = self.default_color
        self.update()

    def default(self):
        self.button_labeled.button.icon_color = self.default_color
        self.update()

