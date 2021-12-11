import hashlib
from database import *
from flask_login import UserMixin

salt = b"LotusOvO"


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.shoppingtrolley = []

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        if finduser(username):
            return User(username)
        else:
            return None


def hashedPwd(password):
    hasher = hashlib.sha256(salt)
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()


def newuser(username, password):
    cursor.execute(f"insert into users values('{username}', '{hashedPwd(password)}')")
    conn.commit()


def finduser(username):
    # cursor.execute(f"SELECT * FROM users")
    # print(cursor.fetchall())
    cursor.execute(f"SELECT COUNT(1) FROM users WHERE name = '{username}'")
    return cursor.fetchall()[0][0]
    # return True


def userlogin(username, password):
    password = hashedPwd(password)
    cursor.execute(f"SELECT COUNT(1) FROM users WHERE name = '{username}' and password = '{password}'")
    return cursor.fetchall()[0][0]


def addorder(username, goodname, price, number):
    cursor.execute("SELECT id from orders order by id")
    ids = [item for t in cursor.fetchall() for item in t]
    ids.append(1)
    orderid = 1
    for i in range(1, max(ids) + 2):
        if i not in ids:
            orderid = i
            break
    cursor.execute(
        f"insert into orders values('{username}', '{goodname}', {number}, (select current_timestamp), {price}, {orderid})")
    conn.commit()
    return


def getorderbyuser(username):
    cursor.execute(f"SELECT * from orders where username = '{username}'")
    return cursor.fetchall()


def gerallorder():
    cursor.execute(f"SELECT * from orders")
    return cursor.fetchall()
