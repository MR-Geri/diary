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
        self.day = 0 if now == 5 or now == 6 else now
        #
        self.last_click = 0
        self.text_keyboard = ''
        self.keys = [
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
                [".", (98 // divider, 2060 // divider, 98 // divider, 180 // divider)],
                [' ', (196 // divider, 2060 // divider, 98 // divider * 7, 180 // divider)],
                ["#", (883 // divider, 2060 // divider, 98 // divider, 180 // divider)]
            ]
        ]
        self.height_block_keys = height // 2 - 220
        self.card_flag = True

    def keyboards_action(self, pos, click):
        for y in self.keys:
            for x in y:
                if x[1][0] < pos[0] < x[1][0] + x[1][2] and x[1][1] < pos[1] < x[1][1] + x[1][3] \
                        and click == 1 and self.last_click == 0:
                    if x[0] == '<':
                        self.text_keyboard = self.text_keyboard[:-1]
                    elif x[0] == '#':
                        self.text_keyboard += '\n'
                    else:
                        self.text_keyboard += x[0]
                    main.draw_all()

    def card_action(self, pos, click):
        pass

    def action(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        main.keyboards_action(pos, click)
        if self.card_flag:
            main.card_action(pos, click)
        self.last_click = 0 if click == 0 else 1

    def keyboards_draw(self):
        pygame.draw.rect(display, (60, 63, 65), (0, (height - self.height_block_keys), width, height))
        for y in self.keys:
            for x in y:
                pygame.draw.rect(display, (60, 63, 65), x[1])
                text_print(message=x[0], x=x[1][0], y=x[1][1], font_size=170 // divider)

    def card_draw(self):
        lessons = self.file[self.day]['lessons']
        date = datetime.date.today()
        date += datetime.timedelta(days=self.day)
        text_print(message=f'{self.file[self.day]["day"]} {date}', x=30, y=20, font_color=(255, 255, 255))
        for i in range(len(lessons)):
            x = 20 // divider
            y_size = ((height - self.height_block_keys - 40 // divider - 15) // 8)
            y = 60 + y_size * i
            pygame.draw.rect(display, (60, 63, 65), (
                x,
                y,
                width - 40 // divider,
                y_size - 10
            ))
            text_print(
                message=f'{lessons[i].get("time_start")}-{lessons[i].get("time_finish")}',
                x=x + 10, y=y + 10, font_size=30)

    def draw_all(self):
        pygame.draw.rect(display, (43, 43, 43), (0, 0, width, height))
        main.keyboards_draw()
        # text_print(message=self.text_keyboard, x=0, y=200, font_size=50)
        if self.card_flag:
            main.card_draw()
        pygame.display.update()

    def add_lesson(self):
        for index in [int(num) for num in input('День недели(0-4) через пробел: ').split()]:
            print(self.file[index]['day'])
            for les in range(int(input('Количество предметов: '))):
                self.file[index]['lessons'].append(
                    {"lesson": input('\tНазвание предмета: '),
                     "time_start": input('\tНачало урока: '),
                     "time_finish": input('\tКонец урока: '),
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
    divider = 1
    width = 1080 // divider
    height = 2240 // divider
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    main.run()
