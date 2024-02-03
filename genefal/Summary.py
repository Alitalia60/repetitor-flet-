import flet as ft
import calendar
from datetime import date, timedelta

from schedule.Lesson_form import LessonForm

months = {
    0: "январь",
    1: "февраль",
    2: "март",
    3: "апрель",
    4: "май",
    5: "июнь",
    6: "июль",
    7: "август",
    8: "сентябрь",
    9: "октябрь",
    10: "ноябрь",
    11: "декабрь",
}

cal = calendar.Calendar(firstweekday=0)


class Summary(ft.UserControl):
    def __init__(self, page, db, month_year: date):
        super().__init__()
        self.page = page
        self.db = db
        self.dt = None
        self.month_year = month_year
        self._period_name = ft.Text(
            value=f"{months[self.month_year.month - 1]} {self.month_year.year}"
        )

        self._period_name = ft.Text(
            value=f"{months[self.month_year.month - 1]} {self.month_year.year}"
        )
        self._btn_prev = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            data="prev",
            on_click=self.change_month,
        )
        self._btn_next = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            data="next",
            on_click=self.change_month,
        )

    def build(self):
        days: list = self.get_days_of_month(self.month_year)
        _btn_prev = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            data="prev",
            on_click=self.change_month,
        )
        _btn_next = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            data="next",
            on_click=self.change_month,
        )
        _change_period_cnt = ft.Container(
            content=ft.Row(controls=[_btn_prev, self._period_name, _btn_next])
        )
        self.dt = ft.DataTable(
            vertical_lines=ft.BorderSide(width=1, color="yellow"),
            heading_row_height=40,
            column_spacing=25,
            show_bottom_border=True,
        )

        self.refresh_summary_table()

        return ft.Container(content=ft.Column(controls=[_change_period_cnt, self.dt]))

    def refresh_summary_table(self):
        days: list = self.get_days_of_month(self.month_year)
        self.dt.columns.clear()
        self.dt.columns.append(ft.DataColumn(
                label=ft.Text("Ученик",
                text_align=ft.TextAlign.END,
                color="red")
            ))

        # for day in self.days:
        for day in days:
            _txt = ft.Text(day.day)
            if day.weekday() == 6:
                _txt.color = "red"
                _txt.bgcolor = "yellow"
                _txt.weight = ft.FontWeight.W_700
            self.dt.columns.append(ft.DataColumn(_txt))

        self.dt.rows.clear()
        start_day = self.month_year.replace(day=1)
        num_days = calendar.monthrange(self.month_year.year, self.month_year.month)[1]
        end_day = self.month_year.replace(day=num_days)
        pupils = self.db.lessons_get_pupils_at_month(start_day, end_day)

        if pupils:
            # Заполнение данных по ученикам
            for pupil in pupils:
                _row = ft.DataRow(data=pupil)
                _row.cells.append(ft.DataCell(ft.Text(value=pupil[1])))
                # for day in self.days:
                for day in days:
                    day_data = self.db.lessons_get_by_date_and_pupil(day, pupil[0])
                    # print("General. day_data=", day, day_data)
                    #             # Если день содержит занятие
                    cell_data = ft.Text("")
                    if day_data:
                        cell_data = ft.Container(
                            # data=int(day_data[2]),
                            alignment=ft.alignment.center,
                            width=20,
                            height=20,
                            border_radius=5,
                            bgcolor="green" if day_data[2] else ft.colors.PINK_100,
                            content=ft.Text(value=day_data[2] if day_data[2] else ""),
                        )
                    #
                    _row.cells.append(
                        ft.DataCell(
                            data=self.db.lessons_get_by_date_and_pupil(day, pupil[0]),
                            on_tap=self.edit_lesson,
                            content=cell_data,
                            # content=ft.Text("?"),
                        )
                    )
                self.dt.rows.append(_row)

        summary = ft.DataRow(color=ft.colors.AMBER_50)
        summary_title = ft.DataCell(
            content=ft.Text(
                "Итоги", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        summary.cells.append(summary_title)
        # for day in self.days:
        for day in days:
            day_sum = self.db.lessons_get_sum_at_date(day)
            if day_sum[0]:
                day_sum = int(day_sum[0])
            else:
                day_sum = ""
            summary.cells.append(ft.DataCell(content=ft.Text(value=day_sum)))

        self.dt.rows.append(summary)

    def change_month(self, e):
        if e.control.data == "prev":
            self.month_year = self.month_year - timedelta(days=15)
        else:
            self.month_year = self.month_year + timedelta(days=45)

        self.month_year = self.month_year.replace(day=1)
        self.refresh_summary_table()
        self._period_name.value = (
            f"{months[self.month_year.month - 1]} {self.month_year.year}"
        )
        self.update()

    def edit_lesson(self, e):
        lesson_data = self.db.lessons_get_by_id(e.control.data[0])
        dlg = LessonForm(self.page, self.db, lesson_data[1], lesson_data)
        self.page.dialog = dlg
        dlg.on_dismiss = self.on_dismiss
        dlg.open = True
        self.page.update()

    def on_dismiss(self,e):
        self.refresh_summary_table()
        self.dt.update()
    def get_days_of_month(self, date_of_month):
        days = []
        for day in cal.itermonthdates(date_of_month.year, date_of_month.month):
            if day.month == date_of_month.month and day.year == date_of_month.year:
                days.append(day)
        return days

    # def change_row_color(self, e):
    #     print(e.control)
    #     if e.control.selected:
    #         e.control.color = "orange"
