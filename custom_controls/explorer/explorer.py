import flet as ft
from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement, FileTypes
from custom_controls.mouse_menu import MouseMenuExplorerElement, MouseMenuExplorerBackground
from custom_controls.explorer.explorer_element import ExplorerElement
from flet_core import DragStartEvent
from flet_core.drag_target import DragTargetEvent

class Explorer(ft.Column):
    def __init__(self, root_path, elems_pr_row = 5, **kwargs):
        super().__init__(**kwargs)
        self.root_path = root_path

        self.grid: ft.Column
        self.icon_size = 200
        self.elems_pr_row = elems_pr_row

        self.top_menu: ft.Row
        self.top_menu_size = self.icon_size * self.elems_pr_row
        self.top_menu_txt: ft.TextField
        self.search_enabled = False
        self.searching = False

        self.overlay: list[ft.Control]
        self.mouse_menu_exp_elem: MouseMenuExplorerElement
        self.mouse_menu_exp_bg: MouseMenuExplorerBackground
        self.bg_unreachable = False
        self.bg_reachable = False

        self.main_dir_tree: DirectoryTree
        self.curr_dir_tree: DirectoryTree
        self.search_dir_tree: DirectoryTree

        self.clipboard: list[DirectoryTreeElement] = []
        self.selected: list[DirectoryTreeElement] = []
        self.has_cut = False

        self.explorer_controls = []
        #self.explorer_overlay:

        self.init_explorer()

    # Element manipulation
    def highlight_element_names(self, files: list[DirectoryTreeElement]):
        for file in files:
            file.exp_elem.label.highlight_all()

    def highlight_fraze_in_element_names(self, files: list[DirectoryTreeElement],
                                     fraze: str):
        try:
            for file in files:
                file.exp_elem.label.highlight(fraze)
        except:
            print("smths wrong")

    def unhighlight_element_names(self, files: list[DirectoryTreeElement]):
        for file in files:
            file.exp_elem.label.unhighlight_all()


    def select_element(self, file: DirectoryTreeElement):
        file.switch_to_selected_mode()
        self.selected.append(file)
        self.update()

    def unselect_element(self, file: DirectoryTreeElement):
        file.switch_to_default_mode()
        self.selected.remove(file)
        self.update()

    def unselect_all(self):
        for file in self.selected:
            file.switch_to_default_mode()
        self.selected = []
        self.update()


    def move_to_parent_dir(self, e):
        if self.curr_dir_tree.current_node.parent is not None:
            self.curr_dir_tree.go_to_parent()
            self.refresh()
            self.update()

    def create_new_folder_element(self):
        new_folder = DirectoryTreeElement(name="New Folder",
                                          file_type=FileTypes.DIRECTORY,
                                          path=self.curr_dir_tree.current_node.path,
                                          depth=self.curr_dir_tree.current_node.depth + 1)
        new_folder.name = self.make_copy_name(self.curr_dir_tree.current_node, new_folder.name)
        self.curr_dir_tree.insert_node_into_parent(self.curr_dir_tree.current_node, new_folder)
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

    def delete_elements(self, files: list[DirectoryTreeElement]):
        for f in files:
            self.curr_dir_tree.remove_node(f.name)
        self.refresh()
        self.update()

    def open_element(self, file: DirectoryTreeElement):
        if file.file_type == FileTypes.DIRECTORY:
            self.curr_dir_tree.go_to_child(file.name)
            self.refresh()
            self.update()

    def cut_elements(self, files: list[DirectoryTreeElement]):
        if self.clipboard_empty():
            for f in self.clipboard: f.switch_to_default_mode()
        for f in files:
            self.clipboard.append(f)
            f.switch_to_cut_mode()
        self.mouse_menu_exp_elem.hide()
        self.update()

    def copy_elements(self, files: list[DirectoryTreeElement]):
        if not self.clipboard_empty():
            for f in self.clipboard: f.switch_to_default_mode()
        for f in files:
            self.clipboard.append(self.curr_dir_tree.copy_node(f.name))
        self.mouse_menu_exp_elem.hide()

    def paste_to_curr_dir(self, _e):
        if self.clipboard_empty():
            return
        #if self.clipboard.is_cut:
        for f in self.clipboard:
            if f.parent.name == self.curr_dir_tree.current_node.name:
                continue
            new_name = self.make_copy_name(self.curr_dir_tree.current_node, f.name)
            self.curr_dir_tree.remove_node_of_parent(f.parent, f.name)
            f.name = new_name
            self.curr_dir_tree.insert_node(self.curr_dir_tree.current_node.name, f)
        print("pasted:", self.clipboard, " to: ", self.curr_dir_tree.current_node.name)
        self.clipboard = []
        self.mouse_menu_exp_elem.hide()
        self.refresh()
        self.update()

    def paste_elem_to_child_dir(self, new_parent_file: DirectoryTreeElement):
        a = self.clipboard_empty()
        b = new_parent_file in self.clipboard
        c = new_parent_file.file_type != FileTypes.DIRECTORY
        if (self.clipboard_empty()
                or new_parent_file in self.clipboard
                or new_parent_file.file_type != FileTypes.DIRECTORY):
            return
        for f in self.clipboard:
            if f.parent.name == new_parent_file.name:
                continue
            new_name = self.make_copy_name(new_parent_file, f.name)
            self.curr_dir_tree.remove_node_of_parent(f.parent, f.name)
            f.name = new_name
            self.curr_dir_tree.insert_node(new_parent_file.name, f)
        self.clipboard = []
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

    def select_all_button_clicked(self, e):
        for f in self.curr_dir_tree.current_node.children:
            self.select_element(f)
        self.mouse_menu_exp_bg.hide()

    # Mouse background menu events end

    # Mouse element menu events
    def open_button_clicked(self, e):
        self.open_element(self.mouse_menu_exp_elem.data)
        self.mouse_menu_exp_elem.hide()

    def copy_button_clicked(self, e):
        self.copy_elements(self.selected)
        self.mouse_menu_exp_elem.hide()

    def cut_button_clicked(self, e):
        self.cut_elements(self.selected)
        self.mouse_menu_exp_elem.hide()

    def delete_button_clicked(self, e):
        self.delete_elements(self.selected)
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
        self.rename_element(file, self.make_copy_name(self.curr_dir_tree.current_node, new_name))

    def element_right_clicked(self, e:ft.TapEvent, file:DirectoryTreeElement):
        self.mouse_menu_exp_elem.data = file
        if file.is_selected:
            self.show_mouse_exp_menu(e.global_x, e.global_y)
        else:
            self.unselect_all()

    def element_double_clicked(self, _e:ft.TapEvent, file:DirectoryTreeElement):
        self.open_element(file)

    def element_left_clicked(self, e:ft.TapEvent, file:DirectoryTreeElement):
        if file.is_selected:
            self.unselect_element(file)
        else:
            self.select_element(file)

    def element_dragged(self, e:DragStartEvent, file:DirectoryTreeElement):
        self.currently_dragged = file
        pass

    def element_dragged_at(self, e:DragTargetEvent, target_file:DirectoryTreeElement):
        dragged_file = self.currently_dragged
        if dragged_file.name == target_file.name:
            return
        self.curr_dir_tree.insert_node(target_file.name, dragged_file)
        self.curr_dir_tree.remove_node(dragged_file.name)
        self.refresh()
        self.update()

    def element_hovered(self, e:ft.HoverEvent, file:DirectoryTreeElement):
        self.bg_unreachable = True
        self.bg_reachable = False

    def element_hover_stopped(self, e:ft.HoverEvent, file:DirectoryTreeElement):
        self.bg_unreachable = False
        self.bg_reachable = True

    # Element events end

    def background_left_clicked(self, e:ft.TapEvent):
        if self.bg_unreachable: return
        self.hide_mouse_menus()
        self.unselect_all()

    def background_right_clicked(self, e: ft.TapEvent):
        if self.bg_unreachable: return
        self.show_mouse_exp_bg(e.global_x, e.global_y)
        self.unselect_all()

    def init_top_menu(self):
        self.top_menu = self.mk_top_menu()
        self.top_menu_search_button.on_click = self.search_button_clicked
        self.top_menu_search_cancel_button.on_click = self.search_cancel_button_clicked

    def init_bg_mouse_menu(self):
        self.mouse_menu_exp_bg = MouseMenuExplorerBackground()
        self.mouse_menu_exp_bg.set_on_new_folder(self.new_folder_button_clicked)
        self.mouse_menu_exp_bg.set_on_paste(self.paste_here_button_clicked)
        self.mouse_menu_exp_bg.set_on_select_all(self.select_all_button_clicked)

    def init_file_mouse_menu(self):
        self.mouse_menu_exp_elem = MouseMenuExplorerElement()
        self.mouse_menu_exp_elem.set_on_open(self.open_button_clicked)
        self.mouse_menu_exp_elem.set_on_delete(self.delete_button_clicked)
        self.mouse_menu_exp_elem.set_on_copy(self.copy_button_clicked)
        self.mouse_menu_exp_elem.set_on_paste(self.paste_into_button_clicked)
        self.mouse_menu_exp_elem.set_on_cut(self.cut_button_clicked)
        self.mouse_menu_exp_elem.set_on_rename_enable(self.rename_button_clicked)

    def init_explorer(self):
        self.main_dir_tree: DirectoryTree = DirectoryTree(self.root_path)
        self.curr_dir_tree: DirectoryTree = self.main_dir_tree
        self.search_dir_tree: DirectoryTree = self.initialize_search_tree()
        self.init_bg_mouse_menu()
        self.init_file_mouse_menu()
        self.init_top_menu()
        self.overlay = [self.mouse_menu_exp_elem, self.mouse_menu_exp_bg]
        self.controls.append(self.top_menu)
        self.controls.append(self.mk_grid())

    # Explorer layout
    def refresh(self):
        self.unselect_all()
        self.controls = self.controls[:1]
        self.update_top_menu_txt()
        self.controls.append(self.mk_grid())


    def mk_file_button(self, file:DirectoryTreeElement):
        element = ExplorerElement(file, icon_size=self.icon_size)
        element.on_new_name_submit =  lambda e: self.element_name_changed(file)
        element.gesture.on_double_tap = lambda e: self.element_double_clicked(e, file)
        element.gesture.on_tap = lambda e: self.element_left_clicked(e, file)
        element.gesture.on_secondary_tap_down = lambda e: self.element_right_clicked(e, file)
        element.draggable.on_drag_start = lambda e: self.element_dragged(e, file)
        element.gesture.on_enter = lambda e: self.element_hovered(e, file)
        element.gesture.on_exit = lambda e: self.element_hover_stopped(e, file)
        if element.drag_target is not None:
            element.drag_target.on_accept = lambda e: self.element_dragged_at(e, file)
        file.exp_elem = element
        return element

    def mk_row(self, files):
        row = ft.Row()
        for file in files:
            row.controls.append(self.mk_file_button(file))
        return row

    def insert_grid (self, grid:ft.Column):
        self.background_gesture.content = grid


    def mk_grid(self):
        curr_node_children = self.curr_dir_tree.current_node.children
        files_cnt =  len(curr_node_children)
        rows_cnt = files_cnt // self.elems_pr_row
        controls = []
        if files_cnt % self.elems_pr_row != 0:
            rows_cnt += 1
        for i in range(0, rows_cnt):
            controls.append(self.mk_row(curr_node_children[i*self.elems_pr_row:(i+1)*self.elems_pr_row]))

        self.grid = ft.Column(controls, alignment=ft.MainAxisAlignment.CENTER)


        self.background_gesture = ft.GestureDetector(content=self.grid)



        self.background_gesture.on_secondary_tap_down = self.background_right_clicked
        self.background_gesture.on_tap_down = self.background_left_clicked
        self.background_gesture.mouse_cursor = ft.MouseCursor.HELP


        return  self.background_gesture

    def mk_top_menu(self):

        back_button = ft.IconButton(icon = ft.icons.ARROW_BACK,
                                    icon_size=15,
                                    padding=ft.Padding(0, 0, 0, 0),
                                    on_click=self.move_to_parent_dir)
        self.top_menu_txt = ft.TextField(
            value=self.curr_dir_tree.current_node.path,
            width=self.top_menu_size,
            content_padding=ft.Padding(0, 0, 0, 0),
            prefix=back_button,
        )

        self.top_menu_search_cancel_button = ft.IconButton(icon=ft.icons.CANCEL,
                                                           icon_size=20,
                                                           icon_color="red")
        self.top_menu_search_button = ft.IconButton(icon=ft.icons.SEARCH,
                                                    icon_size=20,
                                                    on_click=self.search_button_clicked)

        self.top_menu_search_bar = ft.TextField(
            label = "Search:",
            value="",
            width=300,
            content_padding=ft.Padding(0, 0, 0, 0),
            prefix= self.top_menu_search_button,
            suffix= self.top_menu_search_cancel_button

        )

        return ft.Row([self.top_menu_txt, self.top_menu_search_bar])
    # Explorer layout end

    # Mouse menus manipulation
    def show_mouse_exp_menu(self, x, y):
        if self.bg_reachable:
            return
        self.mouse_menu_exp_bg.hide()
        self.mouse_menu_exp_elem.show_at(x, y)

    def show_mouse_exp_bg(self, x, y):
        if self.bg_unreachable:
            return
        self.mouse_menu_exp_elem.hide()
        self.mouse_menu_exp_bg.show_at(x, y)

    def hide_mouse_menus(self):
        self.mouse_menu_exp_elem.hide()
        self.mouse_menu_exp_bg.hide()
    # Mouse menus manipulation end

    def update_top_menu_txt(self):
        self.top_menu_txt.value = self.curr_dir_tree.current_node.path

    def make_copy_name(self, new_dir, curr_name):
        i = 0
        new_name = curr_name
        while new_dir.has_child(new_name):
            i += 1
            new_name = curr_name + "(" + str(i) + ")"
        return new_name

    def clipboard_empty(self):
        return len(self.clipboard) == 0

    def search_files(self, parent_file: DirectoryTreeElement,
                     search_str:str):
        matching_files = []
        for file in parent_file.children:
            if search_str.lower() in file.name.lower():
                #print("hit:", file.name)
                matching_files.append(file)
            matching_files = matching_files + self.search_files(file, search_str)
        return matching_files

    def initialize_search_tree(self):
        search_tree_root = DirectoryTreeElement(name="Search Results",
                                                file_type=FileTypes.DIRECTORY,
                                                path="Search Results",
                                                depth=0)

        return DirectoryTree(root_file=search_tree_root)

    def populate_search_tree(self, found_files: list[DirectoryTreeElement]):
        files = [self.main_dir_tree.copy_node_of_parent(f.parent,f.name) for f in found_files]

        self.search_dir_tree = self.initialize_search_tree()
        for f in files:
            f.data["org_path"] = f.path
            self.search_dir_tree.insert_node("Search Results", f)
        self.curr_dir_tree.go_to_root()


    # Top menu events
    def search_button_clicked(self, _e):
        if self.searching: return
        print("STARTED SEARCH")
        self.searching = True

        search_fraze = self.top_menu_search_bar.value
        if search_fraze == "":
            self.search_cancel_button_clicked(_e)
            self.searching = False
            return
        found_files = self.search_files(self.main_dir_tree.current_node, search_fraze)
        self.search_dir_tree = self.initialize_search_tree()
        self.populate_search_tree(found_files)
        self.curr_dir_tree = self.search_dir_tree
        self.refresh()
        self.highlight_fraze_in_element_names(
            self.curr_dir_tree.current_node.children,
            self.top_menu_search_bar.value)
        self.update()
        self.search_enabled = True
        self.searching = False
        print("FINISHED SEARCH")

    def search_cancel_button_clicked(self,_e):
        if self.searching: return
        self.search_enabled = False
        self.curr_dir_tree = self.main_dir_tree
        if self.search_dir_tree.current_node.depth != 0:
            self.curr_dir_tree.go_to_node(self.search_dir_tree.current_node.data["org_path"])
        #self.search_dir_tree = None
        self.top_menu_search_bar.value = ""
        self.refresh()
        self.update()
