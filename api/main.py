from faker import Faker
from faker.providers import phone_number, internet
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from db import *
from werkzeug.security import check_password_hash

fake = Faker()
fake.add_provider(phone_number)
fake.add_provider(internet)

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
    data = request.get_json()
    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `usuarios` WHERE id = {data['id']}")
        existing_user = cursor.fetchone()
        if existing_user:
            connection.close()
            return "User already exist", 400

        cursor.execute(
            f"INSERT INTO `usuarios` (`id`, `username`, `password`, `email`) VALUES ('{data['id']}', '{data['username']}', '{data['password']}', '{data['email']}')"
        )

    connection.commit()
    connection.close()

    return f'Welcome {data["username"]}', 201


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    _username = body["username"]
    _password = body["password"]

    if _username and _password:
        connection = mysql()
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, password FROM `usuarios`")
            todas_las_cuentas = cursor.fetchall()
        connection.close()

        correct_usuario = None

        for user in todas_las_cuentas:
            if _username in user:
                correct_usuario = user

        if not correct_usuario:
            return jsonify({"message": "Invalid credentials"}), 400

        if _password == correct_usuario[1]:
            return jsonify({"message": "logged in"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 400


@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    return None, 200


@app.route("/reset-pass/<username>", methods=["PATCH"])
def reset_pass(username):
    for user in db:
        if username == user["name"]:
            new_pass = request.get_json()
            user["password"] = new_pass["password"]
            return str(user["password"]), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
