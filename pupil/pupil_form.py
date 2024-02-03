import flet as ft


class PupilForm(ft.AlertDialog):
    def __init__(self, page, db, pupil_data=None, is_new=False):
        super().__init__()
        # self.on_dismiss = lambda e: print("PupilForm. dismiss", e.control)
        self.modal = True
        self.page = page
        self.db = db
        self.is_new = is_new
        if pupil_data is None:
            pupil_data = [0, "", "", "", "", "", "",1]
        self.id, name, surname, school, class_id, phone, parent_phones, is_active = pupil_data

        self.ref_name = ft.Ref[ft.TextField]()
        self.ref_surname = ft.Ref[ft.TextField]()
        self.ref_school = ft.Ref[ft.TextField]()
        self.ref_class_id = ft.Ref[ft.TextField]()
        self.ref_phone = ft.Ref[ft.TextField]()
        self.ref_parent_phones = ft.Ref[ft.TextField]()
        self.ref_is_active = ft.Ref[ft.Checkbox]()

        btn_save = ft.IconButton(icon="save", on_click=self.save_data)
        btn_delete = ft.IconButton(icon="delete", on_click=self.delete)
        btn_cancel = ft.IconButton(icon="cancel", on_click=self.close_form)

        self.content = ft.Container(
            height=330,
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Checkbox(
                                label_position=ft.LabelPosition.LEFT,
                                label='Актуален',
                                ref=self.ref_is_active,
                                value=True if is_active else False
                            )
                        ]
                    ),
                    ft.Container(
                        height=40,
                        content=ft.TextField(
                            ref=self.ref_name, label="Имя", value=name
                        ),
                    ),
                    ft.Divider(),
                    ft.Container(
                        height=40,
                        content=ft.TextField(
                            ref=self.ref_surname, label="Фамилия", value=surname
                        ),
                    ),
                    ft.Divider(),
                    ft.Row(controls=[
                            ft.Container(
                                height=40,
                                width=100,
                                content=ft.TextField(
                                    ref=self.ref_school, label="Школа", value=school
                                )
                            ),
                                ft.Container(
                                    height=40,
                                    width=100,
                                    content=ft.TextField(
                                        ref=self.ref_class_id,
                                        label="Класс", value=class_id
                                    )
                                )
                            ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(),
                    ft.Row(
                        height=40,
                        controls=[
                            ft.Container(
                                width=200,
                                content=ft.TextField(
                                    ref=self.ref_phone,
                                    prefix_text="+375 ",
                                    hint_text="Тел. 9 цифр (например: 291111111)",
                                    value=phone,
                                    on_submit=self.check_tel,
                                    on_change=self.count_symbols,
                                    on_focus=self.ready_input,
                                ),
                            ),
                            ft.Container(
                                on_click=lambda e: print(
                                    "viber://chat?number='+375297180386'"
                                ),
                                width=20,
                                height=20,
                                content=ft.Image(
                                    # src="https://www.flaticon.com/free-icons/viber-logo",
                                    # src=f"/assets/viber.svg",
                                    src="assets/viber.png",
                                    color="violet",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                            ),
                        ]
                    ),
                    ft.Divider(),
                    ft.Container(
                        height=80,
                        content=ft.TextField(
                            max_lines=2,
                            ref=self.ref_parent_phones,
                            label="Тел.родителей",
                            value=parent_phones,
                        ),
                    ),


                ],
            ),
        )
        self.title = ft.Text(
            style=ft.TextStyle(color="green", size=30, weight="bold"),
            value="Новый" if is_new else "Изменить"
        )


        self.actions = [
            btn_save,
            btn_delete,
            btn_cancel,
        ]

    def check_tel(self, e):
        tel = e.control.value
        if len(tel) == 9:
            e.control.value = tel
            e.control.update()

            e.control.value = f"({tel[0:2]}) {tel[2:5]}-{tel[5:7]}-{tel[7:9]}"
            e.control.update()
        else:
            self.page.snack_bar = ft.SnackBar(
                bgcolor="red",
                content=ft.TextField("Не менее 9 цифр, например 297654321 "),
            )
            self.page.snack_bar.open = True
            self.page.update()
        if len(tel) > 9:
            self.page.snack_bar = ft.SnackBar(
                bgcolor="red",
                content=ft.TextField("Не более 9 цифр, например 297654321 "),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def count_symbols(self, e):
        counter = len(e.control.value)
        if counter < 9:
            e.control.counter_text = f"Еще {max(0, 9 - counter)} цифр"
        else:
            e.control.counter_text = ""
        e.control.update()

    def close_form(self, e):
        self.page.dialog.open = False
        self.page.update()

    def ready_input(self, e):
        tel = e.control.value.replace(" ", "")
        tel = tel.replace("(", "")
        tel = tel.replace(")", "")
        tel = tel.replace("-", "")
        e.control.value = tel
        e.control.update()

    def save_data(self, e):
        pupil_data = [
            self.ref_name.current.value,
            self.ref_surname.current.value,
            self.ref_school.current.value,
            self.ref_class_id.current.value,
            self.ref_phone.current.value,
            self.ref_parent_phones.current.value,
            1 if self.ref_is_active.current.value else 0
        ]
        if self.is_new:
            self.db.pupil_create(pupil_data)
        else:
            self.db.pupils_update(self.id, pupil_data)

        self.page.dialog.open = False
        self.page.update()

    def delete(self, e):
        self.db.pupils_delete(self.id)
        self.page.dialog.open = False
        self.page.update()
