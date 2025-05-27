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


async def add_order(user_id):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()
    try:
        cursor.execute('INSERT INTO orders(user_id) VALUES(?);', (user_id,))
        order_id = cursor.lastrowid  # Получаем ID вставленной записи
        connect.commit()
        return order_id
    except Exception as e:
        print("Ошибка при добавлении заказа:", e)
        return None
    finally:
        cursor.close()
        connect.close()


# def get_cours(user_id):
#     connect = sqlite3.connect('Poizon.db')
#     cursor = connect.cursor()
#
#     res = cursor.execute(f"SELECT order_id FROM orders WHERE user_id={}").fetchone()
#     return res