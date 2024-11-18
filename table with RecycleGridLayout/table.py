import os
import pandas as pd
import numpy as np

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


KV = """
<Cell>:
    text_size: self.size
    adaptive_height: True
    halign: "center"

<Table>:
    viewclass: "Cell"
    RecycleGridLayout:
        id: rgl
        spacing: 10
        default_size_hint: None, None
        default_size: dp(98), dp(48)
        size_hint_y: None
        height: self.minimum_height
"""


Builder.load_string(KV)


def calc_font_role(text_length):
    role = 'large'  # Default
    if text_length > 100:
        role = 'small'  # Was 'extra-small' in my custom app
    elif text_length > 50:
        role = 'small'
    elif text_length > 15:
        role = 'medium'
    return role


def calc_valign(text_length):
    alignment = 'center'  # Default
    if text_length > 20:
        alignment = 'top'
    return alignment


def prepare_recycle_view_data(df, truncate=False):
    df_data = []  # List of {'text': 'content'} dicts per GridLayout cell

    arr = df.to_numpy()
    num_rows, num_cols = arr.shape

    tuple_generator = ((i, j) for i in range(num_rows) for j in range(num_cols))
    for tup in tuple_generator:
        cell = str(arr[tup])
        if truncate and len(cell) > 15:
            cell = f"{cell[:15]} ..."
        df_data.append(dict(text=cell))

    return df_data


class Cell(RecycleDataViewBehavior, MDLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = data['text']

        self.role = calc_font_role(len(self.text))
        self.valign = calc_valign(len(self.text))

        return super(Cell, self).refresh_view_attrs(rv, index, data)


class Table(RecycleView):
    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data or []


class TestApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

        dirty_data = pd.read_csv('nonsense.csv')

        formatted_data = prepare_recycle_view_data(dirty_data)
        root = Table(data=formatted_data)

        root.ids.rgl.cols = dirty_data.shape[1]

        return root


if __name__ == '__main__':
    TestApp().run()  # Ran in kivy 2.3.0 and kivymd 2.0.1.dev0
