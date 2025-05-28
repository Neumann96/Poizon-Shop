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


async def change_cours(new_cours):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()

    cursor.execute(f"Update cours set price = ?", (new_cours,))
    connect.commit()
    cursor.close()


async def add_order(info):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()
    try:
        # Предполагается, что info — это список из [user_id, username, sum]
        cursor.execute(
            'INSERT INTO orders(user_id, username, sum) VALUES (?, ?, ?);',
            (info[0], info[1], info[2])
        )
        order_id = cursor.lastrowid  # Получаем ID вставленной записи
        connect.commit()
        return order_id
    except Exception as e:
        print("Ошибка при добавлении заказа:", e)
        return None
    finally:
        cursor.close()
        connect.close()


async def get_order_by_id(order_id):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()
    try:
        cursor.execute('SELECT * FROM orders WHERE order_id = ?;', (order_id,))
        result = cursor.fetchone()  # Используем fetchone, если ожидаем одну строку
        return result if result else None
    except Exception as e:
        print("Ошибка при получении данных заказа:", e)
        return None
    finally:
        cursor.close()
        connect.close()


async def add_propt(info):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()
    try:
        # Предполагается, что info — это список из [user_id, username, sum]
        cursor.execute(
            'INSERT INTO propts(bank, number) VALUES (?, ?);',
            (info[0], info[1])
        )
        connect.commit()
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