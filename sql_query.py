import sqlite3


def get_price_comission(name):
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()

        res = cursor.execute("SELECT price, then_price, fast_price FROM comissions WHERE name = ?", [name]).fetchall()
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
            'INSERT INTO orders(user_id, username, sum, sum_y, comission, then_price) VALUES (?, ?, ?, ?, ?, ?);',
            (info[0], info[1], info[2], info[3], info[4], info[5])
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
            'INSERT INTO propts(bank, number, recipient) VALUES (?, ?, ?);',
            (info[0], info[1], info[2])
        )
        connect.commit()
    except Exception as e:
        print("Ошибка при добавлении заказа:", e)
        return None
    finally:
        cursor.close()
        connect.close()


async def update_current_propts_id(new_id):
    connect = sqlite3.connect('Poizon.db')
    cursor = connect.cursor()

    cursor.execute(f"Update propts_now set id_prop = ?", (new_id,))
    connect.commit()
    cursor.close()


async def get_current_propts_id():
    try:
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()
        cursor.execute("SELECT id_prop FROM propts_now LIMIT 1;")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Ошибка при получении текущего ID реквизитов:", e)
        return None
    finally:
        cursor.close()
        connect.close()


async def get_payment_data_by_id(acc_id: int):
    try:
        connect = sqlite3.connect('Poizon.db')
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM propts WHERE id = ?", (acc_id,))
        result = cursor.fetchone()
        return result  # Возвращает кортеж с полями строки или None
    except Exception as e:
        print("Ошибка при получении данных по ID:", e)
        return None
    finally:
        cursor.close()
        connect.close()