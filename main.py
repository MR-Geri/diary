import pygame
import json
import datetime

width = 1080 // 2
height = 2240 // 2
set_lesson_flag = False


def text_print(message, x, y, font_color=(255, 255, 255), font_size=30, font_type='data/shrift.otf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (int(x), int(y)))


class Diary:
    def __init__(self):
        #
        try:
            with open('data/data.json') as f:
                self.file = json.load(f)
        except:
            self.file = [
                {
                    "day": "Понедельник",
                    "lessons": []
                },
                {
                    "day": "Вторник",
                    "lessons": []
                },
                {
                    "day": "Среда",
                    "lessons": []
                },
                {
                    "day": "Четверг",
                    "lessons": []
                },
                {
                    "day": "Пятница",
                    "lessons": []
                }
            ]
        #
        now = datetime.datetime.weekday(datetime.datetime.now())
        self.day = 0 if now == 5 or now == 6 else now
        #
        self.last_click = 0
        self.time_click = datetime.datetime.now()
        self.text_keyboard = ''
        self.keys = ['1234567890', 'йцукенгшщзх', 'фывапролджэ', ',ячсмитьбю<', ' :.     -# ']
        self.cards_flag = True
        self.add_task_flag = False
        self.keyboard_flag = False
        self.add_lesson_flag = False
        self.swype = False
        self.swype_pos = ()
        self.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())

        self.card_click_num = 0
        self.color = [(55, 55, 55) if i % 2 != 0 else (128, 128, 128) for i in range(8)]
        #
        self.name_lesson_flag = False
        self.less_start_flag = False
        self.less_finish_flag = False
        self.dz_flag = False
        self.name_lesson = []
        self.less_start = []
        self.less_finish = []
        self.dz = []
        #
        self.keyboard_text_size = int((width + height) / 3320 * 180)
        self.keyboard_y0 = int(height * (6 / 10))
        self.keyboard_height = int((height - self.keyboard_y0) / 5)
        self.cards_y0 = int((4 / 100) * (height - self.keyboard_height * 5))
        self.cards_height = int(height - self.cards_y0)
        self.cards_text_size = int((width + height) / 3320 * 60)
        font_type = pygame.font.Font('data/shrift.otf', self.cards_text_size)
        self.card_text_crop = int(width / font_type.render('а', True, (255, 255, 255)).get_width())
        self.card_height = int(self.cards_height / 8)

    def keyboard_action(self, pos, click):
        for y in self.keys:
            for x in range(len(y)):
                keys_width = width / len(y)
                pos_y = self.keyboard_y0 + self.keyboard_height * self.keys.index(y)
                if keys_width * x < pos[0] < keys_width * x + keys_width\
                        and pos_y < pos[1] < pos_y + self.keyboard_height and click == 0 and self.last_click == 1:
                    if y[x] == '<':
                        self.text_keyboard = self.text_keyboard[:-1]
                    elif y[x] == '#':
                        self.last_click = 0
                        if self.name_lesson_flag:
                            self.name_lesson_flag = False
                        elif self.less_start_flag:
                            self.less_start_flag = False
                        elif self.less_finish_flag:
                            self.less_finish_flag = False
                        elif self.dz_flag:
                            self.dz_flag = False
                        else:
                            if self.add_lesson_flag:
                                main.add_lesson_action()
                                self.cards_flag = True
                                self.add_lesson_flag = False
                                self.keyboard_flag = False
                            elif self.add_task_flag:
                                self.file[self.day]['lessons'][self.card_click_num]["task"] = self.text_keyboard
                                self.cards_flag = True
                                self.add_task_flag = False
                                self.keyboard_flag = False
                                main.save()
                        self.text_keyboard = ''
                    else:
                        self.text_keyboard += y[x]
                    main.draw_all()

    def card_action(self, pos, click):
        for i in range(len(self.file[self.day]["lessons"])):
            y = self.cards_y0 + self.card_height * i
            if y < pos[1] < y + self.card_height and click == 0 and self.last_click == 1:
                self.add_task_flag = True
                self.cards_flag = False
                self.keyboard_flag = True
                self.card_click_num = i
        if len(self.file[self.day]["lessons"]) < 8:
            y = self.cards_y0 + self.card_height * len(self.file[self.day]["lessons"])
            if y < pos[1] < y + self.card_height and self.last_click == 1 and click == 0:
                #
                self.name_lesson_flag = True
                self.less_start_flag = True
                self.less_finish_flag = True
                self.dz_flag = True
                self.name_lesson = []
                self.less_start = []
                self.less_finish = []
                self.dz = []
                #
                self.add_lesson_flag = True
                self.keyboard_flag = True
                self.cards_flag = False

    def add_lesson_action(self):
        start = ''.join(self.less_start)
        finish = ''.join(self.less_finish)
        try:
            with open('data/time.json') as f:
                time = json.load(f)
            start = start if len(start) > 0 else time[str(len(self.file[self.day]['lessons']))][0]
            finish = finish if len(finish) > 0 else time[str(len(self.file[self.day]['lessons']))][1]
        except:
            pass
        self.file[self.day]['lessons'].append(
            {"lesson": ''.join(self.name_lesson),
             "less_start": start,
             "less_finish": finish,
             "task": ''.join(self.dz)}
        )
        main.save()

    def action(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if not self.swype and self.last_click == 0 and click == 1:
            self.time_click = datetime.datetime.now()
            self.swype_pos = pos
            self.swype = True
            main.draw_all()
        elif self.swype and self.last_click == 1 and click == 0:
            if pos[1] - self.swype_pos[1] < 0 and \
                    abs(pos[1] - self.swype_pos[1]) >= height * (1/6) and (self.add_task_flag or self.add_lesson_flag):
                self.cards_flag = True
                self.add_task_flag = False
                self.add_lesson_flag = False
                self.keyboard_flag = False
                self.name_lesson_flag = False
                self.less_start_flag = False
                self.less_finish_flag = False
                self.dz_flag = False
            elif pos[0] - self.swype_pos[0] < 0 and\
                    abs(pos[0] - self.swype_pos[0]) >= width * (1/4) and self.cards_flag:
                self.day += 1
                self.day = 0 if self.day == 5 else self.day
                main.draw_all()
            elif pos[0] - self.swype_pos[0] > 0 and\
                    abs(pos[0] - self.swype_pos[0]) >= width * (1/4) and self.cards_flag:
                self.day -= 1
                self.day = 4 if self.day == -1 else self.day
            elif (datetime.datetime.now() - self.time_click).microseconds >= 300000:
                if self.add_task_flag or self.add_lesson_flag:
                    main.keyboard_action(pos, click)
                if self.cards_flag:
                    main.card_action(pos, click)
            self.swype = False
            main.draw_all()

        self.last_click = 0 if click == 0 else 1

    def add_task_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, 0, width, height))
        last_dz = []
        new_dz = []
        task = self.file[self.day]["lessons"][self.card_click_num]["task"]
        while len(task) > 0:
            last_dz.append(task[:self.card_text_crop])
            task = task[self.card_text_crop:]
        text_keyboard = self.text_keyboard
        while len(text_keyboard) > 0:
            new_dz.append(text_keyboard[:self.card_text_crop])
            text_keyboard = text_keyboard[self.card_text_crop:]
        data_print = [f'{self.file[self.day]["day"]} {self.date}',
                      f'{self.file[self.day]["lessons"][self.card_click_num]["lesson"]}',
                      '', 'Старое домашнее задание:', *last_dz, '', 'Новое домашнее задание:', *new_dz]
        for i in range(len(data_print)):
            text_print(message=data_print[i],
                       x=(12 / 1000) * width + width / self.card_text_crop * (
                                   self.card_text_crop - len(data_print[i])) / 2,
                       y=self.card_height / 5 * i,
                       font_size=self.cards_text_size
                       )

    def add_lesson_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, 0, width, height))
        if self.name_lesson_flag:
            self.name_lesson = []
            text_keyboard = self.text_keyboard
            while len(text_keyboard) > 0:
                self.name_lesson.append(text_keyboard[:self.card_text_crop])
                text_keyboard = text_keyboard[self.card_text_crop:]
        elif self.less_start_flag:
            self.less_start = []
            text_keyboard = self.text_keyboard
            while len(text_keyboard) > 0:
                self.less_start.append(text_keyboard[:self.card_text_crop])
                text_keyboard = text_keyboard[self.card_text_crop:]
        elif self.less_finish_flag:
            self.less_finish = []
            text_keyboard = self.text_keyboard
            while len(text_keyboard) > 0:
                self.less_finish.append(text_keyboard[:self.card_text_crop])
                text_keyboard = text_keyboard[self.card_text_crop:]
        elif self.dz_flag:
            self.dz = []
            text_keyboard = self.text_keyboard
            while len(text_keyboard) > 0:
                self.dz.append(text_keyboard[:self.card_text_crop])
                text_keyboard = text_keyboard[self.card_text_crop:]
        data_print = [
            f'{self.file[self.day]["day"]} {self.date}',
            ['Название урока:', (0, 255, 0) if self.name_lesson_flag else (255, 255, 255)],
            *self.name_lesson,
            '',
            ['Время начала урока:',
             (0, 255, 0) if self.less_start_flag and not self.name_lesson_flag else (255, 255, 255)],
            *self.less_start,
            '',
            ['Время окончания урока:',
             (0, 255, 0) if self.less_finish_flag and not self.less_start_flag else (255, 255, 255)],
            *self.less_finish,
            '',
            ['Домашнее задание:',
             (0, 255, 0) if self.dz_flag and not self.less_finish_flag else (255, 255, 255)],
            *self.dz
        ]
        for i in range(len(data_print)):
            color = (255, 255, 255) if type(data_print[i]) == str else data_print[i][1]
            text = data_print[i] if type(data_print[i]) == str else data_print[i][0]
            text_print(message=text,
                       x=width / self.card_text_crop * (self.card_text_crop - len(text)) / 2,
                       y=self.card_height / 5 * i,
                       font_size=self.cards_text_size,
                       font_color=color
                       )

    def keyboards_draw(self):
        for y in self.keys:
            for x in range(len(y)):
                keys_width = width / len(y)
                text_print(y[x],
                           x=keys_width * x,
                           y=self.keyboard_y0 + self.keyboard_height * self.keys.index(y) + self.keyboard_height / 15,
                           font_size=self.keyboard_text_size)

    def cards_draw(self):
        self.file[self.day]["lessons"] = self.file[self.day]['lessons']
        text = f'{self.file[self.day]["day"]} {self.date}'
        x = (12 / 1000) * width
        text_print(message=text,
                   x=width / self.card_text_crop * (self.card_text_crop - len(text)) / 2,
                   y=0,
                   font_size=self.cards_text_size)
        for i in range(len(self.file[self.day]["lessons"])):
            y = self.cards_y0 + self.card_height * i
            pygame.draw.rect(display, (self.color[i]), (0, y, width, self.card_height))
            text_print(message=f'{self.file[self.day]["lessons"][i].get("less_start")}-'
                               f'{self.file[self.day]["lessons"][i].get("less_finish")}',
                       x=x,
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            text = f'{self.file[self.day]["lessons"][i].get("lesson")}'
            text_print(message=text,
                       x=width * (285 / 1000) +
                         int(width * (715 / 1000) / self.card_text_crop * (self.card_text_crop - len(text)) / 2),
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            task = self.file[self.day]["lessons"][i].get("task")
            num = 1
            while len(task) > 0:
                text_print(message=task[:self.card_text_crop],
                           x=x,
                           y=y + self.card_height * (12 / 100) + self.card_height / 5 * num,
                           font_size=self.cards_text_size)
                task = task[self.card_text_crop:]
                num += 1
        if len(self.file[self.day]["lessons"]) < 8:
            pygame.draw.rect(display, self.color[len(self.file[self.day]["lessons"])],
                             (0, self.cards_y0 + self.card_height * len(self.file[self.day]["lessons"]),
                              width, self.card_height))
            text = 'Добавить урок'
            text_print(text,
                       x=width / self.card_text_crop * (self.card_text_crop - len(text)) / 2,
                       y=self.cards_y0 + self.card_height * (len(self.file[self.day]["lessons"])) +
                         self.card_height * (12 / 100) + self.card_height / 5 * 1.5,
                       font_size=self.cards_text_size
                       )

    def draw_all(self):
        pygame.draw.rect(display, (43, 43, 43), (0, 0, width, height))
        self.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        self.date += datetime.timedelta(days=self.day)
        if self.date < datetime.date.today():
            self.date += datetime.timedelta(days=7)
        if self.add_task_flag:
            main.add_task_draw()
        if self.cards_flag:
            main.cards_draw()
        if self.add_lesson_flag:
            main.add_lesson_draw()
        if self.keyboard_flag:
            main.keyboards_draw()
        pygame.display.update()

    def set_lesson(self):
        try:
            self.file = [
                {
                    "day": "Понедельник",
                    "lessons": []
                },
                {
                    "day": "Вторник",
                    "lessons": []
                },
                {
                    "day": "Среда",
                    "lessons": []
                },
                {
                    "day": "Четверг",
                    "lessons": []
                },
                {
                    "day": "Пятница",
                    "lessons": []
                }
            ]
            days = open('data/schedule.text', encoding='utf-8').read().split('\n')
            if len(days) > 5:
                print('Задать можно не более 5 учебных дней')
                quit()
            for day in days:
                if day != '':
                    lessons = day.split('/')
                    if len(lessons) > 8:
                        print('Задать можно не более 8 уроков в день')
                        quit()
                    for lesson in lessons:
                        lesson = lesson.split('-')
                        if len(lesson) > 3:
                            print('Ошибка в записи урока => (Название начало конец)')
                            quit()
                        self.file[days.index(day)]['lessons'].append(
                            {"lesson": lesson[0],
                             "less_start": lesson[1],
                             "less_finish": lesson[2],
                             "task": ""}
                        )
            main.save()
            print('Расписание установлено')
        except:
            print('Ошибка в установке расписания. Ознакомьтесь с правилами записи в README.md')

    def save(self):
        """ Сохранение данных в json"""
        try:
            with open('data/data.json', 'w') as f:
                json.dump(self.file, f, indent=2)
        except:
            print("ERROR save_json_data")

    def run(self):
        """ Запуск приложения """
        main.draw_all()
        while True:
            main.action()
            for en in pygame.event.get():
                if en.type == pygame.QUIT:
                    pygame.quit()
                    quit()


if __name__ == '__main__':
    # Инициализация
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    if set_lesson_flag:
        main.set_lesson()
    main.run()
