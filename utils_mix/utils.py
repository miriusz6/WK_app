import os
from win32api import GetSystemMetrics
CURR_DIR = os.getcwd()
import pyautogui
import win32gui
from pymouse import PyMouse

# def mk_tree_data(path):
#     tree_data = mk_tree_data_h(path,[])
#     return tree_data



def mk_tree_data_h(root_path):
    ret = []
    for name in os.listdir(root_path):
        split = os.path.splitext(name)
        name = split[0]
        path = os.path.join(root_path, name)
        if os.path.isdir(path):
            ret.append({"path": path, "name": name, "type": "dir", "ext": None, "children": mk_tree_data_h(path)})
        else:
            ext = split[1]
            ret.append({"path": path, "name": name, "type": "file", "ext": ext, "children":None})
    return ret





def get_window_info(name):

    chrome = None
    # for x in pyautogui.getAllWindows():
    #     print(x.title)
    for x in pyautogui.getAllWindows():
        if name in x.title:
            chrome = x.title
            break
        # print(x.position)
    #rint(type(chrome))



    handle = win32gui.FindWindow(None, chrome)
    #print(handle)
    # left, top, right, bottom ?!
    " x,  y, w, h"
    #print(win32gui.GetWindowRect(handle))
    return win32gui.GetWindowRect(handle)








def calc_screen_rect(page_width, page_height, left, top, control_w, control_h, window_name):
    # left_upper_corner = (left,top)
    # right_lower_corner = (left+control_w,top+control_h)

    l, t, r, b = get_window_info(window_name)
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)
    r = screen_w - r
    b = screen_h - b

    window_width = screen_w - l - r
    window_height = screen_h - t - b
    #print(window_width, window_height)

    # window border padding
    width_padding = window_width - page_width
    height_padding = window_height - page_height

    #print("width sum: ", window_width+width_padding+l+r)
    #print("height sum: ", window_height+height_padding+t+b)

    left_upper_corner_screen = (l + (width_padding -8) + left, t + (height_padding -8) + top)
    right_lower_corner_screen = left_upper_corner_screen[0] + control_w, left_upper_corner_screen[1] + control_h
    return left_upper_corner_screen, right_lower_corner_screen

def calc_click_pos(page_width,page_height,window_name):


    l, t, r, b = get_window_info(window_name)
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)
    r = screen_w - r
    b = screen_h - b

    window_width = screen_w - l - r
    window_height = screen_h - t - b
    #print(window_width, window_height)

    # window border padding
    width_padding = window_width - page_width
    height_padding = window_height - page_height


    mouse = PyMouse()
    mouse_pos = mouse.position()

    left_pad =  mouse_pos[0] - l
    top_pad = mouse_pos[1] -  t


    return left_pad - (width_padding/1)+8 ,top_pad - (height_padding/1) +8

