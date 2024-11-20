from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.metrics import sp

from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDLabel:
        text: "MDLabel"
        halign: "center"
        font_style: "nasalization-rg"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        LabelBase.register(
            name="nasalization-rg",
            fn_regular="font_nasalization-rg.otf",
        )

        self.theme_cls.font_styles["nasalization-rg"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "nasalization-rg",
                "font-size": sp(57),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "nasalization-rg",
                "font-size": sp(45),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "nasalization-rg",
                "font-size": sp(36),
            },
        }

        return Builder.load_string(KV)


Example().run()

# Source: Docs