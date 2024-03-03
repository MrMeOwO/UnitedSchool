from ModuleRaspisanieWatcher import HtmlParser, ImageGenerator

parser = HtmlParser("rasp.html")
data = parser.parse()
print("data loaded")
gen = ImageGenerator()

groups = []
last_class = ""
for item in data:
    if item.class_name[:-1] != last_class:
        groups.append([])
        groups[-1].append(item)
        last_class = item.class_name[:-1]
    else:
        groups[-1].append(item)

for classes in groups:
    print(classes)
    group_type = classes[0].class_name[:-1]
    for index, i in enumerate([classes[i:i + 3] for i in range(0, len(classes), 3)]):
        temp = []
        for item in i:
            temp.append(gen.generate(item))
        gen.stack_images(temp).save(f"img/{group_type}_{index}.png")

