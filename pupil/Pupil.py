import db.data_base as db


class Pupil:
    def __init__(self, name: str, surname: str, school: int, class_id: str) -> None:
        self.name = name
        self.surname = surname
        self.school = school
        self.class_id = class_id

    def add(self):
        pupil_data = [self.name, self.surname, self.school, self.class_id]
        db.DataBase.pupil_create(pupil_data)

    def edit(self, pupil_id, pupil_data):
        db.DataBase.update(pupil_id, pupil_data)

    def find(self, pupil_id):
        return db.DataBase.pupils_get_one(pupil_id)

    def pupils_delete(self, pupil_id):
        db.DataBase.pupils_delete(pupil_id)
