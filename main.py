import random

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
        self.text_keyboard = ''
        self.keys = ['1234567890', 'йцукенгшщзх', 'фывапролджэ', 'ячсмитьъбю<', ' .       # ']
        self.lessons = self.file[self.day]['lessons']
        self.cards_flag = True
        self.keyboards_flag = False
        self.swype = False
        self.swype_pos = ()
        self.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        self.date += datetime.timedelta(days=self.day)
        self.card_click_num = 0
        self.color = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(8)]
        #
        self.keyboard_text_size = int((width + height) / 3320 * 180)
        self.keyboard_y0 = int(height * (6 / 10))
        self.keyboard_height = int((height - self.keyboard_y0) / 5)
        self.cards_y0 = int((4 / 100) * (height - self.keyboard_height * 5))
        self.cards_height = int(height - self.cards_y0)
        self.cards_text_size = int((width + height) / 3320 * 60)
        self.card_height = int(self.cards_height / 8)
        self.card_text_obr = 32 if (width + height) == 3320 else 31

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
                        self.file[self.day]['lessons'][self.card_click_num]["task"] = self.text_keyboard
                        main.save()
                        self.text_keyboard = ''
                        self.cards_flag = True
                        self.keyboards_flag = False
                    else:
                        self.text_keyboard += y[x]
                    main.draw_all()

    def card_action(self, pos, click):
        for i in range(len(self.lessons)):
            y = self.cards_y0 + self.card_height * i
            if y < pos[1] < y + self.card_height and click == 0 and self.last_click == 1:
                self.keyboards_flag = True
                self.cards_flag = False
                self.card_click_num = i

    def action(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if not self.swype and self.last_click == 0 and click == 1:
            self.swype_pos = pos
            self.swype = True
        elif self.swype and self.last_click == 1 and click == 0:
            if pos[1] - self.swype_pos[1] < 0 and \
                    abs(pos[1] - self.swype_pos[1]) >= height * (1/6) and self.keyboards_flag:
                self.cards_flag = True
                self.keyboards_flag = False
            elif pos[0] - self.swype_pos[0] < 0 and\
                    abs(pos[0] - self.swype_pos[0]) >= width * (1/4) and self.cards_flag:
                self.day += 1
                self.day = 0 if self.day == 5 else self.day
                main.draw_all()
            elif pos[0] - self.swype_pos[0] > 0 and\
                    abs(pos[0] - self.swype_pos[0]) >= width * (1/4) and self.cards_flag:
                self.day -= 1
                self.day = 4 if self.day == -1 else self.day
            else:
                if self.keyboards_flag:
                    main.keyboard_action(pos, click)
                if self.cards_flag:
                    main.card_action(pos, click)
            self.swype = False
            main.draw_all()
        self.last_click = 0 if click == 0 else 1

    def keyboards_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, 0, width, height))
        last_dz = []
        new_dz = []
        task = self.lessons[self.card_click_num]["task"]
        while len(task) > 0:
            last_dz.append(task[:self.card_text_obr])
            task = task[self.card_text_obr:]
        text_keyboard = self.text_keyboard
        while len(text_keyboard) > 0:
            new_dz.append(text_keyboard[:self.card_text_obr])
            text_keyboard = text_keyboard[self.card_text_obr:]
        last_dz = [f'{self.file[self.day]["day"]} {self.date}', f'{self.lessons[self.card_click_num]["lesson"]}',
                   '', 'Старое домашнее задание:', *last_dz, '', 'Новое домашнее задание:', *new_dz]
        for i in range(len(last_dz)):
            text_print(message=last_dz[i],
                       x=(12 / 1000) * width + width / self.card_text_obr * (self.card_text_obr - len(last_dz[i])) / 2,
                       y=self.card_height / 5 * i,
                       font_size=self.cards_text_size
                       )

        for y in self.keys:
            for x in range(len(y)):
                keys_width = width / len(y)
                text_print(y[x],
                           x=keys_width * x,
                           y=self.keyboard_y0 + self.keyboard_height * self.keys.index(y) + self.keyboard_height / 15,
                           font_size=self.keyboard_text_size)

    def cards_draw(self):
        self.lessons = self.file[self.day]['lessons']
        text = f'{self.file[self.day]["day"]} {self.date}'
        x = (12 / 1000) * width
        text_print(message=text,
                   x=x + width / self.card_text_obr * (self.card_text_obr - len(text)) / 2,
                   y=0,
                   font_size=self.cards_text_size)
        for i in range(len(self.lessons)):
            y = self.cards_y0 + self.card_height * i
            pygame.draw.rect(display, (self.color[i]), (0, y, width, self.card_height))
            text_print(message=f'{self.lessons[i].get("time_start")}-{self.lessons[i].get("time_finish")}',
                       x=x,
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            text = f'{self.lessons[i].get("lesson")}'
            text_print(message=text,
                       x=x + width * (285 / 1000) + int(width * (715 / 1000) / 22 * (22 - len(text)) / 2),
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            task = self.lessons[i].get("task")
            num = 1
            while len(task) > 0:
                text_print(message=task[:self.card_text_obr],
                           x=x,
                           y=y + self.card_height * (12 / 100) + self.card_height / 5 * num,
                           font_size=self.cards_text_size)
                task = task[self.card_text_obr:]
                num += 1

    def draw_all(self):
        pygame.draw.rect(display, (43, 43, 43), (0, 0, width, height))
        self.date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        self.date += datetime.timedelta(days=self.day)
        if self.keyboards_flag:
            main.keyboards_draw()
        if self.cards_flag:
            main.cards_draw()
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
                lessons = day.split('/')
                if len(lessons) > 8:
                    print('Задать можно не более 8 уроков в день')
                    quit()
                for lesson in lessons:
                    lesson = lesson.split('-')
                    if len(lessons) > 3:
                        print('Ошибка в записи урока => (Название начало конец)')
                        quit()
                    self.file[days.index(day)]['lessons'].append(
                        {"lesson": lesson[0],
                         "time_start": lesson[1],
                         "time_finish": lesson[2],
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
