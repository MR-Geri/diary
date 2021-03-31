import datetime
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import join
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput

Window.size = (1080, 2240)


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


class MyButton(Button):
    def __init__(self, day: int, lesson: int, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.lesson = lesson

    def on_press(self, *args, **kwargs):
        app.text_edit.day = self.day
        app.text_edit.lesson = self.lesson
        app.text_edit.upd()
        app.main_screen.manager.current = 'text_edit'


class ScreenTextEdit(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.day = 0
        self.lesson = 0
        layout = BoxLayout(size_hint=(1, 0.6), pos_hint={'top': 1}, orientation='vertical')
        self.text = TextInput(
            foreground_color=(1, 1, 1, 1),
            background_color=(0.5, 0.5, 0.5, 1),
            cursor_color=(1, 1, 1, 1),
            text=f'{self.data[self.day]["lessons"][self.lesson]["task"]}',
            font_size='20sp'
        )
        layout.add_widget(self.text)
        layout.add_widget(Button(text='Сохранить', on_press=self.main_screen, size_hint=(1, 0.1)))
        self.add_widget(layout)

    def main_screen(self, *args):
        self.data[self.day]["lessons"][self.lesson]["task"] = self.text.text
        self.manager.current = 'main_screen'
        with open(f"{join(app.data_dir, 'data.json')}", 'w') as f:
            json.dump(self.data, f, indent=2)
        app.main_screen.data = self.data
        app.main_screen.buttons[self.day][self.lesson].text = self.text.text

    def upd(self):
        self.text.text = self.data[self.day]["lessons"][self.lesson]["task"]


class ScreenMain(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        now = datetime.datetime.weekday(datetime.datetime.now())
        self.day = 0 if now == 5 or now == 6 else now
        self.start_of_the_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        self.date = self.start_of_the_week + datetime.timedelta(days=self.day)
        if self.date < datetime.date.today():
            self.start_of_the_week += datetime.timedelta(days=7)
        self.buttons = []
        main_layout = Container()
        self.carousel = Carousel(loop=True)
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
            temp = []
            for j in range(len(self.data[i]["lessons"])):
                lesson = self.data[i]["lessons"][j]
                color = (0.23, 0.23, 0.23, 1) if j % 2 else (0.5, 0.5, 0.5, 1)
                card = GridLayout(rows=2)
                title = GridLayout(cols=2, size_hint_y=0.25)
                title.add_widget(MyLabel(text=f'{lesson["lesson"]}', bg_color=color))
                title.add_widget(MyLabel(text=f'{lesson["less_start"]}-{lesson["less_finish"]}', bg_color=color))
                card.add_widget(title)
                btn = MyButton(background_color=color, text=f'{lesson["task"]}', day=i, lesson=j)
                temp.append(btn)
                card.add_widget(btn)
                day_layout.add_widget(card)
            self.buttons.append(temp)
            self.carousel.add_widget(day_layout)
        self.carousel.index = self.day
        main_layout.add_widget(self.carousel)
        self.add_widget(main_layout)

    def text_edit(self, *args):
        self.manager.current = 'text_edit'

    def save(self, instance, value):
        self.data[instance.day]['lessons'][instance.lesson]['task'] = value


class DiaryApp(App):
    data_dir = App().user_data_dir

    def __init__(self):
        super().__init__()
        try:
            with open(f"{join(self.data_dir, 'data.json')}", encoding='utf-8') as file:
                self.data = json.load(file)
        except:
            self.data = [
                {'day': 'Понедельник',
                 'lessons': [{'lesson': '', 'less_start': '8:00', 'less_finish': '8:40', 'task': '17 вариант'},
                             {'lesson': 'общество', 'less_start': '8:50', 'less_finish': '9:30', 'task': ''},
                             {'lesson': 'математика', 'less_start': '9:50', 'less_finish': '10:30',
                              'task': '6.21-6.24'},
                             {'lesson': 'физкулътура', 'less_start': '10:50', 'less_finish': '11:30',
                              'task': ''},
                             {'lesson': 'физика', 'less_start': '11:45', 'less_finish': '12:25', 'task': ''},
                             {'lesson': 'икт', 'less_start': '12:40', 'less_finish': '13:20', 'task': ''},
                             {'lesson': 'математика', 'less_start': '13:30', 'less_finish': '14:10',
                              'task': ''}]}, {'day': 'Вторник', 'lessons': [
                    {'lesson': 'математика', 'less_start': '8:00', 'less_finish': '8:40', 'task': '18-24 в,г'},
                    {'lesson': 'математика', 'less_start': '8:50', 'less_finish': '9:30', 'task': ''},
                    {'lesson': 'французский', 'less_start': '9:50', 'less_finish': '10:30', 'task': '151-152 '},
                    {'lesson': 'физика', 'less_start': '10:50', 'less_finish': '11:30', 'task': '1.9-1.10'},
                    {'lesson': 'русский язык', 'less_start': '11:45', 'less_finish': '12:25', 'task': '320'},
                    {'lesson': 'литература', 'less_start': '12:40', 'less_finish': '13:20',
                     'task': 'жизнь обман с чарующей тоской'},
                    {'lesson': 'история', 'less_start': '13:30', 'less_finish': '14:10', 'task': ''},
                    {'lesson': 'внеурочка русский', 'less_start': '14:20', 'less_finish': '15:00', 'task': '2.8'}]},
                {'day': 'Среда',
                 'lessons': [{'lesson': 'математика', 'less_start': '8:00', 'less_finish': '8:40', 'task': ''},
                             {'lesson': 'физика', 'less_start': '8:50', 'less_finish': '9:30', 'task': ''},
                             {'lesson': 'икт', 'less_start': '9:50', 'less_finish': '10:30', 'task': ''},
                             {'lesson': 'родной язык', 'less_start': '10:50', 'less_finish': '11:30',
                              'task': ''},
                             {'lesson': 'литература', 'less_start': '11:45', 'less_finish': '12:25',
                              'task': ''},
                             {'lesson': 'астрономия', 'less_start': '12:40', 'less_finish': '13:20',
                              'task': '17-22'},
                             {'lesson': 'физкультура', 'less_start': '13:30', 'less_finish': '14:10',
                              'task': ''}]}, {'day': 'Четверг', 'lessons': [
                    {'lesson': 'французский', 'less_start': '8:00', 'less_finish': '8:40', 'task': ''},
                    {'lesson': 'общество', 'less_start': '8:50', 'less_finish': '9:30', 'task': ''},
                    {'lesson': 'математика', 'less_start': '9:50', 'less_finish': '10:30', 'task': '9.16, 9.20'},
                    {'lesson': 'практикум', 'less_start': '10:50', 'less_finish': '11:30',
                     'task': 'почему люди не понимают друг друга'},
                    {'lesson': 'обж', 'less_start': '11:45', 'less_finish': '12:25', 'task': ''},
                    {'lesson': 'физика', 'less_start': '12:40', 'less_finish': '13:20', 'task': '2.11-2.13'},
                    {'lesson': 'математика', 'less_start': '13:30', 'less_finish': '14:10', 'task': ''}]},
                {'day': 'Пятница', 'lessons': [
                    {'lesson': 'французский', 'less_start': '8:00', 'less_finish': '8:40', 'task': ''},
                    {'lesson': 'математика', 'less_start': '8:50', 'less_finish': '9:30',
                     'task': '8-13 под б.'},
                    {'lesson': 'физкулътура', 'less_start': '9:50', 'less_finish': '10:30', 'task': ''},
                    {'lesson': 'литература', 'less_start': '10:50', 'less_finish': '11:30', 'task': ''},
                    {'lesson': 'история', 'less_start': '11:45', 'less_finish': '12:25', 'task': ''},
                    {'lesson': 'физика', 'less_start': '12:40', 'less_finish': '13:20', 'task': ''},
                    {'lesson': 'икт', 'less_start': '13:30', 'less_finish': '14:10', 'task': ''},
                    {'lesson': ' русский платные', 'less_start': '14:20', 'less_finish': '15:00',
                     'task': '12 вар сенина'}]}]
        self.main_screen = ScreenMain(name='main_screen', data=self.data)
        self.text_edit = ScreenTextEdit(name='text_edit', data=self.data)

    def save(self):
        with open(f"{join(self.data_dir, 'data.json')}", 'w') as f:
            json.dump(self.data, f, indent=2)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(self.main_screen)
        sm.add_widget(self.text_edit)
        return sm


if __name__ == '__main__':
    app = DiaryApp()
    app.run()
