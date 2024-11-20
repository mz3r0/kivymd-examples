from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDCard:
        orientation: "vertical"
        padding: 0, 0, 0 , "36dp"
        size_hint: .5, .5
        style: "elevated"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Theme style - ".format(app.theme_cls.theme_style)
            halign: "center"
            valign: "center"
            bold: True
            font_style: "Display"
            role: "small"

        MDButton:
            on_release: app.switch_theme_style()
            pos_hint: {"center_x": .5}

            MDButtonText:
                text: "Set theme"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Purple" if self.theme_cls.primary_palette == "Blue" else "Blue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

    def on_start(self):
        self.fps_monitor_start()


Example().run()

# Source: Docs