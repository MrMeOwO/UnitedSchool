from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self, path: str):
        with open(path, 'r', encoding="windows-1251") as file:
            self.soup = BeautifulSoup(file.read(), "html.parser")

    def parse(self):
        classes = {}
        for clas in self.soup.findAll("table", attrs={"border": 1}):
            rasp = [[], [], [], [], [], []]
            for row in clas.findAll("tr", recursive=False)[1:]:
                for index, i in enumerate(row.findAll("td", recursive=False)[2:]):
                    temp = list(i.findAll("td"))
                    if len(temp) == 0:
                        continue
                    if len(temp) > 3:
                        temp = list(map(lambda x: x.text, temp))
                        temp.remove("/")
                        temp[1] = temp[1].replace(":1", "")
                        temp[2] = temp[2].replace(":2", "")
                        rasp[index].append(temp)
                    else:
                        rasp[index].append(list(map(lambda x: x.text, temp)))
            classes[clas.find("h2").text] = rasp
        return classes