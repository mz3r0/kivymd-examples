from kivy.lang import Builder
import pandas as pd
import numpy as np

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.scrollview import MDScrollView
from random import random
from kivymd.app import MDApp

from kivy.core.window import Window


KV = """
MDScreen:
    name: 'main'

    Outer:
        bl: bl
        inner: inner

        scroll_type: ['bars']
        scroll_wheel_distance: dp(100)
        bar_width: 10
        bar_color: 146/255, 146/255, 146/255, 1
        bar_inactive_color: 146/255, 146/255, 146/255, 1

        MDBoxLayout:
            id: bl
            orientation: 'horizontal'
            padding: 30
            spacing: 30
            size_hint_x: None
            width: self.minimum_width

            MDCard:
                size_hint_x: None
                width: 400

                Inner:
                    id: inner

            MDCard:
                size_hint_x: None
                width: 400

            MDCard:
                size_hint_x: None
                width: 400

            MDCard:
                size_hint_x: None
                width: 400

<MyTableCell>:
    text_size: self.size
    adaptive_height: True
    halign: "center"

<Inner>:
    do_scroll: True
    bar_width: dp(10)
    bar_color: 146/255, 146/255, 146/255, 1
    bar_inactive_color: 146/255, 146/255, 146/255, 1

    viewclass: "MyTableCell"
    RecycleGridLayout:
        cols: 6
        spacing: 10
        default_size_hint: None, None
        default_size: 98, 48
        size_hint: None, None
        height: self.minimum_height
        width: self.minimum_width

"""


class Outer(MDScrollView):
    shift_down = False  # Used for horizontal scrolling

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    # def _set_do_scroll(self, value):
    #     if value:
    #         self.rv.do_scroll = False, False
    #         self.do_scroll = True, False
    #     else:
    #         self.rv.do_scroll = True, True
    #         self.do_scroll = False, False

    def _on_keyboard_down(self, *args):
        """ Detect left or right shift key down """
        if args[1] in [303, 304]:
            self.shift_down = True
            # self._set_do_scroll(True)

    def _on_keyboard_up(self, *args):
        """ Detect left or right shift key up """
        if args[1] in [303, 304]:
            self.shift_down = False
            # self._set_do_scroll(False)

    def on_scroll_start(self, touch, check_children=True):
        mx = self.scroll_x * (self.bl.width - Window.width) + touch.pos[0]

        # print(self.bl.width, Window.width, self.scroll_x, touch.pos[0], mx)

        if self.shift_down or not self.inner.collide_point(mx, touch.pos[1]):
            # self._set_do_scroll(True)
            self.invert_touch_button(touch)
        elif self.inner.collide_point(mx, touch.pos[1]) and not self.shift_down:
            pass
            # self._set_do_scroll(False)

        super().on_scroll_start(touch, check_children)

    def invert_touch_button(self, touch):
        if touch.button == "scrollup":
            touch.button = "scrollleft"
        if touch.button == "scrolldown":
            touch.button = "scrollright"
        return touch


class MyTableCell(RecycleDataViewBehavior, MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = data['text']
        return super(MyTableCell, self).refresh_view_attrs(rv, index, data)


class Inner(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{"text": f"{random()}"} for _ in range(600)]


class SampleApp(MDApp):
    def build(self):
        Window.always_on_top = True
        Window.minimum_width = 500
        Window.minimum_height = 400
        Window.size = (1080, 720)
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_string(KV)


if __name__ == '__main__':
    SampleApp().run()

# Problem: Scrollbars don't work
