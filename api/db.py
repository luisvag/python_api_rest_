import pymysql
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


def mysql():
    return pymysql.connect(host="localhost", user="root", password="", db="test")
