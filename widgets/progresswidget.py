from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
    BooleanProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
import datetime

Builder.load_string(
    """
<CustomCircularProgress>:

    canvas.before:
        Color:
            rgba: root.background_circle_color if root.background_circle_color else app.theme_cls.primary_light
        Line:
            circle: (self.x + self.width / 2, self.y + self.height / 2, self.height / 2, root.start_deg, root.end_deg)
            width: root.background_line_width
        Color:
            rgba: root.circle_color if root.circle_color else app.theme_cls.primary_color
        Line:
            circle: (self.x + self.width / 2, self.y + self.height / 2, self.height / 2, root.start_deg, root._current_deg)
            width: root.line_width
            cap: root.cap_type

    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            id: _percent_label
            halign: "center"
            theme_text_color: "Custom"
            text_color: root.percent_color if root.percent_color else app.theme_cls.primary_color
            font_size: root.percent_size
            bold: True
        MDLabel:
            halign: "center"
            theme_text_color: "Custom"
            text: root.bottom_text
            color: 133/255, 138/255, 147/255, 1
            font_size: '15sp'
            #text_color: root.percent_color if root.percent_color else app.theme_cls.primary_color
            #font_size: root.percent_size
"""
)


class CustomCircularProgress(ThemableBehavior, BoxLayout):
    circle_color = ListProperty()
    start_deg = NumericProperty(0)
    end_deg = NumericProperty(360)
    line_width = NumericProperty("3dp")
    percent_color = ListProperty()
    percent_size = NumericProperty("20dp")
    current_percent = NumericProperty(-1)
    anim_speed = NumericProperty(0.3)
    anim_transition = StringProperty("out_quad")
    max_percent = NumericProperty(100)
    percent_type = OptionProperty("percent", options=["percent", "relative", "countdown"])
    background_circle_color = ListProperty()
    background_line_width = NumericProperty("1dp")
    cap_type = OptionProperty("round", options=["round", "none"])
    _current_deg = NumericProperty(-1)
    running = BooleanProperty(False)
    counter = NumericProperty(0)
    max_counter = NumericProperty(1200)
    bottom_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())
        self.register_event_type('on_stop')

    def _update(self):
        self.current_percent = 0

    def on_current_percent(self, *args):
        deg_distance = self.end_deg - self.start_deg
        self._each_percent = deg_distance / self.max_percent

        _current_deg = args[1] * self._each_percent
        percent_anim = Animation(
            _current_deg=self.start_deg + _current_deg,
            duration=self.anim_speed,
            t=self.anim_transition,
        )
        percent_anim.start(self)

    def on__current_deg(self, *args):
        if self.percent_type == "percent":
            self.ids._percent_label.text = (
                str(
                    int(
                        (self._current_deg - self.start_deg)
                        / self._each_percent
                    )
                )
                + " %"
            )
        elif self.percent_type == "relative":
            self.ids._percent_label.text = (
                str(
                    int(
                        (self._current_deg - self.start_deg)
                        / self._each_percent
                    )
                )
                + "\\"
                + str(self.max_percent)
            )
        elif self.percent_type == "countdown":
            self.ids._percent_label.text = str(datetime.timedelta(seconds=self.counter))
    
    def start(self):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 1)
    def update(self, *kwargs):
        self.counter = self.counter + 1
        if (self.counter>=self.max_counter):
            self.stop()
            self.dispatch('on_stop')
        self.current_percent = (self.counter/self.max_counter)*100
    def stop(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)
    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()
    def on_stop(self):
        pass
