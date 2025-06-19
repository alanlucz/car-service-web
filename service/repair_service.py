from database.database import get_db

class RepairService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
            SELECT * FROM opravy op
            JOIN uzivatele_opravy uo ON op.id_opravy = uo.id_opravy
            JOIN uzivatele u ON uo.id_uzivatele = u.id_uzivatele
            ORDER BY op.id_opravy DESC
        '''
        return db.execute(sql).fetchall()


    @staticmethod
    def get_all_services():
        db = get_db()

        sql = '''
            SELECT * FROM typy_oprav tp
        '''
        return db.execute(sql).fetchall()


    @staticmethod
    def add_repair(description, time, start_date, end_date, order, employee_id, selected_items):
        db = get_db()

        sql = '''
                INSERT INTO opravy (popis_provedenych_praci, cas_straveny_na_oprave, datum_zacatku_opravy, datum_konce_opravy, objednavka_id_objednavky)
                VALUES (?, ?, ?, ?, ?)
            '''
        arguments = [description, time, start_date, end_date, order]
        db.execute(sql, arguments)

        repair_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        sql = '''
                INSERT INTO uzivatele_opravy (id_opravy, id_uzivatele) VALUES (?, ?)
            '''
        arguments = [repair_id, employee_id]
        db.execute(sql, arguments)


        for item_id, amount in selected_items.items():
            update_stock_query = 'UPDATE polozky SET pocet_kusu = pocet_kusu - ? WHERE id_polozky = ?'
            db.execute(update_stock_query, [amount, item_id])

            sql = '''
                    INSERT INTO opravy_polozky (id_opravy, id_polozky, pocet_pouzitych_kusu)
                    VALUES (?, ?, ?)
                '''
            arguments = [repair_id, item_id, amount]
            db.execute(sql, arguments)

        db.commit()