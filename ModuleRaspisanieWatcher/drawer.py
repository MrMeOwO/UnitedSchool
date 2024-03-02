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
        # draw.text((18 + xsize, 14), teacher, self.text_color, font=self.small_font)
        draw.text((18 + xsize, 34), cab, self.text_color, font=self.small_font)
        return img

    def gen_day(self, lessons: list[Image], lessons_in_day: int):
        img = Image.new("RGB",
                        (self.lesson_block_size_x, self.lesson_block_size_y * lessons_in_day),
                        self.bg_color)

        if len(lessons) < lessons_in_day:
            empty_lesson = self.gen_lesson("", "", "")
            for i in range(lessons_in_day-len(lessons)):
                lessons.append(empty_lesson)
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

    def add_caption(self, img: Image, caption: str) -> Image:
        new_image = Image.new("RGB", (img.size[0], img.size[1]+60), self.bg_color)
        new_image.paste(img, (0, 60))
        draw = ImageDraw.Draw(new_image)
        draw.text((img.size[0]/2, 30), caption, self.text_color, self.large_font, anchor="mm")
        return new_image

    def generate(self, class_data, caption):
        week = []
        max_lessons_in_day = 1
        for day_data in class_data:
            if len(day_data) >= max_lessons_in_day:
                max_lessons_in_day = len(day_data)

        for day_data in class_data:
            day = []
            for i in day_data:
                if len(i) > 4:
                    i = [i[0], i[1]+" / "+i[2], i[3]+" / "+i[4]]
                day.append(self.gen_lesson(*i))
            if day:
                week.append(self.gen_day(day, max_lessons_in_day))
        return self.add_caption(
            self.add_lesson_numbers(
                self.gen_week(
                    week, max_lessons_in_day
                ),
                max_lessons_in_day
            ),
            caption)

    def stack_images(self, data: list[Image]) -> Image:
        prev = Image.new("RGB", (0, 0), color=self.bg_color)
        for index, img in enumerate(data):

            size = [0, 0]
            if img.size[0] > prev.size[0]:
                size[0] = img.size[0]
            else:
                size[0] = prev.size[0]
            size[1] = img.size[1] + prev.size[1]
            past_pose = (0, prev.size[1])
            temp = prev
            prev = Image.new("RGB", size, color=self.bg_color)
            prev.paste(temp, (0, 0))
            prev.paste(img, past_pose)
        return prev
