import config
from database.database import get_db

class StockService:
    @staticmethod
    def get_all():
        db = get_db()

        sql = '''
            SELECT id_polozky, nazev, vyrobce, pocet_kusu, minimalni_pocet_kusu,
                CASE 
                    WHEN pocet_kusu <= minimalni_pocet_kusu THEN 'red'
                    WHEN pocet_kusu <= minimalni_pocet_kusu * 1.3 THEN 'yellow'
                    ELSE 'green'
                END AS status
            FROM polozky
        '''
        return db.execute(sql).fetchall()

    @staticmethod
    def get_by_id(item_id):
        db = get_db()

        sql = '''
                SELECT * FROM polozky p
                WHERE p.id_polozky = ?
            '''
        arguments=[item_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def add_item(name, maker, amount, purchase_price, selling_price, min_amount, description=None):
        db = get_db()

        sql = '''
            INSERT INTO polozky (nazev, vyrobce, pocet_kusu, nakupni_cena, prodejni_cena, minimalni_pocet_kusu, poznamka)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        description_value = description if description is not None else None

        arguments = [name, maker, amount, purchase_price, selling_price, min_amount, description_value]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def edit_item(item_id, name, maker, amount, purchase_price, selling_price, min_amount, description=None):
        db = get_db()

        sql = '''
                UPDATE polozky SET nazev = ?, vyrobce = ?, pocet_kusu = ?, nakupni_cena = ?, prodejni_cena = ?, minimalni_pocet_kusu = ?, poznamka = ?
                WHERE id_polozky = ?
            '''

        description_value = description if description is not None else None

        arguments = [name, maker, amount, purchase_price, selling_price, min_amount, description_value, item_id]
        db.execute(sql, arguments)
        db.commit()