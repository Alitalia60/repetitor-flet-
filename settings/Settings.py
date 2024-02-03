import configparser

import flet as ft


class Settings(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        title = ft.Text("Настройки", text_align="center")
        return ft.Container(content=title)


class Settings1(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.init()
        # self.modal = False
        self.title = ft.Text("Настройки", text_align="center")
        self.tf_url = ft.TextField(label="url", value=self.url, color="white")
        self.tf_port = ft.TextField(
            label="port", value=self.port, text_align="end", color="white"
        )
        self.tf_room_target = ft.TextField(
            label="Комната", value=self.room_target, text_align="end", color="white"
        )
        self.tf_ttk_target = ft.TextField(
            label="ТТ котел", value=self.ttk_target, text_align="end", color="white"
        )

        self.actions = [
            ft.TextButton("Cancel", on_click=self.close_settings),
            ft.TextButton("Save", on_click=self.save_settings),
        ]

        self.content = ft.Container(
            bgcolor="blue",
            border_radius=10,
            margin=0,
            padding=10,
            # height=250,
            content=ft.Column(
                controls=[
                    self.tf_url,
                    self.tf_port,
                    ft.Divider(height=3, color="black"),
                    ft.Text(
                        value="Начальные значения температур",
                        text_align="center",
                        color="#FFFF00",
                        size=22,
                    ),
                    self.tf_room_target,
                    self.tf_ttk_target,
                ]
            ),
        )

    def init(self):
        self.url = " http://127.0.0.1"
        self.port = "5000"
        self.room_target = "18"
        self.ttk_target = "60"
        config = configparser.ConfigParser()
        rez = config.read("config.ini")
        print(rez)
        if rez:
            self.url = config["ServerURL"]["URL"]
            self.port = config["ServerURL"]["PORT"]
            self.room_target = config["Init"]["room_target"]
            self.ttk_target = config["Init"]["ttk_target"]
        else:
            # There's no config.ini else
            print("config.ini not found")

    def close_settings(self, e):
        self.open = False
        self.page.update()

    def save_settings(self, e):
        print(self.tf_room_target.value)
        print(self.tf_ttk_target.value)
        config = configparser.ConfigParser()
        config.add_section("ServerURL")
        config.add_section("Init")

        config.set("ServerURL", "URL", self.tf_url.value)
        config.set("ServerURL", "PORT", self.tf_port.value)
        config.set("Init", "room_target", self.tf_room_target.value)
        config.set("Init", "ttk_target", self.tf_ttk_target.value)
        with open("config.ini", "w") as config_file:
            config.write(config_file)

        self.open = False
        self.page.update()
