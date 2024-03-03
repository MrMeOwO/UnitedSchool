from bs4 import BeautifulSoup
import rich


class Lesson:
    name: str
    teacher: str | list[str, str]
    cabinet: str | list[str, str]

    def __repr__(self):
        return f"<{self.name}|{self.teacher}|{self.cabinet}>"


class Day:
    name: str
    lessons: list[Lesson] = []

    def __repr__(self):
        return f"---{self.name}---"+'\n\t'+'\n\t'.join([str(i) for i in self.lessons])


class RaspisanieClass:
    class_name: str
    start_lesson: int
    days: list[Day] = []

    def __repr__(self):
        return f"<{self.class_name}>"


class HtmlParser:
    def __init__(self, path: str):
        with open(path, 'r', encoding="windows-1251") as file:
            self.soup = BeautifulSoup(file.read(), "html.parser")

    def parse(self) -> list[RaspisanieClass]:
        classes = []
        for clas in self.soup.findAll("table", attrs={"border": 1}):
            rasp = RaspisanieClass()
            rasp.class_name = clas.find("h2").text
            rasp.days = []
            rasp.start_lesson = min([int(i.text) if i.text.isdigit() else 999 for i in clas.findAll("strong")])

            days_names = [i.find("strong").text for i in clas.find("tr").findAll("td")][2:]
            for i in days_names:
                day = Day()
                day.name = i
                day.lessons = []
                rasp.days.append(day)

            for row in clas.findAll("tr", recursive=False)[1:]:
                for day_index, item in enumerate(row.findAll("td", recursive=False)[2:]):
                    temp = [i.text for i in item.findAll("td")]
                    lesson = Lesson()
                    if len(temp) == 3:
                        lesson.name = temp[0]
                        lesson.teacher = temp[1]
                        lesson.cabinet = temp[2]
                    elif len(temp) == 6:
                        if "/" in temp:
                            temp.remove("/")
                            lesson.name = temp[0]
                            lesson.teacher = [temp[1], temp[2]]
                            lesson.cabinet = [temp[3], temp[4]]
                        else:
                            lesson.name = temp[0]+temp[2]
                            lesson.teacher = [temp[1], temp[3]]
                            lesson.cabinet = [temp[4], temp[5]]

                    elif len(temp) == 0:
                        lesson.name = "empty"
                        lesson.teacher = "empty"
                        lesson.cabinet = "empty"
                    else:
                        raise Exception(f"error while parse. temp = {temp}")
                    rasp.days[day_index].lessons.append(lesson)
            classes.append(rasp)
        return classes


if __name__ == '__main__':
    parser = HtmlParser("../rasp.html")
    rich.print(parser.parse())
