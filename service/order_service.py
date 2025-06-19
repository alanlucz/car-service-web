from datetime import datetime

from flask import flash, redirect, url_for

import config
from database.database import get_db

class OrderService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
            SELECT * FROM objednavky o
            JOIN vozidla v on o.vozidlo_id_vozidla = v.id_vozidla
            JOIN uzivatele u on v.uzivatel_id_uzivatele = u.id_uzivatele
            GROUP BY o.id_objednavky, o.datum_vzniku
            ORDER BY o.datum_vzniku DESC
        '''
        return db.execute(sql).fetchall()

    @staticmethod
    def get_all_unfinished():
        db = get_db()

        sql = '''
                SELECT * FROM objednavky o
                JOIN vozidla v on o.vozidlo_id_vozidla = v.id_vozidla
                JOIN uzivatele u on v.uzivatel_id_uzivatele = u.id_uzivatele
                WHERE o.stav != 'dokončeno'
                GROUP BY o.id_objednavky, o.datum_vzniku
                ORDER BY o.datum_vzniku DESC
            '''
        return db.execute(sql).fetchall()

    @staticmethod
    def get_by_id(order_id):
        db = get_db()

        sql = '''
                SELECT * FROM objednavky o
                JOIN vozidla v on o.vozidlo_id_vozidla = v.id_vozidla
                JOIN uzivatele u on v.uzivatel_id_uzivatele = u.id_uzivatele
                WHERE o.id_objednavky = ?
            '''
        arguments=[order_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def get_by_client_id(client_id):
        db = get_db()

        sql = '''
                SELECT t.nazev AS repair_type, o.datum_vzniku AS start_date FROM objednavky o
                JOIN typy_oprav t ON t.id_opravy = o.typ_opravy_id_opravy
                JOIN vozidla v on o.vozidlo_id_vozidla = v.id_vozidla
                JOIN uzivatele u on v.uzivatel_id_uzivatele = u.id_uzivatele
                WHERE u.id_uzivatele = ?
            '''
        arguments=[client_id]
        return db.execute(sql, arguments)

    @staticmethod
    def create_order(description, preferred_date, service_type, vehicle_id):
        db = get_db()

        today = datetime.now().date()


        create_date = today.strftime('%Y-%m-%d')
        status = 'čekající'

        sql = '''
                            INSERT INTO objednavky (popis, preferovany_termin, datum_vzniku, typ_opravy_id_opravy, vozidlo_id_vozidla, stav)
                            VALUES (?, ?, ?, ?, ?, ?)
                        '''
        arguments = [description, preferred_date, create_date, service_type, vehicle_id, status]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def edit_order(order_id, status, note):
        db = get_db()

        sql = '''
                UPDATE objednavky SET stav = ?, poznamka = ?
                WHERE id_objednavky = ?
            '''

        arguments = [status, note, order_id]
        db.execute(sql, arguments)
        db.commit()