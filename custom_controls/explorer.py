import flet as ft
from utils_mix import utils
from custom_controls.icon_button_labeled import IconButtonLabeled, LabelPlacement
from custom_controls.icon_button_g import IconButtonG
from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement, FileTypes
from custom_controls.mouse_menu import MouseMenuExplorerElement, MouseMenuExplorerBackground
from utils_mix.utils import calc_click_pos
from custom_controls.explorer_element import ExplorerElement
from custom_controls.selection_area_visual import SelectionAreaVisual
class Explorer(ft.Column):
    def __init__(self, root_path, elems_pr_row = 5, **kwargs):
        super().__init__(**kwargs)
        self.dir_tree = DirectoryTree(root_path)

        self.elems_pr_row = elems_pr_row
        self.icon_size = 200

        self.top_menu_size = self.icon_size*self.elems_pr_row
        self.top_menu_txt = None
        self.top_menu = self.mk_top_menu()
        self.controls.append(self.top_menu)


        self.mouse_menu_exp_elem = MouseMenuExplorerElement()
        self.mouse_menu_exp_elem.set_on_delete(self.delete_element)
        self.mouse_menu_exp_elem.set_on_open(self.open_element)
        self.mouse_menu_exp_elem.set_on_copy(self.copy_element)
        self.mouse_menu_exp_elem.set_on_paste(self.paste_elem_to_child_dir)
        self.mouse_menu_exp_elem.set_on_cut(self.cut_element)
        self.mouse_menu_exp_elem.set_on_rename(self.enable_rename)

        self.mouse_menu_exp_bg = MouseMenuExplorerBackground()
        self.mouse_menu_exp_bg.set_on_new_folder(self.new_folder)
        self.mouse_menu_exp_bg.set_on_paste(self.paste_to_curr_dir)



        # self.selection_area_visual = SelectionAreaVisual()
        # from custom_controls.selection_area import SelectionArea
        # self.selection_area_visual = SelectionArea().selection_area_visual

        self.overlay = [self.mouse_menu_exp_elem, self.mouse_menu_exp_bg]#, self.selection_area_visual]

        self.clipboard : DirectoryTreeElement|None = None
        self.has_cut = False

        self.currently_dragged = None
        self.currently_hovered = None
        self.assigned_to_menu = None

        self.refresh()

    def on_go_back(self, e):
        if self.dir_tree.current_node.parent is not None:
            self.dir_tree.go_to_parent()
            self.refresh()
            self.update()


    def paste_to_curr_dir(self, _e):
        if self.clipboard is None:
            return
        self.clipboard.name = self.make_copy_name(self.dir_tree.current_node, self.clipboard.name)
        self.dir_tree.insert_node(self.dir_tree.current_node,self.clipboard)
        print("pasted:",self.clipboard.name, " to: ",  self.dir_tree.current_node.name)
        if self.clipboard.is_cut:
            self.dir_tree.remove_node(self.clipboard.name)
        self.clipboard = None
        self.mouse_menu_exp_elem.hide()
        self.refresh()
        self.update()


    def new_folder(self, e):
        new_folder = DirectoryTreeElement(name="New Folder",
                                          file_type=FileTypes.DIRECTORY,
                                          path=self.dir_tree.current_node.path,
                                          depth=self.dir_tree.current_node.depth+1)
        new_folder.name = self.make_copy_name(self.dir_tree.current_node, new_folder.name)
        self.dir_tree.insert_node_into_parent(self.dir_tree.current_node,new_folder)
        self.refresh()
        self.update()
        new_folder.exp_elem.enable_label_edit(
            lambda _e,nN, oN: self.on_new_dir_rename_submit(new_folder, _e, nN, oN))
        new_folder.exp_elem.update()



    def cut_element(self, e):
        print("cut: ", e.control.file.name)
        if self.clipboard is not None:
            self.clipboard.switch_to_default_mode()
        self.clipboard = e.control.file
        self.clipboard.switch_to_cut_mode()
        self.mouse_menu_exp_elem.hide()
        self.update()

    def copy_element(self, e):
        print("copied: ", e.control.file.name)
        if self.clipboard is not None:
            self.clipboard.switch_to_default_mode()
        file = e.control.file
        self.clipboard = self.dir_tree.copy_node(file.name)
        self.mouse_menu_exp_elem.hide()

    def paste_elem_to_child_dir(self, e):
        file = e.control.file
        if (file == self.clipboard or self.clipboard is None or file.file_type != FileTypes.DIRECTORY):
            return
        if self.clipboard.is_cut:
            self.dir_tree.remove_node_of_parent(self.clipboard.parent, self.clipboard.name)
        self.clipboard.name = self.make_copy_name(file, self.clipboard.name)
        self.dir_tree.insert_node(file.name,self.clipboard)
        print("pasted:",self.clipboard.name, " to: ",  file.name)
        self.clipboard = None
        self.mouse_menu_exp_elem.hide()
        self.refresh()
        self.update()

    def on_new_dir_rename_submit(self, file: DirectoryTreeElement, _e, new_name, old_name):
        print("renamed from: ", old_name, " to: ", new_name)
        if new_name != old_name:
            new_name = self.make_copy_name(self.dir_tree.current_node, new_name)
            file.name = new_name
        file.exp_elem.disable_label_edit()
        self.refresh()
        self.update()

    def enable_rename(self, e):
        print("rename: ", e.control.file.name)
        elem: ExplorerElement = e.control.file.exp_elem
        elem.enable_label_edit(self.on_rename_submit)
        self.mouse_menu_exp_elem.hide()


    def on_rename_submit(self, e, new_name, old_name):
        print(e.control)
        print("renamed to: ", e.control.value)
        elem: ExplorerElement = self.find_file_exp_elem(self.mouse_menu_exp_elem.data)
        if new_name != old_name:
            new_name = self.make_copy_name(self.dir_tree.current_node, new_name)
            self.dir_tree.find_child(old_name).name = new_name
            elem.file.name = new_name
        elem.disable_label_edit()
        self.refresh()
        self.update()

    def open_element(self, e):
        file:DirectoryTreeElement = e.control.data
        if file.file_type == FileTypes.DIRECTORY:
            self.dir_tree.go_to_child(file.name)
            self.mouse_menu_exp_elem.hide()
            self.refresh()
            self.update()

    def on_successful_drag(self, dragged_file, target_file):
        if self.clipboard is not None and self.clipboard.name == dragged_file.name and self.clipboard.depth == dragged_file.depth:
            self.clipboard = None
        if target_file.name == dragged_file.name:
            return
        copy = self.dir_tree.copy_node(dragged_file.name)
        copy.name = self.make_copy_name(target_file, copy.name)
        self.dir_tree.insert_node(target_file.name, copy)
        self.dir_tree.remove_node(dragged_file.name)
        self.refresh()
        self.update()

    def make_copy_name(self, new_dir, curr_name):
        i = 0
        new_name = curr_name
        while new_dir.has_child(new_name):
            i += 1
            new_name = curr_name + "(" + str(i) + ")"
        return new_name

    def is_file_name_unique(self, name):
        return not self.dir_tree.current_node.has_child(name)

    def mk_file_button(self, file:DirectoryTreeElement):

        element = ExplorerElement(file, icon_size=self.icon_size)

        element.button_gestured.icon_button.on_click = self.open_element
        element.button_gestured.set_on_secondary_tap(lambda e: print("Right clicked"))

        def on_rigt_click(e, f=file):
            print("Right clicked")
            x,y = calc_click_pos(e.control.page.width, e.control.page.height, "counter")
            self.mouse_menu_exp_elem.data = f
            self.mouse_menu_exp_elem.show_at(x, y)
            #self.assigned_to_menu = f

        element.button_gestured.gesture.on_secondary_tap = on_rigt_click

        def log_me_dragged(_e):
            print("Dragged: ", file.name)
            self.currently_dragged = file


        def on_drag_targeted(_e):
            print("Accepted drag into: ", file.name)
            print("Currently dragged: ", self.currently_dragged.name)
            if self.currently_dragged is not None:
                self.on_successful_drag(self.currently_dragged, file)

        element.draggable.on_drag_start = log_me_dragged

        if element.drag_target is not None:
            element.drag_target.on_accept = on_drag_targeted

        def on_enter(e):
            #print("Entered: ", file.name)
            self.currently_hovered = file

        def on_exit(e):
            #print("Left: ", file.name)
            self.currently_hovered = None

        element.button_gestured.gesture.on_enter = on_enter
        element.button_gestured.gesture.on_exit = on_exit

        #element.drag_target.on_move = lambda e: print("Will accept")

        file.exp_elem = element



        return element


    def mk_row(self, files):
        row = ft.Row()
        for file in files:
            row.controls.append(self.mk_file_button(file))
        return row

    def mk_grid(self):
        curr_node_children = self.dir_tree.current_node.children
        files_cnt =  len(curr_node_children)
        rows_cnt = files_cnt // self.elems_pr_row
        controls = []
        if files_cnt % self.elems_pr_row != 0:
            rows_cnt += 1
        for i in range(0, rows_cnt):
            controls.append(self.mk_row(curr_node_children[i*self.elems_pr_row:(i+1)*self.elems_pr_row]))

        self.grid = ft.Column(controls, alignment=ft.MainAxisAlignment.CENTER)
        # self.grid.width = self.rows*self.icon_size
        # self.grid.height = self.cols*self.icon_size

        self.background_gesture = ft.GestureDetector(content=self.grid)


        #self.selection_area = ft.SelectionArea(content=self.grid, on_change= lambda x: print("Selection area changed"))

        # stack = ft.Stack(clip_behavior=ft.ClipBehavior.NONE) #
        # stack.controls = [ft.TransparentPointer(self.selection_area), ft.TransparentPointer(self.background_gesture)]

        def on_rigt_click(e):
            print("Right clicked")
            x, y = calc_click_pos(e.control.page.width, e.control.page.height, "counter")
            self.mouse_menu_exp_bg.show_at(x, y)
            # self.assigned_to_menu = f
        self.background_gesture.on_secondary_tap = on_rigt_click
        self.background_gesture.on_tap = lambda _e: self.mouse_menu_exp_bg.hide()

        #self.background_gesture.on_tap = self.hide_mouse_file_menu

        # self.background_gesture.on_pan_start = self.show_selection_area
        # self.background_gesture.on_pan_end = self.hide_selection_area
        # self.background_gesture.on_pan_update = self.update_selection_area

        return  self.background_gesture

    def mk_top_menu(self):
        back_button = ft.IconButton(icon = ft.icons.ARROW_BACK,
                                    icon_size=15,
                                    padding=ft.Padding(0, 0, 0, 0),
                                    on_click=self.on_go_back)
        self.top_menu_txt = ft.TextField(
            value=self.dir_tree.current_node.path,
            width=self.top_menu_size,
            content_padding=ft.Padding(0, 0, 0, 0),
            prefix=back_button,
        )
        return ft.Row([self.top_menu_txt])

    from flet_core import DragStartEvent, DragEndEvent, DragUpdateEvent

    def update_selection_area(self,e:DragUpdateEvent):
        # print("local x: ",e.local_x)
        # print("local y: ",e.local_y)
        self.selection_area_visual.on_change((e.global_x, e.global_y))

    def show_selection_area(self, e:DragStartEvent):
        #print("local x: ",e.local_x)
        #print("local y: ",e.local_y)

        #print("show_selection_area")
        self.selection_area_visual.show(e.local_x, e.local_y)

    def hide_selection_area(self, e):
        #print("hide_selection_area")
        self.selection_area_visual.hide()


    def hide_mouse_file_menu(self,_e):
        self.mouse_menu_exp_elem.hide()

    def update_top_menu_txt(self):
        self.top_menu_txt.value = self.dir_tree.current_node.path



    def delete_element(self, e):
        print(e.control.file)
        self.dir_tree.remove_node(e.control.file.name)
        self.refresh()
        self.update()


    def refresh(self):
        self.controls = self.controls[:1]
        self.update_top_menu_txt()
        self.controls.append(self.mk_grid())

    def find_file_exp_elem(self, file:DirectoryTreeElement):
        for row in self.controls[1].content.controls:
                for elem in row.controls:
                    if elem.file.name == file.name and elem.file.depth == file.depth:
                        return elem
        return None