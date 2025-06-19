import hashlib

from database.database import get_db
import config

class UserService():
    @staticmethod
    def verify(login, password):
        db = get_db()

        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        print(hashed_password.hexdigest())

        sql = '''
            SELECT u.id_uzivatele, u.email, r.nazev AS nazev_role, r.id_role
            FROM uzivatele u
            JOIN role r ON u.role_id_role = r.id_role
            WHERE u.email = ? AND u.heslo = ?
        '''
        arguments = [login, hashed_password.hexdigest()]

        user = db.execute(sql, arguments).fetchone()
        return user if user else None  # Zajisteni spravneho datoveho typu, vratim jen user, nic jineho


    @staticmethod
    def register(first_name, last_name, login, password, confirm_password):
        if password != confirm_password:
            return "Hesla se musi shodovat."

        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode()).hexdigest()

        client_role_id = 4

        db = get_db()

        sql_check = 'SELECT COUNT(*) FROM uzivatele WHERE email = ?'
        existing_user = db.execute(sql_check, [login]).fetchone()
        if existing_user[0] > 0:
            return "Tento email jiz existuje."

        sql = '''
            INSERT INTO uzivatele (jmeno, prijmeni, email, heslo, role_id_role)
            VALUES (?, ?, ?, ?, ?)
        '''
        arguments = [first_name, last_name, login, hashed_password, client_role_id]

        db.execute(sql, arguments)
        db.commit()

        return None
