from sqlite3 import sqlite_version

from database.database import get_db

class RoleService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
                SELECT id_role, nazev, popis
                FROM role
            '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_employee_roles():
        db = get_db()

        sql = '''
                SELECT id_role, nazev, popis
                FROM role
                WHERE id_role != 4 AND id_role != 1
            '''

        return db.execute(sql).fetchall()