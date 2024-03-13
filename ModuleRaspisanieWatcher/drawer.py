from PIL import ImageFont, Image, ImageDraw
from .parser import RaspisanieClass, Day, Lesson


class ImageGenerator:
    lesson_block_size = (450, 60)
    lesson_block_size_x = lesson_block_size[0]
    lesson_block_size_y = lesson_block_size[1]

    text_color = (0, 0, 0)
    bg_color = (255, 255, 255)
    outline_color = (0, 0, 0)

    timetable = [
        "08:00-08:40",
        "08:45-09:25",
        "09:30-10:10",
        "10:20-11:00",
        "11:05-11:45",
        "11:50-12:30",
        "12:35-13:15",
        "13:30-14:10",
        "14:15-14:55",
        "15:05-15:45",
        "15:50-16:30",
        "16:35-17:15",
        "17:20-18:00",
        "18:05-18:45",
    ]

    day_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    def __init__(self):
        self.small_font = ImageFont.truetype("NimbusSans-Regular.otf", 30)
        self.medium_font = ImageFont.truetype("NimbusSans-Regular.otf", 40)
        self.large_font = ImageFont.truetype("NimbusSans-Regular.otf", 50)

    def gen_lesson(self, lesson: Lesson):
        img = Image.new("RGB", self.lesson_block_size, self.bg_color)
        draw = ImageDraw.Draw(img)

        replace_data = {
                "Физическая культура": "Физ-ра",
                "Изобразительное искусство": "ИЗО",
                "Основы безопасности жизнедеятельности": "ОБЖ",
                "Вероятность и статистика": "Вероятн",
                "Россия мои горизонты": "Россия",
                "Ввведение в новейшую историю России": "Нов. история",
                "Проектная и иссследовательская деятельность": "ПИД",
                "Практикум по геометрии": "Практик",
                "Разговоры о важном": "Разговоры о важ.",
                "Английский язык": "Англ. яз",

                "Введение в профессию":"Вед.прф",
                "Искусство устной и письменной речи":"Иск.реч",
                "Подготовка к ЕГЭ по химии":"ЕГЭ хим",
                "Индивидуальный проект":"Инд.прк",
                "Человек-общество-мир":"Чел.общ",
                "Психология человека":"Психология",
                "Функции помогают уравнеиям":"фун.ур",
                "Подготовка к ЕГЭ по инфлрматике":"ЕГЭ информатика",
                "Практикум по биологии":"Пр.биол"
            }

        if lesson.name in replace_data.keys():
            lesson.name = replace_data[lesson.name]

        # TODO: replace hotfix with normal fix
        if "Некрылова" in lesson.cabinet:
            lesson.cabinet = ""
            print("WARN: Некрылова detected!!!")

        if type(lesson.teacher) is list:
            lesson.teacher = lesson.teacher[0] + "/" + lesson.teacher[1]

        if type(lesson.cabinet) is list:
            lesson.cabinet = lesson.cabinet[0] + "/" + lesson.cabinet[1]

        if lesson.name == "empty":
            lesson.name = ""
            lesson.cabinet = ""
            lesson.teacher = ""

        xsize = round(self.medium_font.getlength(lesson.name))  # y = 22 if font size is 30
        draw.rectangle(((0, 0), self.lesson_block_size), fill=self.bg_color, outline=self.outline_color, width=2)

        draw.text((10, self.lesson_block_size_y//2), lesson.name, self.text_color, font=self.medium_font, anchor="lm")
        draw.text((20 + xsize, self.lesson_block_size_y//2+3), lesson.cabinet, self.text_color, font=self.small_font, anchor="lm")
        return img

    def gen_day(self, lessons: list[Image]):
        img = Image.new("RGB",
                        (self.lesson_block_size_x, self.lesson_block_size_y * len(lessons)),
                        self.bg_color)

        for index, lesson in enumerate(lessons):
            img.paste(lesson, (0, self.lesson_block_size_y * index))

        return img

    def gen_week(self, days: list[Image], lessons_in_day=8):
        img = Image.new("RGB",
                        (self.lesson_block_size_x * len(days), self.lesson_block_size_y * lessons_in_day),
                        self.bg_color)

        for index, lesson in enumerate(days):
            img.paste(lesson, (self.lesson_block_size_x * index, 0))

        return img

    def add_lesson_numbers(self, image: Image, start: int, end: int, shift: int = 0):
        x, y = image.size
        new_img = Image.new("RGB",
                            (x + self.lesson_block_size_y, y),
                            color=self.bg_color)

        new_img.paste(image, (self.lesson_block_size_y, 0))
        draw = ImageDraw.Draw(new_img)

        for i in range(start, end):
            draw.rectangle((
                    (0, self.lesson_block_size_y * (i-start+shift)),
                    (self.lesson_block_size_y, self.lesson_block_size_y * (i-start+shift) + self.lesson_block_size_y)
                ),
                fill=self.bg_color, outline=self.outline_color, width=2)
            draw.text((30, self.lesson_block_size_y * (i-start+shift) + 35), str(i),
                      font=self.large_font, fill=self.text_color, anchor="mm")
        return new_img

    def add_time(self, image: Image, start: int, end: int, shift: int = 0):
        x, y = image.size
        new_img = Image.new("RGB",
                            (x + self.lesson_block_size_x//2, y),
                            color=self.bg_color)

        new_img.paste(image, (self.lesson_block_size_x//2, 0))
        draw = ImageDraw.Draw(new_img)

        for i in range(start, end):
            draw.rectangle((
                    (0, self.lesson_block_size_y * (i-start+shift)),
                    (self.lesson_block_size_x//2, self.lesson_block_size_y * (i-start+shift) + self.lesson_block_size_y)
                ),
                fill=self.bg_color, outline=self.outline_color, width=2)
            draw.text((self.lesson_block_size_x//4, self.lesson_block_size_y * (i-start+shift) + 35), self.timetable[i-1],
                      font=self.medium_font, fill=self.text_color, anchor="mm")
        return new_img

    def add_days_name(self, img: Image):
        new_img = Image.new("RGB", (img.size[0], img.size[1]+self.lesson_block_size_y), self.bg_color)
        new_img.paste(img, (0, self.lesson_block_size_y))
        draw = ImageDraw.Draw(new_img)
        for i in range(img.size[0]//self.lesson_block_size_x):
            pos = (self.lesson_block_size_x*i, 0)
            # draw.rectangle((pos, (pos[0]+self.lesson_block_size_x, pos[1]+self.lesson_block_size_y)), fill=self.bg_color, outline=self.outline_color, width=2)
            draw.text((pos[0]+self.lesson_block_size_x//2, pos[1]+self.lesson_block_size_y//2), self.day_names[i], font=self.large_font, fill=self.text_color, anchor="mm")
        return new_img

    def add_caption(self, img: Image, caption: str) -> Image:
        new_image = Image.new("RGB", (img.size[0], img.size[1]+60), self.bg_color)
        new_image.paste(img, (0, 60))
        draw = ImageDraw.Draw(new_image)
        draw.text((img.size[0]/2, 30), caption, self.text_color, self.large_font, anchor="mm")
        return new_image

    def generate(self, class_data: RaspisanieClass):
        days_img = []
        for day in class_data.days:
            lessons_img = []
            for lesson in day.lessons:
                lessons_img.append(self.gen_lesson(lesson))
            days_img.append(self.gen_day(lessons_img))

        week = self.add_days_name(self.gen_week(days_img, len(class_data.days[0].lessons)))
        week_with_lessons_number = self.add_lesson_numbers(week, class_data.start_lesson, class_data.start_lesson+len(class_data.days[0].lessons), 1)
        week_with_time = self.add_time(week_with_lessons_number, class_data.start_lesson, class_data.start_lesson+len(class_data.days[0].lessons), 1)
        return self.add_caption(week_with_time, class_data.class_name)

    def stack_images(self, data: list[Image]) -> Image:
        prev = Image.new("RGB", (0, 0), color=self.bg_color)
        for index, img in enumerate(data):

            size = [0, 0]
            if img.size[0] > prev.size[0]:
                size[0] = img.size[0]
            else:
                size[0] = prev.size[0]
            size[1] = img.size[1] + prev.size[1] + 50
            past_pose = (0, prev.size[1])
            temp = prev
            prev = Image.new("RGB", size, color=self.bg_color)
            prev.paste(temp, (0, 0))
            prev.paste(img, past_pose)
        return prev
