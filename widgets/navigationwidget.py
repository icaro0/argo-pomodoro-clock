from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string(
    """
<CustomBottomNavigation>:
    orientation: 'vertical'
    size_hint_y: .1
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: 'pomodoro'
            icon: 'clock'
            PopomodoroScreen:
        MDBottomNavigationItem:
            name: 'options'
            icon: 'cog'
            SettingsScreen:
"""
)


class CustomBottomNavigation(MDBoxLayout):
    pass