import flet as ft
from custom_controls.selection_area_visual import SelectionAreaVisual
class SelectionArea(ft.Draggable):
    def __init__(self):
        self.selection_area_visual = SelectionAreaVisual()
        super().__init__(content = self.selection_area_visual)






