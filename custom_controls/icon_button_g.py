
import flet as ft
from typing import Any, Optional, Union
from flet_core.alignment import Alignment
from flet_core.buttons import ButtonStyle
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.theme import ThemeVisualDensity
from flet_core.types import (
    AnimationValue,
    MouseCursor,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
)




class IconButtonG(ft.Column):
    def __init__(
            self,
            icon: Optional[str] = None,
            icon_color: Optional[str] = None,
            icon_size: OptionalNumber = None,
            selected: Optional[bool] = None,
            selected_icon: Optional[str] = None,
            selected_icon_color: Optional[str] = None,
            bgcolor: Optional[str] = None,
            highlight_color: Optional[str] = None,
            style: Optional[ButtonStyle] = None,
            content: Optional[Control] = None,
            autofocus: Optional[bool] = None,
            disabled_color: Optional[str] = None,
            hover_color: Optional[str] = None,
            focus_color: Optional[str] = None,
            splash_color: Optional[str] = None,
            splash_radius: OptionalNumber = None,
            alignment: Optional[Alignment] = None,
            padding: PaddingValue = None,
            enable_feedback: Optional[bool] = None,
            url: Optional[str] = None,
            url_target: Optional[UrlTarget] = None,
            mouse_cursor: Optional[MouseCursor] = None,
            visual_density: Optional[ThemeVisualDensity] = None,
            on_click=None,
            on_focus=None,
            on_blur=None,
            #
            # GestureDetector
            mouse_cursor_gesture: Optional[MouseCursor] = None,
            drag_interval: Optional[int] = None,
            hover_interval: Optional[int] = None,
            on_tap= lambda *args: None,
            on_tap_down=None,
            on_tap_up=None,
            on_multi_tap=None,
            multi_tap_touches=None,
            on_multi_long_press=None,
            on_secondary_tap=None,
            on_secondary_tap_down=None,
            on_secondary_tap_up=None,
            on_long_press_start=None,
            on_long_press_end=None,
            on_secondary_long_press_start=None,
            on_secondary_long_press_end=None,
            on_double_tap=None,
            on_double_tap_down=None,
            on_horizontal_drag_start=None,
            on_horizontal_drag_update=None,
            on_horizontal_drag_end=None,
            on_vertical_drag_start=None,
            on_vertical_drag_update=None,
            on_vertical_drag_end=None,
            on_pan_start=None,
            on_pan_update=None,
            on_pan_end=None,
            on_scale_start=None,
            on_scale_update=None,
            on_scale_end=None,
            on_hover=None,
            on_enter=None,
            on_exit=None,
            on_scroll=None,
            #
            # ConstrainedControl and AdaptiveControl
            #
            ref: Optional[Ref] = None,
            key: Optional[str] = None,
            width: OptionalNumber = None,
            height: OptionalNumber = None,
            left: OptionalNumber = None,
            top: OptionalNumber = None,
            right: OptionalNumber = None,
            bottom: OptionalNumber = None,
            expand: Union[None, bool, int] = None,
            expand_loose: Optional[bool] = None,
            col: Optional[ResponsiveNumber] = None,
            opacity: OptionalNumber = None,
            rotate: RotateValue = None,
            scale: ScaleValue = None,
            offset: OffsetValue = None,
            aspect_ratio: OptionalNumber = None,
            animate_opacity: AnimationValue = None,
            animate_size: AnimationValue = None,
            animate_position: AnimationValue = None,
            animate_rotation: AnimationValue = None,
            animate_scale: AnimationValue = None,
            animate_offset: AnimationValue = None,
            on_animation_end=None,
            tooltip: Optional[str] = None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
            adaptive: Optional[bool] = None,
    ):
        self.icon_button = ft.IconButton(
                    icon=icon,
                    icon_color=icon_color,
                    icon_size=icon_size,
                    selected=selected,
                    selected_icon=selected_icon,
                    selected_icon_color=selected_icon_color,
                    bgcolor=bgcolor,
                    highlight_color=highlight_color,
                    style=style,
                    content=content,
                    autofocus=autofocus,
                    disabled_color=disabled_color,
                    hover_color=hover_color,
                    focus_color=focus_color,
                    splash_color=splash_color,
                    splash_radius=splash_radius,
                    alignment=alignment,
                    padding=padding,
                    enable_feedback=enable_feedback,
                    url=url,
                    url_target=url_target,
                    mouse_cursor=mouse_cursor,
                    visual_density=visual_density,
                    on_click=on_click,
                    on_focus=on_focus,
                    on_blur=on_blur,
                    ref=ref,
                    key=key,
                    width=width,
                    height=height,
                    left=left,
                    top=top,
                    right=right,
                    bottom=bottom,
                    expand=expand,
                    expand_loose=expand_loose,
                    col=col,
                    opacity=opacity,
                    rotate=rotate,
                    scale=scale,
                    offset=offset,
                    aspect_ratio=aspect_ratio,
                    animate_opacity=animate_opacity,
                    animate_size=animate_size,
                    animate_position=animate_position,
                    animate_rotation=animate_rotation,
                    animate_scale=animate_scale,
                    animate_offset=animate_offset,
                    on_animation_end=on_animation_end,
                    tooltip=tooltip,
                    visible=visible,
                    disabled=disabled,
                    data=data,
                    adaptive=adaptive,
                )
        self.gesture = ft.GestureDetector(
            mouse_cursor=mouse_cursor_gesture,
            drag_interval=drag_interval,
            hover_interval=hover_interval,
            on_tap=on_tap,
            on_tap_down=on_tap_down,
            on_tap_up=on_tap_up,
            on_multi_tap=on_multi_tap,
            multi_tap_touches=multi_tap_touches,
            on_multi_long_press=on_multi_long_press,
            on_secondary_tap=on_secondary_tap,
            on_secondary_tap_down=on_secondary_tap_down,
            on_secondary_tap_up=on_secondary_tap_up,
            on_long_press_start=on_long_press_start,
            on_long_press_end=on_long_press_end,
            on_secondary_long_press_start=on_secondary_long_press_start,
            on_secondary_long_press_end=on_secondary_long_press_end,
            on_double_tap=on_double_tap,
            on_double_tap_down=on_double_tap_down,
            on_horizontal_drag_start=on_horizontal_drag_start,
            on_horizontal_drag_update=on_horizontal_drag_update,
            on_horizontal_drag_end=on_horizontal_drag_end,
            on_vertical_drag_start=on_vertical_drag_start,
            on_vertical_drag_update=on_vertical_drag_update,
            on_vertical_drag_end=on_vertical_drag_end,
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end,
            on_scale_start=on_scale_start,
            on_scale_update=on_scale_update,
            on_scale_end=on_scale_end,
            on_hover=on_hover,
            on_enter=on_enter,
            on_exit=on_exit,
            on_scroll=on_scroll,
        )
        self.gesture.content = self.icon_button
        super().__init__(controls=[self.gesture], alignment=ft.MainAxisAlignment.CENTER)
        self.padding = ft.Padding(0, 0, 0, 0)
        self.icon_button.padding = ft.Padding(0, 0, 0, 0)

    # def __init__(self, icon_button: ft.IconButton, gesture: ft.GestureDetector, **kwargs):
    #     self.icon_button = icon_button
    #     self.gesture = gesture
    #     self.gesture.content = self.icon_button
    #     super().__init__(controls=[self.gesture], alignment = ft.MainAxisAlignment.CENTER, ** kwargs)



    @property
    def icon(self):
        return self.icon_button.icon

    @property
    def selected_icon(self):
        return self.icon_button.selected_icon

    @property
    def icon_size(self):
        return self.icon_button.icon_size

    @property
    def splash_radius(self):
        return self.icon_button.splash_radius

    @property
    def splash_color(self):
        return self.icon_button.splash_color

    @property
    def icon_color(self):
        return self.icon_button.icon_color

    @property
    def highlight_color(self):
        return self.icon_button.highlight_color

    @property
    def selected_icon_color(self):
        return self.icon_button.selected_icon_color

    @property
    def bgcolor(self):
        return self.icon_button.bgcolor

    @property
    def hover_color(self):
        return self.icon_button.hover_color

    @property
    def focus_color(self):
        return self.icon_button.focus_color

    @property
    def disabled_color(self):
        return self.icon_button.disabled_color

    @property
    def selected(self) -> Optional[bool]:
        return self.icon_button.selected

    @property
    def enable_feedback(self) -> Optional[bool]:
        return self.icon_button.enable_feedback

    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.icon_button.style

    @property
    def url(self):
        return self.icon_button.url

    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.icon_button.url_target

    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.icon_button.mouse_cursor

    @property
    def visual_density(self) -> Optional[ThemeVisualDensity]:
        return self.icon_button.visual_density

    @property
    def on_click(self):
        return self.icon_button.on_click

    @property
    def autofocus(self) -> Optional[bool]:
        return self.icon_button.autofocus

    @property
    def on_focus(self):
        return self.icon_button.on_focus

    @property
    def on_blur(self):
        return self.icon_button.on_blur

    def set_on_secondary_tap(self, on_secondary_tap):
        self.gesture.on_secondary_tap = on_secondary_tap

    def set_on_click(self, on_click):
        self.icon_button.on_click = on_click

    def set_on_hover(self, on_hover):
        self.gesture.on_hover = on_hover

    def set_on_secondary_tap_down(self, on_secondary_tap_down):
        self.gesture.on_secondary_tap_down = on_secondary_tap_down

    def set_on_secondary_tap_up(self, on_secondary_tap_up):
        self.gesture.on_secondary_tap_up = on_secondary_tap_up

    def set_on_double_tap(self, on_double_tap):
        self.gesture.on_double_tap = on_double_tap

    def set_on_double_tap_down(self, on_double_tap_down):
        self.gesture.on_double_tap_down = on_double_tap_down

    def set_on_long_press_start(self, on_long_press_start):
        self.gesture.on_long_press_start = on_long_press_start

    def set_on_long_press_end(self, on_long_press_end):
        self.gesture.on_long_press_end = on_long_press_end

    def set_on_secondary_long_press_start(self, on_secondary_long_press_start):
        self.gesture.on_secondary_long_press_start = on_secondary_long_press_start

    def set_on_secondary_long_press_end(self, on_secondary_long_press_end):
        self.gesture.on_secondary_long_press_end = on_secondary_long_press_end

    def set_on_horizontal_drag_start(self, on_horizontal_drag_start):
        self.gesture.on_horizontal_drag_start = on_horizontal_drag_start

    def set_on_horizontal_drag_update(self, on_horizontal_drag_update):
        self.gesture.on_horizontal_drag_update = on_horizontal_drag_update

    def set_on_horizontal_drag_end(self, on_horizontal_drag_end):
        self.gesture.on_horizontal_drag_end = on_horizontal_drag_end

    def set_on_vertical_drag_start(self, on_vertical_drag_start):
        self.gesture.on_vertical_drag_start = on_vertical_drag_start

    def set_on_vertical_drag_update(self, on_vertical_drag_update):
        self.gesture.on_vertical_drag_update = on_vertical_drag_update

    def set_on_vertical_drag_end(self, on_vertical_drag_end):
        self.gesture.on_vertical_drag_end = on_vertical_drag_end

    def set_on_pan_start(self, on_pan_start):
        self.gesture.on_pan_start = on_pan_start

    def set_on_pan_update(self, on_pan_update):
        self.gesture.on_pan_update = on_pan_update

    def set_on_pan_end(self, on_pan_end):
        self.gesture.on_pan_end = on_pan_end

    def set_on_scale_start(self, on_scale_start):
        self.gesture.on_scale_start = on_scale_start

    def set_on_scale_update(self, on_scale_update):
        self.gesture.on_scale_update = on_scale_update

    def set_on_scale_end(self, on_scale_end):
        self.gesture.on_scale_end = on_scale_end



    


