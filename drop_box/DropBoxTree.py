import os
import re
from enum import Enum

import dropbox.files
from dropbox.files import FileMetadata, FolderMetadata, DeletedMetadata,Metadata
class FileTypes(Enum):
    FILE = 1
    DIRECTORY = 2



class DropBoxTreeElement:
    def __init__(self, name, file_type, path, depth,meta_data, extension=None):
        self.name = name
        self.meta_data = meta_data
        self.children = []
        self.parent = None
        self.type = FileTypes.DIRECTORY
        self.extension = extension
        self.file_type = file_type
        self.path = path
        self.depth = depth
        self.relative_path = path
        self.full_name = self.name
        # if self.extension is not None:
        #     self.full_name += self.extension
        self.full_path = self.path
        # if self.extension is not None:
        #     self.full_path += self.extension


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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name





class DropBoxTree:
    def __init__(self, files: list[Metadata]):
        files = [f for f in files if not isinstance(f, DeletedMetadata)]
        self.files = files.sort(key=lambda x: x.path_lower.count("/"))
        #self.files = files.sort(key=lambda x: x.path_lower)

        #self.populate_tree_w_extracted()
        #self.RET = self.smth(files)
        #self.__populate_tree(files)
        self.root = None
        self.levels = self.extract_levels(files)
        self.populate_tree_w_extracted()

        #self.current_node = self.root

    # def extract_levels(self, files: list[Metadata]):
    #     ret = {}
    #     for f in files:
    #         level = f.path_lower.count("/")
    #         if level not in ret:
    #             ret[level] = []
    #         ret[level].append(f)
    #     for k in ret.keys():
    #         ret[k].sort(key=lambda x: x.path_lower)
    #     return ret

    # def populate_tree_w_extracted(self):
    #     self.root = DropBoxTreeElement(name="root", file_type=FileTypes.DIRECTORY, path="", depth=0)
    #     self.current_node = self.root
    #     self.__populate_tree_w_extracted(self.current_node, self.levels[1])
    #
    #


    def mk_elem_of_metadata(self, f:Metadata, depth):
        if isinstance(f, FolderMetadata):
            return DropBoxTreeElement(
                name=os.path.split(f.path_lower)[1],
                file_type=FileTypes.DIRECTORY,
                path=f.path_lower,
                depth=depth,
                meta_data=f)
        elif isinstance(f, FileMetadata):
            return DropBoxTreeElement(
                name=os.path.split(f.path_lower)[1],
                file_type=FileTypes.FILE,
                path=f.path_lower,
                extension=f.name.split(".")[-1],
                depth=depth,
                meta_data=f)

    def populate_tree_w_extracted(self):
        self.root = list(self.levels[1].values())[0]

        for elem in list(self.levels[2].values()):
            self.root.add_child(elem)

        for i in range (3, len(self.levels.keys())+1):
            prev_level = self.levels[i-1]
            curr_level = self.levels[i]
            for (name,elem) in curr_level.items():
                parent_name = elem.path.split("/")[-2]
                parent = prev_level[parent_name]
                parent.add_child(elem)




    def extract_levels(self, files: list[Metadata]):
        ret = {}
        for f in files:
            split = f.path_lower.split("/")
            level = len(split)-1
            elem = self.mk_elem_of_metadata(f, depth = level-1)
            if level not in ret:
                ret[level] = {}
            if elem.name not in ret[level]:
                ret[level][elem.name] = elem
            ret[level][elem.name] = elem
        return ret









    # def extract_parent_dirs(self, files: list[Metadata]):
    #     ret = {}
    #     for f in files:
    #         split = f.path_lower.split("/")
    #         level = len(split)-1
    #         #parent = f.path_lower.split("/")[-2]
    #         parent = f
    #         if level not in ret:
    #             ret[level] = {}
    #         if "parent" not in ret[level]:
    #             ret[level]["parent"] = {parent}
    #             ret[level]["children"] = []
    #         ret[level]["children"].append(f)
    #     # for k in ret.keys():
    #     #     ret[k].sort(key=lambda x: x.path_lower)
    #     return ret

    #def print_extracted(self):

    #
    # def smth(self, levels):
    #     children = []
    #     new_level_start = 0
    #     for i in range(len(levels[1])):
    #         f = files[i]
    #         if f.path_lower.count("/") == 2:
    #             children.append({"file": f, "children":[]})
    #         else:
    #             new_level_start = i
    #             break
    #
    #     for child in children:
    #         if isinstance(child, dropbox.files.FileMetadata):
    #             continue
    #         child["children"] =  self._smth(files = files[new_level_start:],depth=3)
    #
    #     return  {"file":files[0], "children":children }
    #
    # def _smth(self, files: list[Metadata], depth):
    #     children = []
    #     new_level_start = 0
    #     for i in range (1,len(files)):
    #         f = files[i]
    #         if f.path_lower.count("/") == depth:
    #             children.append({"file": f, "children":[]})
    #         else:
    #             new_level_start = i
    #             break
    #
    #     for child in children:
    #         if isinstance(child, dropbox.files.FileMetadata):
    #             continue
    #         child["children"] =  self._smth(files = files[new_level_start:],depth=depth+1)
    #
    #     return children
    #
    #
    #
    # def __populate_tree(self, files: list[Metadata]):
    #     root_meta = files[0]
    #     self.root = DropBoxTreeElement(
    #         name= os.path.split(root_meta.path_lower)[1],
    #         file_type=FileTypes.DIRECTORY,
    #         path=root_meta.path_lower,
    #         depth=0)
    #     self.__populate_node(self.root, files[1:])
    #
    # def __populate_node(self, root_node, files: list[Metadata]):
    #     on_level = []
    #     start = -1
    #     end = -1
    #     for i in range(len(files)):
    #         file = files[i]
    #         slashes = file.path_lower.count("/")-1
    #         level = root_node.depth+1
    #         if root_node.path in file.path_lower:
    #             if slashes == level:
    #                 on_level.append(i)
    #             else:
    #                 end = i
    #             if start == -1:
    #                 start = i
    #         else:
    #             end = i
    #
    #     if start < 0: return
    #     if start > -1 and end < 0:
    #         end = len(files)
    #     on_level = [files.pop(i) for i in on_level]
    #     end -= len(on_level)
    #
    #
    #     for f in on_level:
    #         if root_node.path not in f.path_lower:
    #             break
    #         node_to_add = None
    #         if isinstance(f, FolderMetadata):
    #             node_to_add = DropBoxTreeElement(
    #                 name=os.path.split(f.path_lower)[1],
    #                 file_type=FileTypes.DIRECTORY,
    #                 path=f.path_lower,
    #                 depth=root_node.depth+1)
    #             self.__populate_node(node_to_add, files[start:end])
    #         elif isinstance(f, FileMetadata):
    #             node_to_add = DropBoxTreeElement(
    #                 name=os.path.split(f.path_lower)[1],
    #                 file_type=FileTypes.FILE,
    #                 path=f.path_lower,
    #                 extension=f.name.split(".")[-1],
    #                 depth=root_node.depth+1)
    #
    #         root_node.add_child(node_to_add)

    def go_to_root(self):
        self.current_node = self.root
        return self.current_node

    def add_node(self, child:DropBoxTreeElement = None, child_name = None, file_type = None, extension=None, path=None):
        if child is None:
            child = DropBoxTreeElement(name=child_name,
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
        copy = DropBoxTreeElement(name=child.name,
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
        copy = DropBoxTreeElement(name=child.name,
                                  file_type=child.file_type,
                                  extension=child.extension,
                                  path=child.path,
                                  depth=child.depth)
        copy.parent = parent
        return child,copy

    def copy_node_of_parent(self,parent, c_name):
        child, copy = self.__copy_child_of_parent(parent, c_name)
        if child is not None:
            for c in child.children:
                copy.add_child(self.copy_node_of_parent(child, c.name))
        copy.data["original"] = child
        return copy

    def copy_node(self, child_name):
        return self.copy_node_of_parent(self.current_node, child_name)

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

    def insert_node(self, new_parent_name:str, node_to_insert:DropBoxTreeElement):
        if new_parent_name == self.current_node.name:
            self.insert_node_into_parent(self.current_node, node_to_insert)
            return
        new_parent = self.find_child(new_parent_name)
        if new_parent is None:
            return None



    def find_node(self, path):
        pointer = self.root
        buff = os.path.split(path)
        for file_name in buff[1:]:
            pointer = self.find_child_of_parent(pointer, file_name)
        return pointer

    def go_to_node(self, node):
        self.current_node = node
        return self.current_node

    def go_to_node_by_path(self, path):
        under_root = []
        while len(path) > 0:
            h, t = os.path.split(path)
            path = h
            if t == self.root.name:
                self.current_node = self.root
                break
            else:
                under_root.append(t)

        #under_root.reverse()
        while len(under_root) > 0:
            self.current_node = self.find_child(under_root.pop())
        return self.current_node

        # self.current_node = self.find_node(under_root)
        # return self.current_node


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

    def get_all_nodes(self):
        nodes = []
        self.__get_all_nodes(self.root, nodes)
        return nodes

    def __get_all_nodes(self, node, nodes):
        nodes.append(node)
        for child in node.children:
            self.__get_all_nodes(child, nodes)

    def compare(self, other_tree):
        return self.compare_nodes(self.root, other_tree.root)
    def compare_nodes(self, target_node, other_node):
        to_delete = []
        to_download = []
        if target_node.full_name.lower() != other_node.full_name.lower():
            return [target_node], []

        target_children = target_node.children.copy()
        other_children = other_node.children.copy()
        other_children.reverse()

        for target in target_node.children:
            found = False
            for other in other_node.children:
                x = target.full_name
                y = other.full_name.lower()
                if target.full_name.lower() == other.full_name.lower():
                    #print("found", target.full_path, " == ", other.full_path)
                    found = True
                    to_del, to_down = self.compare_nodes(target, other)
                    to_delete.extend(to_del)
                    to_download.extend(to_down)
                    other_children.pop(other_children.index(other))
                    target_children.pop(target_children.index(target))
                    break
            # if not found:
            #     to_download.append(target)
        to_delete.extend(other_children)
        to_download.extend(target_children)
        return to_delete, to_download



# tree = DirectoryTree("C:/felt_WK_app/mockup_files")
# tree.print_tree()
