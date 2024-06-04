from pynput.mouse import Button
from pynput import mouse


from typing import Callable


def subscribe_click_events(button:Button, handler:Callable[[int, int], None]):
    def listener_handler(x, y, button_pressed:Button, _pressed):
        if button == button_pressed:
            handler(x,y)
    l = mouse.Listener(
        on_click=listener_handler)
    l.start()


def subscribe_move_events(handler:Callable[[int, int], None]):
    l = mouse.Listener(
        on_move=handler)
    l.start()


def subscribe_scroll_events(handler:Callable[[int, int, int, int], None]):
    l = mouse.Listener(
        on_scroll=handler)
    l.start()