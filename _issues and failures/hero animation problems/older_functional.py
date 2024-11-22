from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.hero import MDHeroFrom
from kivymd.uix.transition import MDSharedAxisTransition


KV = '''
<HeroItem>
    size_hint_x: 1
    size_hint_y: None
    height: "200dp"
    radius: "24dp"

    MDSmartTile:
        id: tile
        size_hint: None, None
        size: root.size
        on_release: root.on_release()

        MDSmartTileImage:
            id: image
            source: 'https://github.com/kivymd/internal/raw/main/logo/kivymd_logo_blue.png'
            radius: dp(24)

        MDSmartTileOverlayContainer:
            id: overlay
            md_bg_color: 0, 0, 0, .5
            adaptive_height: True
            padding: "8dp"
            spacing: "8dp"
            radius: [0, 0, dp(24), dp(24)]

            MDLabel:
                text: root.tag
                theme_text_color: "Custom"
                text_color: "white"
                adaptive_height: True


MDScreenManager:
    md_bg_color: self.theme_cls.backgroundColor
    transition: app.transition

    MDScreen:
        name: "screen A"

        ScrollView:

            MDGridLayout:
                id: box
                cols: 2
                spacing: "12dp"
                padding: "12dp"
                adaptive_height: True

    MDScreen:
        name: "screen B"
        heroes_to: [hero_to]

        MDBoxLayout:
            orientaion: 'horizontal'
            
            MDHeroTo:
                id: hero_to
                size_hint: 1, None
                height: "220dp"
                pos_hint: {"top": 1}
    
        MDButton:
            pos_hint: {"center_x": .5}
            y: "36dp"
            on_release:
                root.current_heroes = [hero_to.tag]
                root.current = "screen A"

            MDButtonText:
                text: "Move Hero To Screen A"
'''

def set_size_hint_one(widget):
    widget.ids.tile.size_hint = (1, 1)

def set_size_hint_none(widget):
    widget.ids.tile.size_hint = (None, None)

class HeroItem(MDHeroFrom):
    text = StringProperty()
    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.image.ripple_duration_in_fast = 0.05

    def on_transform_in(self, instance_hero_widget, duration):
        set_size_hint_none(self)

        for instance in [
            instance_hero_widget,
            instance_hero_widget._overlay_container,
            instance_hero_widget._image,
        ]:
            Animation(radius=[0, 0, 0, 0], duration=duration).start(instance)

        Clock.schedule_once(lambda x: set_size_hint_one(self), duration+0.1)

    def on_transform_out(self, instance_hero_widget, duration):
        set_size_hint_none(self)

        for instance, radius in {
            instance_hero_widget: [dp(24), dp(24), dp(24), dp(24)],
            instance_hero_widget._overlay_container: [0, 0, dp(24), dp(24)],
            instance_hero_widget._image: [dp(24), dp(24), dp(24), dp(24)],
        }.items():
            Animation(
                radius=radius,
                duration=duration,
            ).start(instance)

        Clock.schedule_once(lambda x: set_size_hint_one(self), duration+0.1)


    def on_release(self):
        def switch_screen(*args):

            print(self.manager.current_heroes)
            self.manager.current_heroes = [self.tag]
            print(self.manager.current_heroes)
            self.manager.ids.hero_to.tag = self.tag
            self.manager.current = "screen B"

        Clock.schedule_once(switch_screen, 0.2)


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = MDSharedAxisTransition()
        self.transition.transition_axis = "z"
        self.transition.duration = 0.2

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for i in range(12):
            hero_item = HeroItem(
                text=f"Item {i + 1}", tag=f"Tag {i}", manager=self.root
            )
            if not i % 2:
                hero_item.md_bg_color = "lightgrey"
            self.root.ids.box.add_widget(hero_item)


Example().run()