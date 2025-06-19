from database.database import get_db

class StatsService:
    @staticmethod
    def get_repair_stats(start_date, end_date):
        db = get_db()

        sql = '''
            SELECT COUNT(*) AS repair_count
            FROM opravy o
            WHERE o.datum_zacatku_opravy BETWEEN ? AND ?
        '''

        return db.execute(sql, (start_date, end_date)).fetchone()

    @staticmethod
    def get_vehicle_leaderboard():
        db = get_db()

        sql = '''
                SELECT v.typ_vozidla, COUNT(*) AS repair_count
                FROM vozidla v
                JOIN objednavky ob ON ob.vozidlo_id_vozidla = v.id_vozidla
                JOIN opravy op ON ob.id_objednavky = op.objednavka_id_objednavky
                
                GROUP BY v.typ_vozidla
                ORDER BY repair_count DESC
            '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_employee_stats():
        db = get_db()

        sql = '''
                    SELECT u.id_uzivatele, u.jmeno, u.prijmeni, COUNT(*) AS repair_count
                    FROM uzivatele u
                    JOIN uzivatele_opravy uo ON uo.id_uzivatele = u.id_uzivatele

                    GROUP BY u.id_uzivatele
                    ORDER BY repair_count DESC
                '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_income_stats():
        db = get_db()

        sql = '''
                        SELECT t.nazev, SUM(oppo.pocet_pouzitych_kusu * p.prodejni_cena) AS total_price
                        FROM objednavky o
                        JOIN typy_oprav t ON t.id_opravy = o.typ_opravy_id_opravy
                        JOIN opravy op ON op.objednavka_id_objednavky = o.id_objednavky
                        JOIN opravy_polozky oppo ON oppo.id_opravy = op.id_opravy
                        JOIN polozky p ON p.id_polozky = oppo.id_polozky
                        
                        GROUP BY t.nazev
                        ORDER BY total_price DESC
                    '''

        return db.execute(sql).fetchall()

    @staticmethod
    def get_services_stats():
        db = get_db()

        sql = '''
                        SELECT t.nazev, COUNT(*) AS count
                        FROM objednavky o
                        JOIN typy_oprav t ON t.id_opravy = o.typ_opravy_id_opravy

                        GROUP BY t.id_opravy
                        ORDER BY count DESC
                    '''

        return db.execute(sql).fetchall()
