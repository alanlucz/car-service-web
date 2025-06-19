import config
from database.database import get_db

class VehicleService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
            SELECT * FROM vozidla
        '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_by_client_id(client_id):
        db = get_db()

        sql = '''
               SELECT * FROM vozidla
               WHERE uzivatel_id_uzivatele = ?
           '''
        arguments = [client_id]
        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def add_vehicle(owner_id, brand, license_plate, type):
        db = get_db()

        license_plate = license_plate.replace(" ", "").upper()

        sql = '''
                INSERT INTO vozidla (spz, znacka_vozidla, typ_vozidla, uzivatel_id_uzivatele)
                VALUES (?, ?, ?, ?)
            '''
        arguments = [license_plate, brand, type, owner_id]
        db.execute(sql, arguments)
        db.commit()