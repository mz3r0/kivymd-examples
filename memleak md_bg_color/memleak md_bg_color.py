from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class MainApp(MDApp):
    def build(self):
        self.loop_count = 0

        #create MDLabel object
        self.banner = MDLabel(
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
