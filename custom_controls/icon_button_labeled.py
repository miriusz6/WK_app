import flet as ft
from custom_controls.icon_button_g import IconButtonG

#
# class IconButtonLabeled():
#     def __init__(self,label: ft.Text, icon_button : ft.IconButton):
#
#         self.icon_button = icon_button
#
#         self.icon_button.padding = ft.Padding(0, 0, 0, 0)
#         self.label = label
#         self.label.width = self.icon_button.icon_size
#         self.column = ft.Column([self.icon_button, self.label], alignment=ft.MainAxisAlignment.CENTER)

from custom_controls.icon_button_g import IconButtonG
from enum import Enum


class LabelPlacement(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class IconButtonLabeled(ft.Column):
    def __init__(self, label: ft.Text,
                 button: ft.IconButton | IconButtonG,
                 label_placement: LabelPlacement = LabelPlacement.BOTTOM,
                 **kwargs,
                 ):
        super().__init__(**kwargs)

        self.label_placement = label_placement
        self.label = label
        self.button = button



        self.alignment = ft.MainAxisAlignment.CENTER

        self.button.padding = ft.Padding(0, 0, 0, 0)
        self.label.width = self.button.icon_size

        self.insert_label(label)

    def insert_label(self,label):
        self.label = label
        if self.label_placement == LabelPlacement.TOP:
            self.controls = [self.label, self.button]
        elif self.label_placement == LabelPlacement.BOTTOM:
            self.controls = [self.button, self.label]
        elif self.label_placement == LabelPlacement.LEFT:
            self.controls = [ft.Row([self.label, self.button],
                                    alignment=ft.MainAxisAlignment.CENTER)]
        elif self.label_placement == LabelPlacement.RIGHT:
            self.controls = [ft.Row([self.button, self.label],
                                    alignment=ft.MainAxisAlignment.CENTER)]





