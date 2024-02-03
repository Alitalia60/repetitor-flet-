import flet as ft

from SearchBar.CastomSearchBar import CustomSearchBar


class LessonForm(ft.AlertDialog):
    def __init__(self, page, db, selected_date, lesson_data=None, is_new=False):
        super().__init__()
        self.modal = True
        self.page = page
        self.db = db
        self.selected_date = selected_date

        self.ref_search_pupil = ft.Ref[ft.SearchBar]()
        self.ref_date = ft.Ref[ft.Text]()
        self.ref_time = ft.Ref[ft.Text]()

        self.tf_date = ft.Container(
            on_click=self.pick_data,
            content=ft.TextField(
                ref=self.ref_date,
                width=130,
                expand=False,
                height=40,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="blue"),
                label="Дата",
            ),
        )

        _name = self.db.pupils_get_name(lesson_data[2])

        self.sb_pupil = CustomSearchBar(self.page, _name, self.db.pupils_get_all())

        # self.sb_pupil = ft.SearchBar(

        #     value=f"{_name[0]}, {_name[1]}" if _name else "выбрать ученика",
        #     ref=self.ref_search_pupil,
        #     height=40,
        #     bar_hint_text="имя ученика",
        #     on_change=self.search_pupil,
        #     on_submit=self.select_pupil,
        #     on_tap=self.search_tap,
        #     bar_overlay_color=ft.colors.AMBER,
        #     bar_trailing=[ft.Icon(name=ft.icons.QUESTION_MARK)]
        # )

        # self.sb_pupil.controls = [
        #     ft.ListTile(
        #         data=pupil,
        #         on_click=self.close_list,
        #         title=ft.Text(
        #             value=f"{pupil[1]}, {pupil[2]}"),
        #     )
        #     for pupil in self.db.pupils_get_all()
        # ]

        self.tf_time = ft.TextField(
            width=130,
            expand=False,
            height=40,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                color="blue",
            ),
            label="Время",
        )
        self.tf_price = ft.TextField(
            height=40,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="blue"),
            label="Цена",
        )
        self.tf_place = ft.TextField(
            height=40,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="blue"),
            label="Место",
        )
        self.is_new = is_new

        self.lesson_data = lesson_data
        if is_new:
            (
                self.ref_date.current.value,
                self.pupil_id,
                self.tf_time.value,
                self.tf_price.value,
                self.tf_place.value,
            ) = lesson_data
        else:
            (
                self.lesson_id,
                self.ref_date.current.value,
                self.pupil_id,
                self.tf_time.value,
                self.tf_price.value,
                self.tf_place.value,
            ) = lesson_data

        btn_save = ft.IconButton(icon="save", on_click=self.edit_data)
        btn_delete = ft.IconButton(icon="delete", on_click=self.delete)
        btn_cancel = ft.IconButton(icon="cancel", on_click=self.close_form)

        self.title = ft.Text("Новый" if is_new else "Изменить")
        self.content = ft.Container(
            height=330,
            width=300,
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        expand=False,
                        width=280,
                        controls=[
                            self.tf_date,
                            self.tf_time,
                        ],
                    ),
                    ft.Divider(),
                    self.sb_pupil,
                    ft.Divider(),
                    self.tf_price,
                    ft.Divider(),
                    self.tf_place,
                    ft.Divider(),
                ],
            ),
        )
        self.actions = [btn_save, btn_delete, btn_cancel]

    # ==================================
    def pick_data(self, e):
        dp = ft.DatePicker(
            first_date=self.selected_date,
        )
        self.page.overlay.append(dp)
        self.page.update()
        dp.pick_date()
        pass

    # ==================================

    def search_pupil(self, e):
        print("LessonForm.search_pupil", e.data)

    # ==================================

    def select_pupil(self, e):
        old_pupil = self.lesson_data[2]
        if not e.data:
            print("LessonForm.select_pupil. e.data", e.data)
            e.control.value = old_pupil

    # ==================================
    def search_tap(self, e):
        self.sb_pupil.open_view()

    # ==================================
    def close_list(self, e):
        name = e.control.data[1]
        self.pupil_id = e.control.data[0]
        self.sb_pupil.close_view(name)

    # ==================================
    def edit_data(self, e):
        lesson_data = (
            self.ref_date.current.value,
            self.pupil_id,
            self.tf_time.value,
            self.tf_price.value,
            self.tf_place.value,
        )
        if self.is_new:
            self.db.lesson_create(lesson_data)
        else:
            self.db.lesson_update(self.lesson_data[0], lesson_data)
        self.page.dialog.open = False
        self.page.update()

    # ==================================
    def delete(self, e):
        self.db.lesson_delete(self.lesson_data[0])
        self.close_form(e)

    # ==================================
    def close_form(self, e):
        self.page.dialog.open = False
        self.page.update()
