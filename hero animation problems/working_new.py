from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.hero import MDHeroFrom, MDHeroTo
from kivymd.uix.imagelist.imagelist import MDSmartTile, MDSmartTileImage, MDSmartTileOverlayContainer
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label.label import MDLabel
from kivymd.uix.scrollview import StretchOverScrollStencil, MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivymd.uix.transition.transition import MDTransitionBase

class HeroItem(MDHeroFrom):
    text = StringProperty()
    tag = StringProperty()
    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = "200dp"
        self.radius = "24dp"

    def create_tile(self, img_path):
        # Create SmartTile
        self.tile = MDSmartTile(size_hint=(0.5, None), height="200dp")  # Use size_hint appropriately
        self.tile.bind(on_release=self.on_release)

        # Create SmartTileImage
        self.image = MDSmartTileImage(source=img_path, radius="24dp")
        self.image.ripple_duration_in_fast = 0.05
        self.tile.add_widget(self.image)

        # Create Overlay Container
        self.overlay = MDSmartTileOverlayContainer(
            md_bg_color=(0, 0, 0, .5),
            adaptive_height=True,
            radius=[0, 0, dp(24), dp(24)],
            padding="8dp",
            spacing="8dp",
        )

        self.label = MDLabel(text=self.tag, theme_text_color='Custom', text_color="white", adaptive_height=True)
        self.overlay.add_widget(self.label)
        self.tile.add_widget(self.overlay)

        self.add_widget(self.tile)

    def on_transform_in(self, instance_hero_widget, duration):
        for instance in [
            instance_hero_widget,
            instance_hero_widget._overlay_container,
            instance_hero_widget._image,
        ]:
            Animation(radius=[0, 0, 0, 0], duration=duration).start(instance)

    def on_transform_out(self, instance_hero_widget, duration):
        for instance, radius in {
            instance_hero_widget: [dp(24), dp(24), dp(24), dp(24)],
            instance_hero_widget._overlay_container: [0, 0, dp(24), dp(24)],
            instance_hero_widget._image: [dp(24), dp(24), dp(24), dp(24)],
        }.items():
            Animation(
                radius=radius,
                duration=duration,
            ).start(instance)

    def on_release(self, *args):
        def switch_screen(*args):
            self.manager.current_heroes = [self.tag]
            screen_b = self.manager.get_screen("screen B")
            screen_b.hero_to.tag = self.tag
            self.manager.current = "screen B"

        Clock.schedule_once(switch_screen, 0.2)

class ScreenA():

    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager

        # ScrollView
        self.scroll_view = MDScrollView()
        self.grid = MDGridLayout(id='grid', cols=2, spacing="12dp", padding="12dp", adaptive_height = True,)
    def add_hero_items(self):
        for i in range(12):
            hero_item = HeroItem(text=f"Item {i + 1}", tag=f"Tag {i}", manager=self.manager)
            hero_item.create_tile('4.png')
            #if not i % 2:
            #    hero_item.md_bg_color = "lightgrey"
            self.grid.add_widget(hero_item)

        self.scroll_view.add_widget(self.grid)

        return self.scroll_view

    def get_logs_page(self):
        page = MDScreen(name='screen A')
        page.add_widget(self.add_hero_items())
        return page


class ScreenB(MDScreen):
    hero_to = ObjectProperty()  # Use ObjectProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hero_to = MDHeroTo(size_hint=(1, None), height="220dp", pos_hint={"top": 1})
        self.add_widget(self.hero_to)

        self.button = MDButton(MDButtonText(text="Move Hero To Screen A"),
                            pos_hint={"center_x": .5}, y = "36dp")#size_hint_y=None, height=dp(50)
        self.button.bind(on_release=self.switch_to_screen_a)
        self.add_widget(self.button)

    def switch_to_screen_a(self, *args):
        print('b', self.hero_to.tag)
        self.manager.current = "screen A"
        self.manager.current_heroes = [self.hero_to.tag]

class Mainscreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.label = MDLabel(text='Hello', theme_text_color='Custom', text_color="white", adaptive_height=True,
                             pos_hint={"center_x": 1, "center_y": .5},)
        self.add_widget(self.label)

        self.button = MDButton(MDButtonText(text="Go the Images"),
                            pos_hint={"center_x": .5}, y = "36dp")#size_hint_y=None, height=dp(50)
        self.button.bind(on_release=self.switch_to_screen_image)
        self.add_widget(self.button)

    def switch_to_screen_image(self, *args):
        self.app.root.current = "screen A"

class Example2(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"  # "Light"
        print('self.theme_cls.backgroundColor', self.theme_cls.backgroundColor)

        MDTransitionBase._direction = "out"
        self.manager = MDScreenManager()
        self.manager.primary_palette = "Orange"
        self.manager.theme_style = "Dark"  # "Light"
        #self.manager.md_bg_color = (1, 1, 1, 1) #self.theme_cls.backgroundColor
        main_screen = Mainscreen(name="main screen")

        screen_a = ScreenA(manager=self.manager)
        screen_a_page = screen_a.get_logs_page()

        screen_b = ScreenB(name="screen B")

        self.manager.add_widget(main_screen)
        self.manager.add_widget(screen_a_page)
        self.manager.add_widget(screen_b)

        return self.manager

Example2().run()