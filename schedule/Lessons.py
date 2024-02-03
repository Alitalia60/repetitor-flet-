import flet as ft
from my_calendar.calendar_module import Calendar
from schedule.Lesson_form import LessonForm


class Lessons(ft.UserControl):
    def __init__(self, month_year, db, selected_date) -> None:
        super().__init__()
        self.db = db
        self.month_year = month_year
        self.selected_date = month_year
        self.date_value = ft.Text(size=24, value=self.selected_date)
        self.lessons_list = ft.ListView(auto_scroll=True, spacing=10)
        self._lessons_view = ft.Container()
        self.selected_lesson_id = None

    def build(self):
        _current_date_cnt = ft.Stack(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=False,
                    padding=5,
                    border=ft.border.all(3),
                    border_radius=10,
                    bgcolor=ft.colors.GREY_600,
                    content=self.date_value,
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon="add",
                        icon_color="black",
                        bgcolor="blue",
                        on_click=lambda e: self.edit_lesson(True),
                    ),
                    offset=ft.Offset(0, 0.5),
                ),
            ]
        )

        _lessons_cnt = ft.Container(
            expand=True,
            border=ft.border.all(3),
            border_radius=10,
            content=self.lessons_list,
        )

        _calendar_cnt = Calendar(
            self.month_year, self.selected_date, self.on_day_select
        )

        self._lessons_view.content = ft.Column(
            controls=[
                _current_date_cnt,
                _lessons_cnt,
                _calendar_cnt,
            ]
        )

        return self._lessons_view

    def on_day_select(self, e):
        self.selected_date = e.control.data
        self.date_value.value = e.control.data
        self.refresh_lessons_list()
        self.date_value.update()
        self._lessons_view.update()

    def one_lesson(self, lesson_data: list):
        id, date, pupil_id, time, price, place = lesson_data
        lesson_cnt = ft.Container()
        lesson_cnt.data = lesson_data
        if lesson_cnt.data[0] == self.selected_lesson_id:
            lesson_cnt.border = ft.border.all(2, ft.colors.PINK_600)
        lesson_cnt.border_radius = 5
        lesson_cnt.on_click = self.on_lesson_select
        lesson_cnt.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(expand=False, content=ft.Text(size=30, value=time)),
                ft.VerticalDivider(width=20),
                ft.Container(
                    expand=True,
                    content=ft.Text(size=30, value=self.db.pupils_get_one(pupil_id)[1]),
                ),
                # ft.Text(size=30, value=price),
            ],
        )
        return lesson_cnt

    def refresh_lessons_list(self):
        lessons = self.db.lessons_get_by_date(self.selected_date)
        self.lessons_list.controls.clear()
        if lessons:
            for lesson in lessons:
                self.lessons_list.controls.append(self.one_lesson(lesson))
        self.lessons_list.update()

    def edit_lesson(self, is_new=False, lesson_data=None):
        # print("Schedule.edit_lesson.  lesson_data= ", lesson_data)
        if is_new:
            lesson_data = [self.selected_date, "", "", 0, ""]
            dlg = LessonForm(self.page, self.selected_date,
                              self.db, lesson_data, is_new)
        else:
            dlg = LessonForm(self.page, self.db, self.selected_date,  lesson_data)
        self.page.dialog = dlg
        self.page.dialog.open = True
        self.page.update()
        dlg.on_dismiss = lambda e: self.refresh_lessons_list()

    def on_lesson_select(self, e):
        self.selected_lesson_id = e.control.data[0]
        # print("Schedule.on_lesson_select ", e.control.data)
        self.edit_lesson(False, e.control.data)
