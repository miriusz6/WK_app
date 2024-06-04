

import flet as ft
from custom_controls.icon_button_g import IconButtonG
from custom_controls.icon_button_labeled import IconButtonLabeled, LabelPlacement
from utils_mix.DirectoryTree import FileTypes


class ExplorerElement(ft.Column):
    def __init__(self,file, icon_size=50, **kwargs):
        super().__init__(**kwargs)
        self.icon_size = icon_size
        self.file = file


        icon = None
        name = file.name

        if file.file_type == FileTypes.DIRECTORY:
            icon = ft.icons.FOLDER
            if len(file.children) == 0:
                #name = name + "(empty)"
                icon = ft.icons.FOLDER_OPEN
        else:
            icon = ft.icons.AUDIO_FILE
            name = name + file.extension

        self.label = ft.Text(name, text_align=ft.TextAlign.CENTER)
        self.button_gestured = IconButtonG(icon,
                                           data=file,
                                           icon_size=self.icon_size
                                           )
        self.button_labeled = IconButtonLabeled(button=self.button_gestured,
                                                label=self.label,
                                                label_placement=LabelPlacement.BOTTOM)

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

        self.default_color= self.button_gestured.icon_button.icon_color
        self.cut_color = ft.colors.with_opacity(0.5, ft.colors.PRIMARY)



    def disable_label_edit(self):
        label_txt = self.buffered_label_txt = self.button_labeled.label.value
        self.button_labeled.insert_label(ft.Text(value=label_txt))
        self.update()


    def enable_label_edit(self, on_submit):
        self.buffered_label_txt = self.button_labeled.label.value
        new_label = ft.TextField(value=self.buffered_label_txt, autofocus=True)
        def on_submit_wrapper(e):
            on_submit(e, new_label.value, self.buffered_label_txt)
        new_label.on_submit = on_submit_wrapper
        new_label.on_blur = on_submit_wrapper
        self.button_labeled.insert_label(new_label)
        self.update()


    def cut(self):
        self.button_gestured.icon_button.icon_color = self.cut_color
        self.update()

    def selected(self):
        self.button_gestured.icon_button.icon_color = self.default_color
        self.update()

    def default(self):
        self.button_gestured.icon_button.icon_color = self.default_color
        self.update()


