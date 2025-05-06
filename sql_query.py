import sqlite3


def get_price_comission(name):
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()

        res = cursor.execute("SELECT price FROM comissions WHERE name = ?", [name]).fetchone()
        return res