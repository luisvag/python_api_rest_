from faker import Faker
from faker.providers import phone_number, internet, misc
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from db import *

fake = Faker()
fake.add_provider(phone_number)
fake.add_provider(internet)
fake.add_provider(misc)

"""
GET = OBTENER INFOs
POST = CREAR INFO
PUT = ACTUALIZAR INFO
DELETE = DELETE

"""

app = Flask(__name__)
CORS(app)

db = []


@app.route("/get-users")
def get_users():
    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `usuarios`")
        users = cursor.fetchall()
    connection.close()

    user_list = []

    for user_tuple in users:
        user = {}
        user["id"] = user_tuple[0]
        user["username"] = user_tuple[1]
        user["password"] = user_tuple[2]
        user["email"] = user_tuple[3]

        user_list.append(user)

    return jsonify(user_list), 200


@app.route("/get-user/<id>")
def get_user(id):
    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `usuarios` WHERE id = {id}")
        user_tuple = cursor.fetchone()
    connection.close()

    user = {}
    user["id"] = user_tuple[0]
    user["username"] = user_tuple[1]
    user["email"] = user_tuple[2]

    return jsonify(user), 200


@app.route("/create-user", methods=["POST"])
def create_user():
    body = request.get_json()

    _username = body["username"]
    _password = body["password"]
    _email = body["email"]
    _token = fake.uuid4()

    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `usuarios` WHERE username = '{_username}'")
        existing_user = cursor.fetchone()
        if existing_user:
            connection.close()
            return jsonify({"message": "User already exist"}), 400

        cursor.execute(
            f"INSERT INTO `usuarios` (`id`, `username`, `password`, `email`, `token`) VALUES (NULL, '{_username}', '{_password}', '{_email}', '{_token}')"
        )

    connection.commit()
    connection.close()

    return jsonify({"message": "user created"}), 201


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    _username = body["username"]
    _password = body["password"]

    if _username and _password:
        connection = mysql()
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, password, token FROM `usuarios`")
            todas_las_cuentas = cursor.fetchall()
            cursor.lastrowid
        connection.close()

        correct_usuario = None

        for user in todas_las_cuentas:
            if _username in user:
                correct_usuario = user

        if not correct_usuario:
            return jsonify({"message": "Invalid credentials"}), 400

        if _password == correct_usuario[1]:
            return jsonify({"message": "logged in", "token": correct_usuario[2]}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 400


@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    return None, 200


@app.route("/reset-pass/<username>", methods=["PATCH"])
def reset_pass(username):
    json = request.get_json()
    new_password = json["new_password"]

    if json:
        connection = mysql()
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT id, username, password FROM `usuarios` WHERE username = '{username}'"
            )
            existing = cursor.fetchone()

        if existing:
            existing[2] == new_password
            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE `usuarios` SET `password` = '{new_password}' WHERE `usuarios`.`id` = '{existing[0]}' "
                )
                connection.commit()
                connection.close()
                return ({"message": "password changed"}), 200

        else:
            return ({"message": "this user does not exist"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
