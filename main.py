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
        self.keys = [
            [
                ["1", (0, 1340, 108, 180)],
                ["2", (108, 1340, 108, 180)],
                ["3", (216, 1340, 108, 180)],
                ["4", (324, 1340, 108, 180)],
                ["5", (432, 1340, 108, 180)],
                ["6", (540, 1340, 108, 180)],
                ["7", (648, 1340, 108, 180)],
                ["8", (756, 1340, 108, 180)],
                ["9", (864, 1340, 108, 180)],
                ["0", (972, 1340, 108, 180)]
            ],
            [
                ["й", (0, 1520, 98, 180)],
                ["ц", (98, 1520, 98, 180)],
                ["у", (196, 1520, 98, 180)],
                ["к", (294, 1520, 98, 180)],
                ["е", (392, 1520, 98, 180)],
                ["н", (490, 1520, 98, 180)],
                ["г", (589, 1520, 98, 180)],
                ["ш", (687, 1520, 98, 180)],
                ["щ", (785, 1520, 98, 180)],
                ["з", (883, 1520, 98, 180)],
                ["х", (981, 1520, 98, 180)]
            ],
            [
                ["ф", (0, 1700, 98, 180)],
                ["ы", (98, 1700, 98, 180)],
                ["в", (196, 1700, 98, 180)],
                ["а", (294, 1700, 98, 180)],
                ["п", (392, 1700, 98, 180)],
                ["р", (490, 1700, 98, 180)],
                ["о", (589, 1700, 98, 180)],
                ["л", (687, 1700, 98, 180)],
                ["д", (785, 1700, 98, 180)],
                ["ж", (883, 1700, 98, 180)],
                ["э", (981, 1700, 98, 180)]
            ],
            [
                ["я", (0, 1880, 98, 180)],
                ["ч", (98, 1880, 98, 180)],
                ["с", (196, 1880, 98, 180)],
                ["м", (294, 1880, 98, 180)],
                ["и", (392, 1880, 98, 180)],
                ["т", (490, 1880, 98, 180)],
                ["ь", (589, 1880, 98, 180)],
                ["ъ", (687, 1880, 98, 180)],
                ["б", (785, 1880, 98, 180)],
                ["ю", (883, 1880, 98, 180)],
                ["<", (981, 1880, 98, 180)]
            ],
            [
                [".", (98, 2060, 98, 180)],
                [' ', (196, 2060, 98 * 7, 180)],
                ["#", (883, 2060, 98, 180)]
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
        print()
        pygame.draw.rect(display, (60, 63, 65), (0, (height - self.height_block_keys), width, height))
        for y in self.keys:
            for x in y:
                pygame.draw.rect(display, (60, 63, 65), x[1])
                text_print(message=x[0], x=x[1][0], y=x[1][1], font_size=170)

    def card_draw(self):
        lessons = self.file[self.day]['lessons']
        date = datetime.date.today()
        date += datetime.timedelta(days=self.day)
        text_print(message=f'{self.file[self.day]["day"]} {date}', x=30, y=20, font_color=(255, 255, 255))
        for i in range(len(lessons)):
            x = 20
            y_size = ((height - self.height_block_keys - 40 - 15) // 8)
            y = 60 + y_size * i
            pygame.draw.rect(display, (60, 63, 65), (
                x,
                y,
                width - 40,
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
            with open('data/data.json', "w") as file:
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
    width = 1080
    height = 2240
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    main.run()
