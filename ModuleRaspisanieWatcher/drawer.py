from PIL import ImageFont, Image, ImageDraw


class ImageGenerator:
    lesson_block_size = (450, 60)
    lesson_block_size_x = lesson_block_size[0]
    lesson_block_size_y = lesson_block_size[1]

    text_color = (0, 0, 0)
    bg_color = (255, 255, 255)
    outline_color = (0, 0, 0)

    def __init__(self):
        self.small_font = ImageFont.truetype("/usr/share/fonts/gsfonts/NimbusSans-Regular.otf", 18)
        self.medium_font = ImageFont.truetype("/usr/share/fonts/gsfonts/NimbusSans-Regular.otf", 30)
        self.large_font = ImageFont.truetype("/usr/share/fonts/gsfonts/NimbusSans-Regular.otf", 50)

    def gen_lesson(self, lesson, teacher, cab):
        img = Image.new("RGB", self.lesson_block_size, self.bg_color)
        draw = ImageDraw.Draw(img)

        xsize = round(self.medium_font.getlength(lesson))  # y = 22 if font size is 30
        draw.rectangle(((0, 0), self.lesson_block_size), fill=self.bg_color, outline=self.outline_color, width=2)

        draw.text((10, 18), lesson, self.text_color, font=self.medium_font)
        draw.text((18 + xsize, 14), teacher, self.text_color, font=self.small_font)
        draw.text((18 + xsize, 34), cab, self.text_color, font=self.small_font)
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

    def add_lesson_numbers(self, image: Image, lessons_in_day=8):
        x, y = image.size
        new_img = Image.new("RGB",
                            (x + self.lesson_block_size_y, y),
                            color=self.bg_color)

        new_img.paste(image, (self.lesson_block_size_y, 0))
        draw = ImageDraw.Draw(new_img)

        for i in range(lessons_in_day):
            draw.rectangle((
                    (0, self.lesson_block_size_y * i),
                    (self.lesson_block_size_y, self.lesson_block_size_y * i + self.lesson_block_size_y)
                ),
                fill=self.bg_color, outline=self.outline_color, width=2)
            draw.text((30, self.lesson_block_size_y * i + 35), str(i + 1),
                      font=self.large_font, fill=self.text_color, anchor="mm")
        return new_img

    def generate(self, class_data):
        week = []
        for day_data in class_data:
            day = []
            for i in day_data:
                if len(i) > 4:
                    continue
                day.append(self.gen_lesson(*i))
            week.append(self.gen_day(day))
        return self.add_lesson_numbers(self.gen_week(week))
