import datetime
import re
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"plu (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"link TEXT,"
                                f"name TEXT,"
                                f"area TEXT,"
                                f"devel TEXT,"
                                f"date TEXT,"
                                f"text TEXT,"
                                f"link_wp TEXT,"
                                f"other TEXT)")
        except Exception as es:
            print(f'SQL исключение check_table имя таблицы{es}')

    def exist_plu(self, link):
        try:
            result = self.cursor.execute(f"SELECT * FROM plu WHERE link = '{link}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! При exist_plu в DB "{es}"')
            return []

        return response

    def add_plu(self, link, name, area, devel, date, text):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO plu ('link', 'name', "
                                "'area', 'devel', 'date', 'text') VALUES (?,?,?,?,?,?)", (link, name, area,
                                                                                          devel, date, text[:100]))
            self.conn.commit()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить plu в DB "{es}"')

            return False

        return True

    def insert_publish_links(self, link, link_wp):
        try:
            self.cursor.execute(f"UPDATE plu SET link_wp='{link_wp}' WHERE link='{link}'")
            self.conn.commit()
        except Exception as es:
            print(f'SQL ошибка! Не смог insert_publish_links в DB "{es}"')

            return False

        return True

    def update_sql(self, id_pk, link, name, area, devel, date, text):
        try:
            self.cursor.execute(f"UPDATE plu SET link='{link}', name='{name[:100]}', area='{area}', devel='{devel}',"
                                f" date='{date}', text='{text[:100]}' WHERE id_pk='{id_pk}'")
            self.conn.commit()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить update_sql в DB "{es}"')

            return False

        return True

    def update_check(self, link, name, area, devel, date, text):
        try:
            result = self.cursor.execute(f"SELECT id_pk, name, area, devel, date, text FROM plu WHERE link = '{link}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить plu в DB "{es}"')

            return False

        try:
            id_pk, name_sql, area_sql, devel_sql, date_sql, text_sql = response[0]
        except Exception as es:
            print(f'Ошибка при обновление изменений "{es}"')

            return False

        if name[:100] != name_sql or area != area_sql or devel != devel_sql or date != date_sql or text[:100] != text_sql:
            print(f'Надо обновить')
            self.update_sql(id_pk, link, name, area, devel, date, text)

            return True

        return False

    def update_double(self, artikl, collection, proiz):
        try:
            result = self.cursor.execute(f"SELECT id_pk, collection FROM plu WHERE artikl = '{artikl}' AND "
                                         f"proiz = '{proiz}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! При update_double 1 в DB "{es}"')
            return []

        if response != []:
            id_pk = response[0][0]
            coll_sql = response[0][1]

            if collection in coll_sql:
                print(f'Уже есть коллекция {collection} в sql пропускаю')
                return True

            update_coll = coll_sql + ';' + collection

            try:

                result = self.cursor.execute(
                    f"UPDATE plu SET collection = '{update_coll}' WHERE id_pk = '{id_pk}'")
                self.conn.commit()
                # x = result.fetchall()
            except Exception as es:
                print(f'Ошибка SQL update_double 2: {es}')

        return True

    def get_all_count(self):
        try:
            result = self.cursor.execute("SELECT count(*) FROM plu")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить get_all_count в DB "{es}"')

            return 0

        try:
            res = int(response[0][0])
        except:
            res = 0

        return res

    def get_tovar(self, id_pk):
        try:
            result = self.cursor.execute(f"SELECT * FROM plu WHERE id_pk = '{id_pk}'")
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить get_tovar в DB "{es}"')

            return False

        try:
            res = response[0]
        except:
            return []

        return res

    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')
