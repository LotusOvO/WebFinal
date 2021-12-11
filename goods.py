from database import *
from forms import *


def addgood(name, number, price):
    cursor.execute("SELECT id from goods order by id")
    ids = [item for t in cursor.fetchall() for item in t]
    ids.append(1)
    goodid = 1
    for i in range(1, max(ids)+2):
        if i not in ids:
            goodid = i
            break
    cursor.execute(f"insert into goods values ({goodid}, '{name}', {price}, {number})")

    conn.commit()


def showgood():
    cursor.execute(f'SELECT * from goods')
    res = []
    for good in cursor.fetchall():
        tempform = GoodForm()
        tempform.ID.data = good['id']
        tempform.name.data = good['name']
        tempform.price.data = good['price']
        tempform.number.data = good['inventory']
        tempform.image.data = good['image']
        res.append(tempform)
    return res


def findbyid(ID):
    cursor.execute(f"select * from goods where id = {ID}")
    return cursor.fetchall()[0]


def salegood(id, num):
    cursor.execute(f"update goods set inventory = (inventory - {num}) where id = {id}")
    conn.commit()


def changegood(id, name, price, num):
    print(id, name, price, num)
    cursor.execute(f"update goods set name = '{name}', price = {price}, inventory = {num} where id = {id}")
    conn.commit()


def delgood(id):
    cursor.execute(f"delete from goods where id = {id}")
    conn.commit()

