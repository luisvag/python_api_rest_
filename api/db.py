import pymysql


def mysql():
    return pymysql.connect(host="localhost", user="root", password="", db="test")
