import os
import tomllib
import requests


class AbstractNotifierSender:
    def __init__(self, data: str):
        self.data = data

    def send_text(self, text: str): ...
    def send_image(self, image_path: str): ...


class NotifierException(Exception): pass
class TelegramNotifierException(NotifierException): pass


class TelegramNotifierSender(AbstractNotifierSender):
    def send_text(self, text: str):
        token, chat_id = self.data.split("|")
        req = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                            data={"chat_id": chat_id, "text": text}).json()
        if not req["ok"]:
            raise TelegramNotifierException(req["description"])

    def send_image(self, image_path: str):
        token, chat_id = self.data.split("|")
        with open(image_path, "rb") as file:
            img = file.read()
        req = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto",
                            data={"chat_id": chat_id}, files={"photo": img}).json()
        if not req["ok"]:
            raise TelegramNotifierException(req["description"])


class Notifier:

    type_link = {
        "telegram": TelegramNotifierSender
    }

    def __init__(self, config_path):
        self.classes = {}
        with open(config_path, "rb") as file:
            raw_config = tomllib.load(file)
        for target in raw_config["target"]:
            self.classes[target['name']] = {'type': target['type'], 'data': target['data']}

    def send_text(self, clas, text: str):
        self.type_link[self.classes[clas]["type"]](self.classes[clas]["data"]).send_text(text)

    def send_image(self, clas, image_path):
        self.type_link[self.classes[clas]["type"]](self.classes[clas]["data"]).send_image(image_path)
