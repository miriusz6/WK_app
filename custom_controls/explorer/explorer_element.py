import flet as ft
from custom_controls.buttons.icon_labeled import IconLabeled
from custom_controls.buttons.label_placement import LabelPlacement
from utils_mix.DirectoryTree import FileTypes
from custom_controls.buttons.text_highlightable import TextHighlightable
from typing import Callable
class ExplorerElement(ft.Column):
    def __init__(self,file, icon_size=50, **kwargs):
        super().__init__(**kwargs)
        self.icon_size = icon_size
        self.file = file

        name = file.name

        if file.file_type == FileTypes.DIRECTORY:
            icon_name = ft.icons.FOLDER
            if len(file.children) == 0:
                icon_name = ft.icons.FOLDER_OPEN
        else:
            icon_name = ft.icons.AUDIO_FILE
            name = name + file.extension

        self.label = TextHighlightable(value= name, text_align=ft.TextAlign.CENTER)
        self.icon_labeled = IconLabeled(label=self.label,
                                        icon=ft.Icon(icon_name, size=icon_size),
                                        label_placement=LabelPlacement.BOTTOM)
        self.icon_labeled.run_spacing = 0
        self.icon_labeled.tight = True
        self.expand_loose = False

        self.icon_labeled.alignment = ft.MainAxisAlignment.CENTER



        self.gesture = ft.GestureDetector(content = self.icon_labeled)



        if file.file_type == FileTypes.DIRECTORY:
            self.draggable = ft.Draggable(
                              group="exp",
                              content=self.gesture
                              )
            self.drag_target = ft.DragTarget(
                                group="exp",
                                content=self.draggable
                                )
            self.card = ft.Card(self.drag_target)

        else:
            self.draggable = ft.Draggable(
                    group="exp",
                    content=self.gesture
                )
            self.drag_target = None
            self.card = ft.Card(self.draggable)

        self.controls = [self.card]
        self.spacing = 10

        self.default_icon_color = self.icon_labeled.icon.color
        self.icon_cut_color = ft.colors.with_opacity(0.4, ft.colors.PRIMARY)
        self.selected_color = ft.colors.with_opacity(0.5, ft.colors.PRIMARY)
        self.default_color = self.card.color
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
        self.icon_labeled.on_new_label_txt_submit = value

    def disable_name_edit(self):
        self.icon_labeled.disable_label_edit()

    def enable_name_edit(self):
        self.icon_labeled.enable_label_edit()



    def cut(self):
        self.icon_labeled.icon.color = self.icon_cut_color
        self.update()

    def selected(self):
        self.card.color = self.selected_color
        self.update()

    def default(self):
        self.icon_labeled.icon.color = self.default_icon_color
        self.card.color = self.default_color
        self.update()

    def highlight_name(self):
        self.label.highlight_all()
        self.update()

    def unhighlight_name(self):
        self.label.unhighlight_all()
        self.update()

    def highlight_name_fraze(self, fraze:str, case_sensitive=False):
        self.label.highlight(fraze, case_sensitive)
        self.update()