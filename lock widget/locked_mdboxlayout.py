from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


Window.clearcolor = (1, 1, 1, 1)


class DisabledOverlayWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(DisabledOverlayWidget, self).__init__(**kwargs)
        self.enabled = False

        # Draw the semi-transparent overlay
        with self.canvas.after:
            Color(0.8, 0.8, 0.8, 0.5)
            self.overlay = Rectangle(size=self.size, pos=self.pos)

        # Bind size and position updates
        self.bind(size=self.update_overlay, pos=self.update_overlay)

    def set_enabled(self, enabled):
        """ Method to enable or disable the widget. """
        self.enabled = enabled
        self.overlay.opacity = 0 if enabled else 0.5  # Hide overlay if enabled

    def update_overlay(self, *args):
        """ Method to toggle the overlay opacity. """
        self.overlay.size = self.size
        self.overlay.pos = self.pos

    def on_touch_down(self, touch):
        if not self.enabled and self.collide_point(*touch.pos):
            return True  # Consume touch event if disabled
        return super(DisabledOverlayWidget, self).on_touch_down(touch)


class TestApp(MDApp):
    def build(self):
        root = DisabledOverlayWidget(size_hint=(1, 1))
        root.add_widget(MDLabel(text='DisabledOverlayWidget'))
        return root


if __name__ == '__main__':
    TestApp().run()