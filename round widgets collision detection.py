from math import sqrt, pow, fabs

from kivy import platform
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDButton


KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    BoxLayout:
        orientation: "vertical"
        spacing: "10px"
        pos_hint: {'center_x':.5, 'center_y':.5}
        size_hint: None, None
        size: self.minimum_size
        
        MDButton:
            MDButtonIcon:
                icon: "plus"
                
            MDButtonText:
                text: "Hello World!"
        MyButton:
            pos_hint: {'center_x':.5, 'center_y':.5}
            MDButtonIcon:
                icon: "plus"
            MDButtonText:
                text: "Hello!"
'''


class MyButton(MDButton):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.check_collision(touch.pos):
                print("Collision VALID")
                return super(MyButton, self).on_touch_down(touch)
        return False

    def check_collision(self, touch_pos):
        r = self.radius[0]
        tx, ty = touch_pos
        px, py = self.pos
        sx, sy = self.size

        # Get coordinates relative to the widget axes
        rx = tx - px
        ry = ty - py

        # Get coordinates relative to the widget center
        half_wx = sx / 2
        half_wy = sy / 2

        fx = fabs(rx - half_wx)
        fy = fabs(ry - half_wy)

        xx = fx - half_wx + r
        yy = fy - half_wy + r

        return self.og_check(xx, yy)

    def og_check(self, x, y):
        r = self.radius[0]
        if x > r or y > r:
            return False

        if x < 0 or y < 0:
            return True

        expected_y = sqrt(pow(r, 2) - pow(x, 2))
        if y > expected_y:
            return False

        return True


class MainApp(MDApp):
    def build(self):
        print(platform)

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        return Builder.load_string(KV)


if __name__ == '__main__':
    MainApp().run()

# NOTE:
# Only works for widgets whose 4 corners use the SAME RADIUS