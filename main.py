from ModuleRaspisanieWatcher import HtmlParser, ImageGenerator

parser = HtmlParser("/home/ivan/test.html")
data = parser.parse()
gen = ImageGenerator()
temp = []
for key, value in data.items():
    temp.append(gen.generate(value, key))
for index in range(len(temp)//3):
    index += 1
    gen.stack_images(temp[index*3-3:index*3]).save(f"test{index}.png")
