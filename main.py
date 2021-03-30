import datetime

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput

Window.size = (1080 // 2, 2240 // 2)
# path = 'data'
path = '/storage/emulated/0/'


class Container(BoxLayout):
    orientation = 'vertical'


class MyLabel(Label):
    def __init__(self, bg_color, **kwargs):
        self.bg_color = bg_color
        super().__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)


class MyTextInput(TextInput):
    def __init__(self, day: int, lesson: int, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.lesson = lesson
        # self.data[i]["lessons"][j]['lesson']


class DiaryApp(App):
    def __init__(self):
        super(DiaryApp, self).__init__()
        with open(f'{path}/data.json', encoding='utf-8') as file:
            self.data = json.load(file)
        now = datetime.datetime.weekday(datetime.datetime.now())
        self.day = 0 if now == 5 or now == 6 else now
        self.start_of_the_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        self.date = self.start_of_the_week + datetime.timedelta(days=self.day)
        if self.date < datetime.date.today():
            self.start_of_the_week += datetime.timedelta(days=7)

    def save(self, instance, value):
        self.data[instance.day]['lessons'][instance.lesson]['task'] = value
        with open(f'{path}/data.json', 'w') as f:
            json.dump(self.data, f, indent=2)

    def build(self):
        main_layout = Container()
        carousel = Carousel(loop=True)
        for i in range(5):
            day_layout = Container()
            # дата
            date_box = Container(size_hint=(1, 0.15))
            date = self.start_of_the_week + datetime.timedelta(days=i)
            date_label = MyLabel(text=f'{self.data[i]["day"]} [{date}]',
                                 bg_color=(0.23, 0.23, 0.23, 1))
            date_box.add_widget(date_label)
            day_layout.add_widget(date_box)
            #
            for j in range(len(self.data[i]["lessons"])):
                lesson = self.data[i]["lessons"][j]
                color = (0.23, 0.23, 0.23, 1) if j % 2 else (0.5, 0.5, 0.5, 1)
                card = GridLayout(rows=2)
                title = GridLayout(cols=2, size_hint_y=0.25)
                title.add_widget(MyLabel(text=f'{lesson["lesson"]}', bg_color=color))
                title.add_widget(MyLabel(text=f'{lesson["less_start"]}-{lesson["less_finish"]}', bg_color=color))
                card.add_widget(title)
                text = MyTextInput(
                    foreground_color=(1, 1, 1, 1),
                    background_color=color,
                    cursor_color=(1, 1, 1, 1),
                    text=f'{lesson["task"]}',
                    font_size='25sp',
                    day=i, lesson=j
                )
                text.bind(text=self.save)
                card.add_widget(text)
                day_layout.add_widget(card)
            carousel.add_widget(day_layout)
        carousel.index = self.day
        main_layout.add_widget(carousel)
        return main_layout


if __name__ == '__main__':
    app = DiaryApp()
    app.run()
