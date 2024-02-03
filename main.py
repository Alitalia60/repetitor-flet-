import flet as ft
from datetime import date

import db.data_base as data_base
from genefal.Summary import Summary
from schedule.Lessons import Lessons
from pupil.pupils_table import PupilsTable
from settings.Settings import Settings


# ************************************ main
def main(page: ft.Page):
    month_year: date = date.today()
    selected_date = month_year
    db = data_base.DataBase()
    _table_pupils = PupilsTable(page, db)
    _schedule_cnt = Lessons(month_year, db, selected_date)
    _general = Summary(page, db, month_year)

    ref_tab_lessons = ft.Ref[ft.Tabs]()
    ref_tab_pupils = ft.Ref[ft.Tabs]()
    ref_tab_general = ft.Ref[ft.Tabs]()
    ref_tab_settings = ft.Ref[ft.Tabs]()

    def change_tab(e):
        # print("on_change_tab", e.control)
        if e.control.selected_index == 0:
            page.window_width = 500
            # pupils tab
            pass
        elif e.control.selected_index == 1:
            page.window_width = 500
            # lessons tab
            pass
        elif e.control.selected_index == 2:
            page.window_width = 1350
            _general.refresh_summary_table()
            _general.update()
            pass
        elif e.control.selected_index == 3:
            page.window_width = 500
            pass
        page.update()

    page.title = "Repetitor"
    page.window_width = 500
    page.theme_mode = "light"
    # page.window_center()

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    tab = ft.Tabs(
        on_change=change_tab,
        expand=True,
        selected_index=0,
        tabs=[
            ft.Tab(ref=ref_tab_pupils, text="Ученики", content=_table_pupils),
            ft.Tab(ref=ref_tab_lessons, text="Занятия", content=_schedule_cnt),
            ft.Tab(ref=ref_tab_general, text="Cвод", content=_general),
            ft.Tab(ref=ref_tab_settings, text="Настройки", content=Settings(page)),
        ],
    )

    page.add(tab)
    _schedule_cnt.refresh_lessons_list()
    page.update()


ft.app(target=main)
