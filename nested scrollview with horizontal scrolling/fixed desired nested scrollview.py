import pandas as pd
import numpy as np
from random import random

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ListProperty
from kivy.effects.scroll import ScrollEffect

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.scrollview import MDScrollView


class NoOverscrollEffect(ScrollEffect):
    """Custom Scroll Effect to Disable Overscroll"""

    def convert_overscroll(self, *args):
        return 0, 0

    def reset_scale(self, *args):
        return 0, 0

    def on_scroll_stop(self):
        self.scroll_y = max(0, min(self.scroll_y, 1))
        self.scroll_x = max(0, min(self.scroll_x, 1))


class Outer(MDScrollView):
    masks = ListProperty()
    shift_down = False  # Used for horizontal scrolling

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.effect_cls = NoOverscrollEffect
        Window.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _on_keyboard_down(self, *args):
        """ Detect left or right shift key down """
        if args[1] in [303, 304]:
            self.shift_down = True

    def _on_keyboard_up(self, *args):
        """ Detect left or right shift key up """
        if args[1] in [303, 304]:
            self.shift_down = False

    @staticmethod
    def invert_touch_button(touch):
        if touch.button == "scrollup":
            touch.button = "scrollleft"
        if touch.button == "scrolldown":
            touch.button = "scrollright"
        return touch

    def on_touch_down(self, touch):
        # Inspired by el3phanten's scripts in kivy discord
        # and snu's script linked at the end
        for mask in self.masks:
            coords = mask.to_parent(*mask.to_widget(*touch.pos))
            collide = mask.collide_point(*coords)

            if self.shift_down:
                self.invert_touch_button(touch)

            if collide \
                    and not mask.scroll_x == 1 \
                    and not mask.scroll_x == 0:
                touch.apply_transform_2d(mask.to_widget)
                touch.apply_transform_2d(mask.to_parent)
                mask.on_touch_down(touch)
                return True
            else:
                self.invert_touch_button(touch)
        super().on_touch_down(touch)


KV = """
MDScreen:
    name: 'main'

    Outer:
        bl: bl
        inner: inner
        masks: [inner]
        
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: 80
        bar_width: 12
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
    viewclass: "MyTableCell"
    
    do_scroll: True
    scroll_type: ['bars', 'content']
    
    bar_width: 13
    bar_color: 146/255, 146/255, 146/255, 1
    bar_inactive_color: 146/255, 146/255, 146/255, 1
    
    RecycleGridLayout:
        cols: 6
        spacing: 10
        default_size_hint: None, None
        default_size: 98, 48
        size_hint: None, None
        height: self.minimum_height
        width: self.minimum_width

"""


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
        root = Builder.load_string(KV)
        root.ids.inner.effect_cls = NoOverscrollEffect
        return root


if __name__ == '__main__':
    SampleApp().run()

# Snu: https://github.com/snuq/KivyExamples/blob/854608232c9ef3a86097d4b96e1fffda7baac646/ScrollView/scrollview_exclude.py