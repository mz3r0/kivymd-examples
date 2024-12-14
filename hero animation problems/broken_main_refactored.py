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
            # print(self.manager.current_heroes)
            self.manager.current_heroes = [self.tag]
            # print(self.manager.current_heroes)
            self.manager.get_screen("screen b").heroes_to[0].tag = self.tag
            self.manager.current = "screen b"

        Clock.schedule_once(switch_screen, 0.2)


def to_screen(manager, sc_name, heroes=None):
    # First set the manager's heroes if
    # the target screen contains as any heroes
    if heroes is not None:
        manager.current_heroes = heroes
        print(12)

    # Second change the current screen name
    manager.current = sc_name


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"  # "Light"
        
        self.manager = MDScreenManager()

        # MAIN SCREEN STUFF

        main_screen = MDScreen(name='MainScreen')
        main_screen.app = self  # We no longer need MDApp.get_running_app()
        hello_message = MDLabel(text='Hello', theme_text_color='Custom', text_color="white", adaptive_height=True,
                                pos_hint={"center_x": 1, "center_y": .5}, )
        main_screen.add_widget(hello_message)
        go_to_images_button = MDButton(MDButtonText(text="Go the Images"),
                                 pos_hint={"center_x": .5}, y="36dp")  # size_hint_y=None, height=dp(50)
        go_to_images_button.bind(
            on_release=lambda *args: to_screen(self.manager, 'screen a')
        )

        main_screen.add_widget(go_to_images_button)

        # SCREEN A STUFF

        screen_a = MDScreen(name='screen a')

        # Next line throws error, because self.manager.add_widget(screen_a) already sets self.manager
        # screen_a.manager = self.manager

        # we can access grid using id, so no need to store it inside any objects
        heroes_grid = MDGridLayout(id='grid', cols=2, spacing="12dp", padding="12dp", adaptive_height=True, )

        # Fill the grid!
        for i in range(12):
            tag = f"Tag {i}"
            hero_item = HeroItem(text=f"Item {i + 1}", tag=tag, manager=self.manager)
            hero_item.create_tile('https://github.com/kivymd/internal/raw/main/logo/kivymd_logo_blue.png')
            if not i % 2:
                hero_item.md_bg_color = "lightgrey"
            heroes_grid.add_widget(hero_item)

        # no need to store this inside screen_a, we won't have to access it later
        scroll_view = MDScrollView()

        scroll_view.add_widget(heroes_grid)  # Add the grid!
        screen_a.add_widget(scroll_view)  # Add the scrollview!

        # SCREEN B STUFF

        screen_b = MDScreen(name="screen b")

        screen_b.heroes_to = [MDHeroTo(size_hint=(1, None), height="220dp", pos_hint={"top": 1})]
        screen_b.add_widget(screen_b.heroes_to[0])

        go_back_button = MDButton(MDButtonText(text="Move Hero To Screen A"),
                          pos_hint={"center_x": .5},
                          y="36dp")#size_hint_y=None, height=dp(50)

        go_back_button.bind(
            on_release=lambda *args: to_screen(self.manager, 'screen a', [])
        )

        screen_b.add_widget(go_back_button)

        self.manager.add_widget(main_screen)
        self.manager.add_widget(screen_a)
        self.manager.add_widget(screen_b)

        return self.manager

Example().run()

