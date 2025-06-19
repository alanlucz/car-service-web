import hashlib

import config
from database.database import get_db

class ClientService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
            SELECT u.id_uzivatele, u.jmeno, u.prijmeni, r.nazev AS nazev_role
            FROM uzivatele u
            JOIN role r ON u.role_id_role = r.id_role
            WHERE u.role_id_role = 4
        '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_by_id(client_id):
        db = get_db()

        sql = '''
               SELECT * FROM uzivatele
               WHERE id_uzivatele = ?
           '''
        arguments = [client_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def add_client(first_name, last_name, email, password):
        db = get_db()

        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())

        sql = '''
            INSERT INTO uzivatele (jmeno, prijmeni, email, role_id_role, heslo)
            VALUES (?, ?, ?, ?, ?)
        '''
        arguments = [first_name, last_name, email, 4, hashed_password.hexdigest()]
        db.execute(sql, arguments)
        db.commit()


    @staticmethod
    def edit_client(client_id, first_name, last_name, email):
        db = get_db()

        sql = '''
            UPDATE uzivatele SET jmeno = ?, prijmeni = ?, email = ?
            WHERE id_uzivatele = ?
        '''
        arguments = [first_name, last_name, email, client_id]
        db.execute(sql, arguments)
        db.commit()
