import random
import time

import pygame
import json
import datetime


def text_print(message, x, y, font_color=(255, 255, 255), font_size=30, font_type='data/shrift.otf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


class Diary:
    def __init__(self):
        #
        try:
            self.file = json.load(open('data/data.json'))
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
        now = 0 if now == 5 or now == 6 else now
        self.draw_data = self.file[now:] + self.file[:now]
        #
        self.last_click = 0
        self.text_keyboard = ''
        self.key = [
            [
                ["1", (0 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["2", (108 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["3", (216 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["4", (324 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["5", (432 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["6", (540 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["7", (648 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["8", (756 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["9", (864 // divider, 1340 // divider, 108 // divider, 180 // divider)],
                ["0", (972 // divider, 1340 // divider, 108 // divider, 180 // divider)]
            ],
            [
                ["й", (0 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["ц", (98 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["у", (196 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["к", (294 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["е", (392 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["н", (490 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["г", (589 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["ш", (687 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["щ", (785 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["з", (883 // divider, 1520 // divider, 98 // divider, 180 // divider)],
                ["х", (981 // divider, 1520 // divider, 98 // divider, 180 // divider)]
            ],
            [
                ["ф", (0 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["ы", (98 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["в", (196 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["а", (294 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["п", (392 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["р", (490 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["о", (589 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["л", (687 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["д", (785 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["ж", (883 // divider, 1700 // divider, 98 // divider, 180 // divider)],
                ["э", (981 // divider, 1700 // divider, 98 // divider, 180 // divider)]
            ],
            [
                ["я", (0 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["ч", (98 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["с", (196 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["м", (294 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["и", (392 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["т", (490 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["ь", (589 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["ъ", (687 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["б", (785 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["ю", (883 // divider, 1880 // divider, 98 // divider, 180 // divider)],
                ["<", (981 // divider, 1880 // divider, 98 // divider, 180 // divider)]
            ],
            [

            ]
        ]
        self.keys = ['1234567890', 'йцукенгшщзх', 'фывапролджэ', 'ячсмитьъбю<', '']
        self.h_keys = height // 2 - 220
        self.keyboards_flag = False

    def action(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if self.keyboards_flag:
            for y in range(len(self.keys)):
                for x in range(len(self.keys[y])):
                    _x = x * width // len(self.keys[y])
                    _y = (height - self.h_keys) + y * self.h_keys // len(self.keys)
                    if _x < pos[0] < _x + width // len(self.keys[y]) and _y < pos[1] < _y + self.h_keys // len(
                            self.keys) \
                            and click == 1 and self.last_click == 0:
                        if self.keys[y][x] == '<':
                            self.text_keyboard = self.text_keyboard[:-1]
                        else:
                            self.text_keyboard += self.keys[y][x]
            for x in [[0, '.'], [10 * width // 11, '\n']]:
                _y = (height - self.h_keys) + 4 * self.h_keys // len(self.keys)
                if x[0] < pos[0] < x[0] + width // 11 and _y < pos[1] < _y + self.h_keys // len(self.keys) \
                        and click == 1 and self.last_click == 0:
                    self.text_keyboard += x[1]

        if self.last_click == 0 and click == 1 and 0 < pos[1] < (height - self.h_keys):
            self.keyboards_flag = not self.keyboards_flag
        self.last_click = 0 if click == 0 else 1

    def keyboards_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, (height - self.h_keys), width, height))
        for y in range(len(self.keys)):
            for x in range(len(self.keys[y])):
                _x = x * width // len(self.keys[y])
                _y = (height - self.h_keys) + y * self.h_keys // len(self.keys)
                pygame.draw.rect(
                    display,
                    (60, 63, 65),
                    (_x, _y, width // len(self.keys[y]), self.h_keys // len(self.keys))
                )
                text_print(message=self.keys[y][x], x=_x, y=_y, font_size=170 // divider)
                print(f'["{self.keys[y][x]}", ({_x} // divider, {_y} // divider, {width // len(self.keys[y])} // divider, {self.h_keys // len(self.keys)} // divider)]')
            print()
        time.sleep(10)
        _x = 10 * width // 11
        _y = (height - self.h_keys) + 4 * self.h_keys // len(self.keys)
        pygame.draw.rect(display, (0, 0, 0), (_x, _y, width // len(self.keys[3]), self.h_keys // len(self.keys)))
        text_print(message='#', x=_x, y=_y, font_size=170 // divider)
        _x = 0
        pygame.draw.rect(display, (0, 0, 0), (_x, _y, width // len(self.keys[3]), self.h_keys // len(self.keys)))
        text_print(message='.',
                   x=_x + width // 11 // 10, y=_y - self.h_keys // len(self.keys) // 10,
                   font_size=170 // divider)

    def add_lesson(self):
        for index in [int(num) for num in input('День недели(0-4) через пробел: ').split()]:
            print(self.file[index]['day'])
            for les in range(int(input('Количество предметов: '))):
                self.file[index]['lessons'].append(
                    {"lesson": input('\tНазвание предмета: '),
                     "time_start": float(input('\tНачало урока: ')),
                     "task": "Домашнее задание"}
                )
        for day in self.file:
            print(day)
        main.save()

    def save(self):
        """ Сохранение данных в json"""
        try:
            with open('data/data.json', 'w') as file:
                json.dump(self.file, file, indent=2, ensure_ascii=False)
        except:
            print("ERROR save_json_data")

    def draw_all(self):
        pygame.draw.rect(display, (43, 43, 43), (0, 0, width, height))
        text_print(message=self.text_keyboard, x=0, y=200, font_size=50)
        if self.keyboards_flag:
            main.keyboards_draw()
        pygame.display.update()

    def run(self):
        """ Запуск приложения """
        while True:
            main.action()
            main.draw_all()
            for en in pygame.event.get():
                if en.type == pygame.QUIT:
                    pygame.quit()
                    quit()


if __name__ == '__main__':
    # Инициализация
    divider = 1
    width = 1080 // divider
    height = 2240 // divider
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    main.run()
