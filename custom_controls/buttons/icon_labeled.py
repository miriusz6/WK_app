import flet as ft

from custom_controls.buttons.label_placement import LabelPlacement

class IconLabeled(ft.Column):
    def __init__(self, label: ft.Text,
                 icon: ft.Icon = None,
                 label_placement: LabelPlacement = LabelPlacement.BOTTOM,
                 gestured: bool = False,
                 **kwargs,
                 ):
        super().__init__(**kwargs)

        self.label_placement = label_placement
        if gestured:
            self.gesture = ft.GestureDetector(content = icon)
        self.icon = icon
        self.label = label

        self.alignment = ft.MainAxisAlignment.CENTER

        self.icon.padding = ft.Padding(0, 0, 0, 0)
        self.label.width = self.icon.size
        self.editable_label = ft.TextField(value=label.value, autofocus=True)

        self.label = label
        if gestured:
            button_child = self.gesture
        else:
            button_child = self.icon

        if self.label_placement == LabelPlacement.TOP:
            self.controls = [self.label, self.editable_label, button_child]
        elif self.label_placement == LabelPlacement.BOTTOM:
            self.controls = [button_child, self.editable_label, self.label]
        elif self.label_placement == LabelPlacement.LEFT:
            self.controls = [ft.Row([self.editable_label, self.label, button_child],
                                    alignment=ft.MainAxisAlignment.CENTER)]
        elif self.label_placement == LabelPlacement.RIGHT:
            self.controls = [ft.Row([button_child, self.label, self.editable_label],
                                    alignment=ft.MainAxisAlignment.CENTER)]
        self.editable_label.visible = False
        self._on_new_label_txt_submit = lambda _e: print("No on_new_label_txt_submit set")


    def disable_label_edit(self):
        self.label.visible = True
        self.editable_label.visible = False
        self.label.value = self.editable_label.value
        self.update()


    def enable_label_edit(self):
        self.editable_label.visible = True
        self.label.visible = False
        self.editable_label.value = self.label.value
        self.update()

    @property
    def on_new_label_txt_submit(self):
        return self._on_new_label_txt_submit

    @on_new_label_txt_submit.setter
    def on_new_label_txt_submit(self, value):
        self._on_new_label_txt_submit = value
        self.editable_label.on_submit = self.on_new_label_txt_submit
        self.editable_label.on_blur = self.on_new_label_txt_submit
