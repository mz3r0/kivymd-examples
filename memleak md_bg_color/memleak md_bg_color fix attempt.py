from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tooltip import MDTooltipPlain
from kivymd.uix.label import MDIcon
from kivy.graphics import Color, RoundedRectangle


class OptimizedLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not issubclass(
                self.__class__, (MDCheckbox, MDIcon, MDTooltipPlain)
        ):
            self.canvas.remove_group("Background_instruction")

            # FIXME: IndexError
            # try:
            #     self.canvas.before.clear()
            # except IndexError:
            #     pass

            with self.canvas.before:
                self._canvas_bg_color = Color(rgba=kwargs['color'], group="md-label-selection-color")
                self._canvas_bg = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=self.radius,
                    group="md-label-selection-color-rectangle",
                )
                self.bind(pos=self.update_canvas_bg_pos)

    def on_md_bg_color(self, instance_label, color: list | str) -> None:
        """Fired when the :attr:`md_bg_color` value changes."""
        with instance_label.canvas.before:
            self._canvas_bg_color.rgb = color


class MainApp(MDApp):
    def build(self):
        self.loop_count = 0

        #create OptimizedLabel object
        self.banner = OptimizedLabel(
            text="AC POWER LOSS DETECTED",
            size_hint=(None, None),
            size=(1280,28),
            font_style='Headline',
            role='small',
            halign='center',
            valign='center',
            color=(0,0,0,1))

        #set a fixed time update loop
        Clock.schedule_interval(self.update, 1.0/15.0)
        return self.banner

    def update(self,data):
        red = (.9,.2,.2,1)
        white = (1,1,1,1)
        
        #simple timer
        if self.loop_count == 30:
            self.loop_count = 0
        else:
            self.loop_count = self.loop_count + 1

        #alternates background color of label box between red and white
        if self.loop_count > 15:
            #self.banner.text_color = white
            self.banner.md_bg_color = red
        else:
            #self.banner.text_color = red
            self.banner.md_bg_color = white


MainApp().run()