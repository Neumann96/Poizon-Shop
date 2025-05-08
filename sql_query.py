import sqlite3


def get_price_comission(name):
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()

        res = cursor.execute("SELECT price FROM comissions WHERE name = ?", [name]).fetchone()
        return res


def get_cours():
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()

        res = cursor.execute("SELECT price FROM cours").fetchone()
        return res


def change_cours(new_cours):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()

    new_cours = float(new_cours)
    cursor.execute(f"Update cours set price = ?", (new_cours,))
    connect.commit()
    cursor.close()