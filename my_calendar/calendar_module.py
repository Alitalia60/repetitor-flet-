import flet as ft
import calendar
from datetime import date, timedelta

cal = calendar.Calendar(firstweekday=0)
week_days = {
    0: "пнд",
    1: "втр",
    2: "срд",
    3: "чтв",
    4: "птн",
    5: "сбб",
    6: "вск",
}

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


class Calendar(ft.UserControl):
    def __init__(self, month_year, selected_date, on_day_select) -> None:
        super().__init__()
        self.selected_date = selected_date
        self.on_day_select = on_day_select
        self.month_year = month_year
        self._period_name = ft.Text(
            value=f"{months[self.month_year.month-1]} {self.month_year.year}"
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
        self._days_grid = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def DayOfCalendar(self, day):
        return ft.Container(
            content=ft.Text(
                value=day if day > 0 else None, text_align=ft.TextAlign.CENTER
            ),
            alignment=ft.alignment.center,
            width=30,
            height=30,
            border_radius=5,
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.GREY,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    def build(self):
        _nav_row = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self._btn_prev,
                    self._period_name,
                    self._btn_next,
                ],
            ),
        )

        _week_row = ft.Container(
            border=ft.border.only(bottom=ft.BorderSide(2, "black")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=30,
                        content=ft.Text(week_days[name_week_day]),
                    )
                    for name_week_day in cal.iterweekdays()
                ],
            ),
        )

        self._fill_days_grid(self.month_year)

        _main_container = ft.Container(
            expand=False,
            content=ft.Column(
                controls=[_nav_row, _week_row, self._days_grid],
            ),
            padding=10,
            border=ft.border.all(3, "black"),
            border_radius=10,
            height=300,
        )
        return _main_container

    def _fill_days_grid(self, month_year):
        self._days_grid.controls.clear()
        for week_number in range(
            0,
            len(cal.monthdayscalendar(year=month_year.year, month=month_year.month)),
        ):
            days_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            for day_of_week in cal.monthdayscalendar(
                year=month_year.year, month=month_year.month
            )[week_number]:
                box_day = self.DayOfCalendar(day_of_week)
                # box_day.on_click = self.on_day_select
                box_day.on_click = self.change_day
                box_day.data = day_of_week

                today = date.today()
                if day_of_week > 0:
                    if (
                        date(
                            year=month_year.year,
                            month=month_year.month,
                            day=day_of_week,
                        )
                        == today
                    ):
                        box_day.border = ft.border.all(2, "red")
                    box_day.data = date(
                        year=month_year.year, month=month_year.month, day=day_of_week
                    )
                if (
                    self.selected_date.day == day_of_week
                    and today.month == self.month_year.month
                ) and today.year == self.month_year.year:
                    box_day.bgcolor = "purple"
                days_row.controls.append(box_day)

            self._days_grid.controls.append(days_row)

    def change_month(self, e):
        if e.control.data == "prev":
            self.month_year = self.month_year - timedelta(days=15)
        else:
            self.month_year = self.month_year + timedelta(days=45)

        self.month_year = self.month_year.replace(day=1)
        self._fill_days_grid(self.month_year)
        self._period_name.value = (
            f"{months[self.month_year.month-1]} {self.month_year.year}"
        )
        self.update()

    def change_day(self, e):
        self.selected_date = e.control.data
        self.on_day_select(e)
        self._fill_days_grid(self.month_year)
        self._days_grid.update()
