import sqlite3
from sqlite3 import Error

database_name = "db/database.db"


class DataBase:
    def __init__(self):
        self.connection = None
        self.cur = None
        self.database_name = database_name
        try:
            self.connection = sqlite3.connect(
                self.database_name, check_same_thread=False
            )

        except Error as error:
            self.error_message(f"Ошибка открытия БД \n ({error})")

        self.cur = self.connection.cursor()
        query = 'CREATE TABLE IF NOT EXISTS "pupils" ("id" INTEGER UNIQUE, "name" TEXT, "surname" TEXT, "school" INTEGER, "class_id" TEXT, "phone" TEXT, "parent_phones" TEXT, "is_active" INTEGER DEFAULT (1), PRIMARY KEY("id" AUTOINCREMENT))'

        try:
            self.cur.execute(
                query
                # "CREATE TABLE IF NOT EXISTS pupils (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, "
                # "school INTEGER, class_id TEXT, phone TEXT, parent_phones TEXT, is_active INTEGER DEFAULT 1, "
                # "FOREIGN KEY(id) REFERENCES lessons (pupil_id) ON DELETE CASCADE,  FOREIGN KEY(id) REFERENCES "
                # "accounts (pupil_id) ON DELETE CASCADE)"
            )
        except Error as error:
            self.error_message(f"Ошибка создания PUPILS \n ({error})")

        query = "CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT , date TEXT, pupil_id INTEGER REFERENCES pupils (id) ON DELETE CASCADE, time TEXT, price INTEGER  DEFAULT 0, place TEXT)"
        try:
            self.cur.execute(
                query
                # "CREATE TABLE IF NOT EXISTS lessons (id INTEGER, date TEXT, pupil_id INTEGER, time TEXT, price INTEGER, place TEXT, PRIMARY KEY(id AUTOINCREMENT))"
            )
        except Error as error:
            self.error_message(f"Ошибка создания LESSONS \n ({error})")

        query = "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, pupil_id INTEGER REFERENCES pupils (id) ON DELETE CASCADE, date TEXT, sum_dt INTEGER, sum_kt INTEGER)"
        try:
            self.cur.execute(
                query
                # "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, pupil_id INTEGER, date TEXT, sum_dt INTEGER, sum_kt INTEGER)"
            )
        except Error as error:
            self.error_message(f"Ошибка создания PUPILS \n ({error})")

    # =======================

    def error_message(self, message):
        print("************************************")
        print(message)

    # =======================

    def pupil_create(self, pupil_data):
        (
            name,
            surname,
            school,
            class_id,
            phone,
            parent_phones,
            is_active,
        ) = pupil_data
        try:
            self.cur.execute(
                f"INSERT INTO pupils (name, surname, school, class_id, phone, parent_phones ) VALUES ('{                    name}', '{surname}', '{school}','{class_id}', '{phone}' , '{parent_phones}')"
                # f"INSERT INTO pupils (name, surname) VALUES ('{name}', '{surname}')"
            )
            self.connection.commit()

        except Error as error:
            self.error_message(f"db.pupil_create Ошибка создания pupil \n {error}")

        # self.connection.close()

    # =======================
    def pupils_get_all(self):
        # self.cur = self.connection.cursor()
        try:
            self.cur.execute("SELECT * FROM pupils")
            return self.cur.fetchall()
        except Error as error:
            self.error_message(f"db.pupils_get_all \n {error}")

    # =======================
    def pupils_get_one(self, pupil_id):
        try:
            if pupil_id:
                self.cur.execute(f"SELECT * FROM pupils WHERE id={pupil_id}")
                return self.cur.fetchone()
            else:
                return
        except Error as error:
            self.error_message(f"db.pupils_get_one \n {error}")

    # =======================
    def pupils_get_name(self, pupil_id):
        try:
            if pupil_id:
                self.cur.execute(
                    f"SELECT name, surname FROM pupils WHERE id={pupil_id}"
                )
                return self.cur.fetchone()
            else:
                return
        except Error as error:
            self.error_message("************************")
            self.error_message(f"db.pupils_get_name \n {error}")

    # =======================
    def pupils_delete(self, pupil_id):
        try:
            # self.cur = self.connection.cursor()
            self.cur.execute(f"DELETE FROM pupils WHERE id={pupil_id}")
            self.connection.commit()
            # return self.cur.fetchall()
        except Error as error:
            self.error_message("************************")
            self.error_message(f"db.pupils_delete \n {error}")

    # =======================
    def pupils_update(self, pupil_id, pupil_data):
        # self.cur = self.connection.cursor()
        try:
            (
                name,
                surname,
                school,
                class_id,
                phone,
                parent_phones,
                is_active,
            ) = pupil_data
            query = f"UPDATE pupils SET name=?, surname=?, school=?, class_id=?, phone=?, parent_phones=?, is_active=? WHERE id={                pupil_id}"
            self.cur.execute(query, pupil_data)
            self.connection.commit()
        except Error as error:
            self.error_message("************************")
            self.error_message(f"db.pupils_update \n {error}")

    # =======================
    def lesson_create(self, lesson_data):
        date, pupil_id, time, price, place = lesson_data
        try:
            self.cur.execute(
                f"INSERT INTO lessons (date, pupil_id, time, price, place) VALUES"
                f" ('{date}', '{pupil_id}', '{time}','{price}','{place}')"
            )
            self.connection.commit()

        except Error as error:
            self.error_message(f"db.lesson_create \n {error}")

    # =======================
    def lessons_get_all(self):
        try:
            self.cur.execute("SELECT * FROM lessons")
            return self.cur.fetchall()
        except Error as error:
            self.error_message(f"db.lessons_get_all \n {error}")

    # =======================
    def lessons_get_by_date_and_pupil(self, date, pupil_id):
        try:
            query = f"SELECT * FROM lessons WHERE date=:date and pupil_id=:pupil_id"
            params = {"date": date, "pupil_id":pupil_id}
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except Error as error:
            self.error_message(f"db.lessons_get_by_date_and_pupil \n {error}")

    # =======================
    def lessons_get_pupils_at_month(self, start_date, end_date):
        try:
            # query = f"SELECT pupils.id,  pupils.name, lessons.date, lessons.price FROM lessons JOIN pupils WHERE pupils.id = lessons.pupil_id AND lessons.date>=:start_date AND date<=:end_date"
            # query = f"SELECT DISTINCT pupils.id,  pupils.name  FROM lessons JOIN pupils WHERE pupils.id = lessons.pupil_id AND lessons.date>=:start_date AND date<=:end_date"
            query = f"SELECT DISTINCT pupils.id,  pupils.name  FROM lessons JOIN pupils WHERE pupils.id = lessons.pupil_id AND lessons.date BETWEEN :start_date AND :end_date"
            params = {"start_date": start_date, "end_date": end_date}
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except Error as error:
            self.error_message(f"db.lessons_get_at_month \n {error}")


    # =======================
    def lessons_get_by_id(self, lesson_id):
        try:
            query = (
                f"SELECT id, date,pupil_id, time, price, place FROM lessons WHERE id=:lesson_id"
            )
            params = {"lesson_id": lesson_id}
            self.cur.execute(query, params)
            return self.cur.fetchone()
        except Error as error:
            self.error_message(f"lessons_get_by_id \n {error}")

    # =======================
    def lessons_get_by_date(self, date):
        try:
            query = (
                f"SELECT lessons.id, lessons.date, pupils.id, lessons.time, lessons.price, lessons.place FROM lessons JOIN pupils WHERE "
                f"lessons.date=:date AND pupils.id=lessons.pupil_id"
                # f"lessons.date=:date"
            )
            params = {"date": date}
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except Error as error:
            self.error_message(f"db.lessons_get_by_date \n {error}")

    # =======================
    def lessons_get_by_date_and_pupil(self, date, pupil_id):
        try:
            query = (
                f"SELECT lessons.id, lessons.date, lessons.price FROM lessons WHERE "
                f"lessons.date=:date AND lessons.pupil_id=:pupil_id"
            )
            params = {"date": date, "pupil_id": pupil_id}
            self.cur.execute(query, params)
            return self.cur.fetchone()
        except Error as error:
            self.error_message("************************")
            self.error_message(f"db.lessons_get_by_date_and_pupil \n {error}")

    # =======================
    def lessons_get_sum_at_date(self, date):
        try:
            query = f"SELECT SUM(price) FROM lessons WHERE date=:date"
            params = {"date": date}
            self.cur.execute(query, params)
            return self.cur.fetchone()

        except Error as error:
            self.error_message(f"db.lessons_get_sum_at_date \n {error}")

    # =======================
    def lesson_update(self, lesson_id, lesson_data):
        try:
            query = f"UPDATE lessons SET date=?, pupil_id=?, time=?, price=?, place=? WHERE id={                lesson_id}"
            self.cur.execute(query, lesson_data)
            self.connection.commit()
        except Error as error:
            self.error_message("db.lesson_update ", error)

    # =======================
    def lesson_delete(self, lesson_id):
        try:
            query = f"DELETE FROM lessons WHERE id=:lesson_id"
            params = {"lesson_id": lesson_id}
            self.cur.execute(query, params)
            self.connection.commit()

        except Error as error:
            self.error_message("db.lesson_delete ", error)
