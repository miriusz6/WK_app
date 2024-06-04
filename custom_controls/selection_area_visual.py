
import flet as ft


class SelectionAreaVisual(ft.Image):
    def __init__(self):
        super().__init__(src="custom_controls/blue_square.png",
                        #src = "C:/felt_WK_app/blue_square.png",
                         height=0,
                         color = ft.colors.with_opacity(0.5, ft.colors.INDIGO),
                         width = 0,
                         )
        self.init_pos = (0, 0)
        #self.visible = False
        self.fit = "fill"

    def calc_new_pos(self, old_pos, new_pos):
        # calculate left upper corner of the selection area
        # with two opposite corners old_pos and new_pos
        return min(old_pos[0], new_pos[0]), min(old_pos[1], new_pos[1])

    def on_change(self, new_pos):
        from utils_mix.utils import calc_click_pos
        #print("selection_are: on_change")
        new_pos = calc_click_pos(self.page.width, self.page.height, "counter")
        self.width = abs(self.init_pos[0] - new_pos[0])
        self.height = abs(self.init_pos[1] - new_pos[1])
        self.left, self.top = self.calc_new_pos(self.init_pos, new_pos)
        self.update()

    def show(self,x,y):
        #print("selection_are: show")
        #self.visible = True
        self.init_pos = (x,y)
        self.update()

    def hide(self):
        #print("selection_are: hide")
        self.height = 0
        self.width = 0
        self.update()


