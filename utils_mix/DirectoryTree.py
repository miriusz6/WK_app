import os

from enum import Enum

class FileTypes(Enum):
    TXT_FILE = 1
    DIRECTORY = 2


from custom_controls.explorer_element import ExplorerElement

class DirectoryTreeElement:
    def __init__(self, name, file_type, path, depth, extension=None, explorer_element:ExplorerElement = None):
        self.name = name
        self.children = []
        self.parent = None
        self.type = FileTypes.DIRECTORY
        self.extension = extension
        self.file_type = file_type
        self.path = path
        self.depth = depth
        self.exp_elem = explorer_element
        self.is_cut = False
        self.is_selected = False

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        child.depth = self.depth + 1
        child.path = os.path.join(self.path, child.name)
        self.fixup_paths()
        self.fixup_depth(self.depth)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def has_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return True
        return False

    def fixup_paths(self):
        for child in self.children:
            child.path = os.path.join(self.path, child.name)
            child.fixup_paths()

    def fixup_depth(self, depth):
        for child in self.children:
            child.fixup_depth(depth+1)

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None
        child.depth = None
        child.path = None

    def switch_to_cut_mode(self):
        self.is_cut = True
        self.is_selected = False
        self.exp_elem.cut()


    def switch_to_selected_mode(self):
        self.is_selected = True
        self.is_cut = False
        self.exp_elem.selected()


    def switch_to_default_mode(self):
        self.is_cut = False
        self.is_selected = False
        self.exp_elem.default()


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name







class DirectoryTree:
    def __init__(self, path_to_root):
        self.__populate_tree(path_to_root)
        self.current_node = self.root

    def __populate_tree(self, root_path):
        self.root = DirectoryTreeElement(
            name=root_path.split('/')[-1],
            file_type=FileTypes.DIRECTORY,
            path=root_path,
            depth=0)
        self.__populate_node(self.root)

    def __populate_node(self, root_node):
        root_node.children = self.__make_children(root_node.path, root_node)
        for child in root_node.children:
            child.parent = root_node
            if child.file_type == FileTypes.DIRECTORY:
                self.__populate_node(child)

    def __make_children(self, root_path, root_node):
        ret = []
        for name in os.listdir(root_path):
            split = os.path.splitext(name)
            name = split[0]
            path = os.path.join(root_path, name)
            if os.path.isdir(path):
                ret.append(DirectoryTreeElement(name=name,
                                                file_type=FileTypes.DIRECTORY,
                                                path=path,
                                                depth=root_node.depth+1))
            else:
                ext = split[1]
                ret.append(DirectoryTreeElement(name=name,
                                                file_type=FileTypes.TXT_FILE,
                                                path=path,
                                                extension=ext,
                                                depth=root_node.depth+1))
        return ret

    def go_to_root(self):
        self.current_node = self.root
        return self.current_node

    def add_node(self, child:DirectoryTreeElement = None, child_name = None, file_type = None, extension=None, path=None):
        if child is None:
            child = DirectoryTreeElement(name=child_name,
                                         file_type=file_type,
                                         extension=extension,
                                         path=path,
                                         depth=self.current_node.depth + 1)
        else:
            child.depth = self.current_node.depth + 1
        child.parent = self.current_node
        self.current_node.add_child(child)
        return child

    def has_child(self, child_name):
        for child in self.current_node.children:
            if child.name == child_name:
                return True
        return False



    def move_child_to_another_child(self, to_be_moved_name, target_name):
        to_be_moved = self.remove_node(to_be_moved_name)
        self.go_to_child(target_name)
        self.add_node(to_be_moved)
        to_be_moved.depth = self.current_node.depth + 1
        self.go_to_parent()
        return to_be_moved

    def find_child(self, child_name):
        for child in self.current_node.children:
            if child.name == child_name:
                return child
        return None

    def __copy_node(self, child_name):
        child = self.find_child(child_name)
        if child is None: return None
        copy = DirectoryTreeElement(name=child.name,
                                    file_type=child.file_type,
                                    extension=child.extension,
                                    path=child.path,
                                    depth=child.depth)
        return child,copy

    def find_child_of_parent(self, parent, child_name):
        for child in parent.children:
            if child.name == child_name:
                return child
        return None

    def __copy_child_of_parent(self, parent, child_name):
        child = self.find_child_of_parent(parent, child_name)
        if child is None: return None,None
        copy = DirectoryTreeElement(name=child.name,
                                    file_type=child.file_type,
                                    extension=child.extension,
                                    path=child.path,
                                    depth=child.depth)
        return child,copy

    def copy_node(self, child_name):
        def _copy_branch(parent, c_name):
            child, copy = self.__copy_child_of_parent(parent, c_name)
            if child is not None:
                for c in child.children:
                    copy.add_child(_copy_branch(child, c.name))
            return copy
        return _copy_branch(self.current_node, child_name)

    def remove_node(self, child_name):
        for child in self.current_node.children:
            if child.name == child_name:
                self.current_node.children.remove(child)
                return child
        return None

    def remove_node_of_parent(self,parent, child_name):
        for child in parent.children:
            if child.name == child_name:
                parent.children.remove(child)
                return child
        return None

    def insert_node_into_parent(self, parent, new_child):
        parent.add_child(new_child)
        return new_child

    def insert_node(self, new_parent_name, node_to_insert):
        if new_parent_name == self.current_node.name:
            self.insert_node_into_parent(self.current_node, node_to_insert)
        new_parent = self.find_child(new_parent_name)
        if new_parent is None:
            return None
        self.insert_node_into_parent(new_parent, node_to_insert)





    def go_to_child(self, child_name):
        for child in self.current_node.children:
            if child.name == child_name:
                self.current_node = child
                return child
        return None

    def go_to_parent(self):
        if self.current_node.parent is not None:
            self.current_node = self.current_node.parent
            return self.current_node
        return None

    def __str__(self):
        return self.current_node.name

    def __repr__(self):
        return self.current_node.name

    def __iter__(self):
        return self.current_node.children

    def print_tree(self, node = None, indent = 0):
        if node is None:
            node = self.root
        print("  "*indent, node)
        for child in node.children:
            self.print_tree(child, indent+2)

tree = DirectoryTree("C:/felt_WK_app/mockup_files")
tree.print_tree()
