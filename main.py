import random

import pygame
import json
import datetime


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
        print(self.file)
        #
        now = datetime.datetime.weekday(datetime.datetime.now())
        self.day = 0 if now == 5 or now == 6 else now
        #
        self.last_click = 0
        self.text_keyboard = ''
        self.keys = ['1234567890', 'йцукенгшщзх', 'фывапролджэ', 'ячсмитьъбю<', ' .       # ']
        self.cards_flag = True
        self.keyboards_flag = False
        self.swype = False
        self.swype_pos = ()
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
                        and pos_y < pos[1] < pos_y + self.keyboard_height and click == 1 and self.last_click == 0:
                    if y[x] == '<':
                        self.text_keyboard = self.text_keyboard[:-1]
                    elif y[x] == '#':
                        self.text_keyboard += '\n'
                    else:
                        self.text_keyboard += y[x]
                    main.draw_all()

    def card_action(self, pos, click):
        pass

    def action(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if not self.swype and self.last_click == 0 and click == 1:
            self.swype_pos = pos[0]
            self.swype = True
        elif self.swype and self.last_click == 1 and click == 0:
            if pos[0] - self.swype_pos < 0 and abs(pos[0] - self.swype_pos) >= width * (1/4):
                print('Влево')
                self.day += 1
                self.day = 0 if self.day == 5 else self.day
                main.draw_all()
            elif pos[0] - self.swype_pos > 0 and abs(pos[0] - self.swype_pos) >= width * (1/4):
                print('Вправо')
                self.day -= 1
                self.day = 4 if self.day == -1 else self.day
                main.draw_all()
            else:
                if self.keyboards_flag:
                    main.keyboard_action(pos, click)
                if self.cards_flag:
                    main.card_action(pos, click)
            self.swype = False
        self.last_click = 0 if click == 0 else 1

    def keyboards_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, self.keyboard_y0, width, height - self.keyboard_y0))
        for y in self.keys:
            for x in range(len(y)):
                keys_width = width / len(y)
                text_print(y[x],
                           x=keys_width * x,
                           y=self.keyboard_y0 + self.keyboard_height * self.keys.index(y) + self.keyboard_height / 15,
                           font_size=self.keyboard_text_size)

    def card_draw(self):
        lessons = self.file[self.day]['lessons']
        date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        date += datetime.timedelta(days=self.day)
        text = f'{self.file[self.day]["day"]} {date}'
        text_print(message=text,
                   x=(2 / 100) * width + width / self.card_text_obr * (self.card_text_obr - len(text)) / 2,
                   y=0,
                   font_size=self.cards_text_size)
        for i in range(len(lessons)):
            x = (12 / 1000) * width
            y = self.cards_y0 + self.card_height * i
            pygame.draw.rect(display, (random.randint(0, 255), 43, 43), (0, y, width, self.card_height))
            text_print(message=f'{lessons[i].get("time_start")}-{lessons[i].get("time_finish")}',
                       x=x,
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            text = f'{lessons[i].get("lesson")}'
            text_print(message=text,
                       x=x + width * (285 / 1000) + int(width * (715 / 1000) / 22 * (22 - len(text)) / 2),
                       y=y + self.card_height * (12 / 100),
                       font_size=self.cards_text_size)
            task = lessons[i].get("task")
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
        if self.keyboards_flag:
            main.keyboards_draw()
        if self.cards_flag:
            main.card_draw()
        text_print(message=self.text_keyboard, x=0, y=200, font_size=50)
        pygame.display.update()

    def add_lesson(self):
        for index in [int(num) for num in input('День недели(0-4) через пробел: ').split()]:
            print(self.file[index]['day'])
            for les in range(int(input('Количество предметов: '))):
                self.file[index]['lessons'].append(
                    {"lesson": input('\tНазвание предмета: '),
                     "time_start": input('\tНачало урока: '),
                     "time_finish": input('\tКонец урока: '),
                     "task": "1234567890123456789012345678901234567890123456789012345678901234567890"}
                )
        for day in self.file:
            print(day)
        main.save()

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
    width = 1080 // 2
    height = 2240 // 2
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    main.run()
