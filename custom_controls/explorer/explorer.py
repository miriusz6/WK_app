import flet as ft
from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement, FileTypes
from custom_controls.mouse_menu import MouseMenuExplorerElement, MouseMenuExplorerBackground
from custom_controls.explorer.explorer_element import ExplorerElement
from flet_core import DragStartEvent
from flet_core.drag_target import DragTargetEvent

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
        self.mouse_menu_exp_elem.set_on_open(self.open_button_clicked)
        self.mouse_menu_exp_elem.set_on_delete(self.delete_button_clicked)
        self.mouse_menu_exp_elem.set_on_copy(self.copy_button_clicked)
        self.mouse_menu_exp_elem.set_on_paste(self.paste_into_button_clicked)
        self.mouse_menu_exp_elem.set_on_cut(self.cut_button_clicked)
        self.mouse_menu_exp_elem.set_on_rename_enable(self.rename_button_clicked)

        self.mouse_menu_exp_bg = MouseMenuExplorerBackground()
        self.mouse_menu_exp_bg.set_on_new_folder(self.new_folder_button_clicked)
        self.mouse_menu_exp_bg.set_on_paste(self.paste_here_button_clicked)

        self.overlay = [self.mouse_menu_exp_elem, self.mouse_menu_exp_bg]

        self.clipboard: DirectoryTreeElement| None = None
        self.has_cut = False
        self.bg_menu_blocked = False
        self.file_menu_blocked = False




        self.refresh()

    # Element manipulation
    def move_to_parent_dir(self, e):
        if self.dir_tree.current_node.parent is not None:
            self.dir_tree.go_to_parent()
            self.refresh()
            self.update()

    def create_new_folder_element(self):
        new_folder = DirectoryTreeElement(name="New Folder",
                                          file_type=FileTypes.DIRECTORY,
                                          path=self.dir_tree.current_node.path,
                                          depth=self.dir_tree.current_node.depth+1)
        new_folder.name = self.make_copy_name(self.dir_tree.current_node, new_folder.name)
        self.dir_tree.insert_node_into_parent(self.dir_tree.current_node,new_folder)
        self.refresh()
        self.update()
        # new_folder.exp_elem.enable_label_edit(
        #     lambda _e,nN, oN: self.on_new_dir_rename_submit(new_folder, _e, nN, oN))
        # new_folder.exp_elem.update()

    def enable_rename(self, file: DirectoryTreeElement):
        file.exp_elem.enable_name_edit()
        self.mouse_menu_exp_elem.hide()

    def rename_element(self, file: DirectoryTreeElement, new_name):
        file.name = new_name
        self.refresh()
        self.update()

    def delete_element(self, file: DirectoryTreeElement):
        self.dir_tree.remove_node(file.name)
        self.refresh()
        self.update()

    def open_element(self, file: DirectoryTreeElement):
        if file.file_type == FileTypes.DIRECTORY:
            self.dir_tree.go_to_child(file.name)
            self.refresh()
            self.update()

    def cut_element(self, file: DirectoryTreeElement):
        if self.clipboard is not None:
            self.clipboard.switch_to_default_mode()
        self.clipboard = file
        self.clipboard.switch_to_cut_mode()
        self.mouse_menu_exp_elem.hide()
        self.update()

    def copy_element(self, file: DirectoryTreeElement):
        if self.clipboard is not None:
            self.clipboard.switch_to_default_mode()
        self.clipboard = self.dir_tree.copy_node(file.name)
        self.mouse_menu_exp_elem.hide()

    def paste_to_curr_dir(self, _e):
        if self.clipboard is None:
            return
        if self.clipboard.is_cut:
            self.dir_tree.remove_node_of_parent(self.clipboard.parent, self.clipboard.name)

        self.clipboard.name = self.make_copy_name(self.dir_tree.current_node, self.clipboard.name)
        self.dir_tree.insert_node(self.dir_tree.current_node.name,self.clipboard)
        print("pasted:",self.clipboard.name, " to: ",  self.dir_tree.current_node.name)

        self.clipboard = None
        self.mouse_menu_exp_elem.hide()
        self.refresh()
        self.update()

    def paste_elem_to_child_dir(self, file: DirectoryTreeElement):
        if (self.clipboard is None
                or  file == self.clipboard
                or file.file_type != FileTypes.DIRECTORY):
            return
        if self.clipboard.is_cut:
            self.dir_tree.remove_node_of_parent(self.clipboard.parent, self.clipboard.name)
        self.clipboard.name = self.make_copy_name(file, self.clipboard.name)
        self.dir_tree.insert_node(file.name,self.clipboard)
        self.clipboard = None
        self.mouse_menu_exp_elem.hide()
        self.refresh()
        self.update()
    # Element manipulation end

    # Mouse background menu events
    def paste_here_button_clicked(self, e):
        self.paste_to_curr_dir(e)
        self.mouse_menu_exp_bg.hide()

    def new_folder_button_clicked(self, e):
        self.create_new_folder_element()
        self.mouse_menu_exp_bg.hide()

    # Mouse background menu events end

    # Mouse element menu events
    def open_button_clicked(self, e):
        self.open_element(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def copy_button_clicked(self, e):
        self.copy_element(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def cut_button_clicked(self, e):
        self.cut_element(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def delete_button_clicked(self, e):
        self.delete_element(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def paste_into_button_clicked(self, e):
        self.paste_elem_to_child_dir(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def rename_button_clicked(self, e):
        self.enable_rename(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()
    # Mouse element menu events end

    # Element events
    def element_name_changed(self, file:DirectoryTreeElement):
        new_name = file.exp_elem.name
        file.exp_elem.disable_name_edit()
        if new_name == "" or new_name == file.name:
            return
        self.rename_element(file, self.make_copy_name(self.dir_tree.current_node, new_name))

    def element_right_clicked(self, e:ft.TapEvent, file:DirectoryTreeElement):
        self.mouse_menu_exp_elem.data = file
        self.show_mouse_exp_menu(e.global_x, e.global_y)

    def element_left_clicked(self, _e:ft.TapEvent, file:DirectoryTreeElement):
        self.open_element(file)

    def element_dragged(self, e:DragStartEvent, file:DirectoryTreeElement):
        self.currently_dragged = file
        pass

    def element_dragged_at(self, e:DragTargetEvent, target_file:DirectoryTreeElement):
        if self.currently_dragged is None:
            return
        dragged_file = self.currently_dragged
        if (self.clipboard is not None and
                self.clipboard.name == dragged_file.name and
                self.clipboard.depth == dragged_file.depth):
            self.clipboard = None
        if target_file.name == dragged_file.name:
            return
        copy = self.dir_tree.copy_node(dragged_file.name)
        copy.name = self.make_copy_name(target_file, copy.name)
        self.dir_tree.insert_node(target_file.name, copy)
        self.dir_tree.remove_node(dragged_file.name)
        self.refresh()
        self.update()

    def element_hovered(self, e:ft.HoverEvent, file:DirectoryTreeElement):
        self.bg_menu_blocked = True
        self.file_menu_blocked = False

    def element_hover_stopped(self, e:ft.HoverEvent, file:DirectoryTreeElement):
        self.bg_menu_blocked = False
        self.file_menu_blocked = True

    # Element events end

    # Explorer layout
    def refresh(self):
        self.controls = self.controls[:1]
        self.update_top_menu_txt()
        self.controls.append(self.mk_grid())

    def mk_file_button(self, file:DirectoryTreeElement):

        element = ExplorerElement(file, icon_size=self.icon_size)
        element.on_new_name_submit =  lambda e: self.element_name_changed(file)
        element.button_labeled.button.on_click = lambda e: self.element_left_clicked(e, file)
        element.gesture.on_secondary_tap_down = lambda e: self.element_right_clicked(e, file)
        element.draggable.on_drag_start = lambda e: self.element_dragged(e, file)
        element.button_labeled.gesture.on_enter = lambda e: self.element_hovered(e, file)
        element.button_labeled.gesture.on_exit = lambda e: self.element_hover_stopped(e, file)
        if element.drag_target is not None:
            element.drag_target.on_accept = lambda e: self.element_dragged_at(e, file)
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


        self.background_gesture = ft.GestureDetector(content=self.grid)

        def on_rigt_click(e:ft.TapEvent):
            self.show_mouse_exp_bg(e.global_x, e.global_y)

        self.background_gesture.on_secondary_tap_down = on_rigt_click
        self.background_gesture.on_tap_down = lambda _e: self.hide_mouse_menus()

        # self.background_gesture.on_pan_start = self.show_selection_area
        # self.background_gesture.on_pan_end = self.hide_selection_area
        # self.background_gesture.on_pan_update = self.update_selection_area

        return  self.background_gesture

    def mk_top_menu(self):
        back_button = ft.IconButton(icon = ft.icons.ARROW_BACK,
                                    icon_size=15,
                                    padding=ft.Padding(0, 0, 0, 0),
                                    on_click=self.move_to_parent_dir)
        self.top_menu_txt = ft.TextField(
            value=self.dir_tree.current_node.path,
            width=self.top_menu_size,
            content_padding=ft.Padding(0, 0, 0, 0),
            prefix=back_button,
        )
        return ft.Row([self.top_menu_txt])
    # Explorer layout end

    # Mouse menus manipulation
    def show_mouse_exp_menu(self, x, y):
        if self.file_menu_blocked:
            return
        self.mouse_menu_exp_bg.hide()
        self.mouse_menu_exp_elem.show_at(x, y)

    def show_mouse_exp_bg(self, x, y):
        if self.bg_menu_blocked:
            return
        self.mouse_menu_exp_elem.hide()
        self.mouse_menu_exp_bg.show_at(x, y)

    def hide_mouse_menus(self):
        self.mouse_menu_exp_elem.hide()
        self.mouse_menu_exp_bg.hide()
    # Mouse menus manipulation end

    def update_top_menu_txt(self):
        self.top_menu_txt.value = self.dir_tree.current_node.path

    def make_copy_name(self, new_dir, curr_name):
        i = 0
        new_name = curr_name
        while new_dir.has_child(new_name):
            i += 1
            new_name = curr_name + "(" + str(i) + ")"
        return new_name



