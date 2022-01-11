from os import name

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

import widgets.navigationwidget
import widgets.progresswidget

if platform == "android":
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.FOREGROUND_SERVICE])
if platform != "android":
    Window.size = (300, 600)
    

Builder.load_file('kvs/signin.kv')
Builder.load_file('kvs/login.kv')
Builder.load_file('kvs/main.kv')
Builder.load_file('kvs/pomodoro_tab.kv')
Builder.load_file('kvs/settings.kv')

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class PopomodoroScreen(Screen):
    current_working_sessions = NumericProperty(0)
    actual_mode = StringProperty("pomodoro")
    def start(self):
        app = MDApp.get_running_app()
        print('Actual mode', self.actual_mode)
        self.ids.circular_progress.bottom_text = "{} of {} sessions".format(self.current_working_sessions, app.working_sessions)
        if(self.actual_mode=='pomodoro'):
            self.ids.actual_status_msg.text = "Focus for {} minutes".format(app.focus_time)
            self.ids.circular_progress.max_counter = app.focus_time * 60
        elif (self.actual_mode=='break'):
            self.ids.actual_status_msg.text = "Take a break for {} minutes".format(app.short_break)
            self.ids.circular_progress.max_counter = app.short_break * 60
        else:
            self.ids.actual_status_msg.text = "Take a long break for {} minutes".format(app.focus_time)
            self.ids.circular_progress.max_counter = app.long_break * 60
        self.ids.circular_progress.bind(on_stop=self.on_stop)
        if not self.ids.circular_progress.running:
            self.ids.play_button.icon = 'pause'
        else:
            self.ids.play_button.icon = 'play'
        self.ids.circular_progress.toggle()
    def reset(self):
        #app = MDApp.get_running_app()
        self.ids.circular_progress.current_percent = 0
        self.ids.circular_progress.counter = 0
    def stop(self):
        self.ids.circular_progress.stop()
        self.ids.play_button.icon = 'play'
        self.ids.circular_progress.current_percent = 0
        self.ids.circular_progress.counter = 0
    def on_stop(self, value, *args):
        print('parent on_stop')
        self.stop()
        #next pomodoro or relax time
        app = MDApp.get_running_app()
        if (self.actual_mode=='pomodoro' and self.current_working_sessions < app.working_sessions):
            self.actual_mode ='break'
            self.current_working_sessions = self.current_working_sessions + 1
        elif (self.actual_mode=='break' and self.current_working_sessions < app.working_sessions):
            self.actual_mode ='pomodoro'
        elif (self.actual_mode=='break' and self.current_working_sessions >= app.working_sessions):
            self.actual_mode ='long_break'
        else:
            self.actual_mode ='pomodoro'
            self.current_working_sessions = 0
        print('Actual mode', self.actual_mode, self.current_working_sessions, app.working_sessions,self.current_working_sessions< app.working_sessions)
class SettingsScreen(Screen):
    pass
class SigninScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class MainApp(MDApp):
    focus_time = NumericProperty(20)
    short_break = NumericProperty(5)
    long_break = NumericProperty(25)
    working_sessions = NumericProperty(4)
    def __init__(self, **kwargs):
        self.title = "Pomodoro"
        super().__init__(**kwargs)
    def build_config(self, config):
        config.setdefaults('pomodorooptions', {
            'focus_time': '20',
            'short_break': '5',
            'long_break': '25',
            'working_sessions': '4'
        })

    def build(self):
        config = self.config
        self.focus_time = config.getint('pomodorooptions','focus_time')
        self.short_break = config.getint('pomodorooptions','short_break')
        self.long_break = config.getint('pomodorooptions','long_break')
        self.working_sessions = config.getint('pomodorooptions','working_sessions')

        self.wm = WindowManager()
        screens = [
            # SigninScreen(name='signin'),
            # LoginScreen(name='login'),
            MainScreen(name='main')
        ]
        for screen in screens:
            self.wm.add_widget(screen)
        self.wm.current = 'main'
        return self.wm
    def on_focus_time(self, instance, value):
        self.config.set('pomodorooptions','focus_time',str(value))
        self.config.write()
        self.focus_time = value
    def on_short_break(self, instance, value):
        self.config.set('pomodorooptions','short_break',str(value))
        self.config.write()
        self.short_break = value
    def on_long_break(self, instance, value):
        self.config.set('pomodorooptions','long_break',str(value))
        self.config.write()
        self.long_break = value
    def on_working_sessions(self, instance, value):
        self.config.set('pomodorooptions','working_sessions',str(value))
        self.config.write()
        self.working_sessions = value

if __name__ == "__main__":
    MainApp().run()
