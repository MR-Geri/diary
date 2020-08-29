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

    def action(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text_print(message=str(click), x=20, y=100)

    def draw_all(self):
        pass

    def run(self):
        """ Запуск приложения """
        while True:
            pygame.draw.rect(display, (43, 43, 43), (0, 0, width, height))
            main.draw_all()
            main.action()
            for en in pygame.event.get():
                if en.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()


if __name__ == '__main__':
    # Инициализация
    width = 1080
    height = 2340
    pygame.init()
    display = pygame.display.set_mode((width, height))

    # Запуск
    main = Diary()
    main.run()
