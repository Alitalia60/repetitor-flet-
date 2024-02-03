import flet as ft

from pupil.pupil_form import PupilForm

# ************************************ PupilTable
class PupilsTable(ft.UserControl):
    def __init__(self, page, db):
        super().__init__()
        self.page = page
        self.db = db
        self.dt = ft.DataTable()
        self._main_cnt = ft.Container(
            content=ft.Stack(controls=[
                self.dt,
                ft.Container(
                    content=ft.IconButton(
                        icon="add",
                        icon_color="black",
                        bgcolor="blue",
                        on_click=lambda e: self.edit_pupil(e, True),
                    ),
                    offset=ft.Offset(0, 1),
                ),
            ]))

    # **************************
    def PupilRow(self, pupil_data: list):
        (self.id, name, surname, school, class_id, phone, parent_phones, is_active) = pupil_data

        return ft.DataRow(
            data=pupil_data,
            on_long_press=lambda e: self.edit_pupil(e, False, pupil_data),
            cells=[
                ft.DataCell(ft.Text(value=f"{name} {surname}", color="red")),
                ft.DataCell(ft.Text(school)),
                ft.DataCell(ft.Text(phone)),
            ],
        )

    def fill_pupils_table(self,e):
        self.dt.rows.clear()
        all_pupils = self.db.pupils_get_all()
        for pupil in all_pupils:
            self.dt.rows.append(self.PupilRow(pupil))
        self._main_cnt.update()

    def edit_pupil(self,e, is_new=False, pupil_data=None):
        edit_dlg = PupilForm(self.page, self.db, pupil_data, is_new)
        self.page.dialog = edit_dlg
        edit_dlg.open = True
        self.page.update()
        edit_dlg.on_dismiss = self.fill_pupils_table

    def build(self):

        headers = [
            {"name": "Имя", "width": 100},
            {"name": "Школа", "width": 60},
            {"name": "Тел.", "width": 50},
        ]
        self.dt.border_radius=10
        self.dt.column_spacing=0
        self.dt.width=550
        self.dt.checkbox_horizontal_margin=5
        self.dt.border=ft.border.all(2, "brown")
        self.dt.columns=[ft.DataColumn(ft.Text(col_name["name"])) for col_name in headers]
        self.dt.divider_thickness=0
        self.dt.data_row_min_height=30

        all_pupils = self.db.pupils_get_all()
        for pupil in all_pupils:
            self.dt.rows.append(self.PupilRow(pupil))
        return self._main_cnt
