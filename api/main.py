from faker import Faker
from faker.providers import phone_number, internet
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import mysql

fake = Faker()
fake.add_provider(phone_number)
fake.add_provider(internet)

"""
GET = OBTENER INFO
POST = CREAR INFO
PUT = ACTUALIZAR INFO
DELETE = DELETE

"""

#empizo mi server
app = Flask(__name__)
CORS(app)

db = []

@app.route('/get-users')
def get_users():
    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `usuarios`")
        users = cursor.fetchall()
    connection.close()

    dictList = []

    for userTuple in users:
        user = {}
        user["id"] = userTuple[0]
        user["username"] = userTuple[1]
        user["password"] = userTuple[2]
        user["email"] = userTuple[3]

        dictList.append(user)

    return jsonify(dictList), 200

#creo funcion para obtener la data de un usuario(2007)
@app.route("/get-user/<id>")
def get_user(id):
    connection = mysql()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `usuarios` WHERE id = {id}")
        userTuple = cursor.fetchone()
    connection.close()

    user = {}
    user["id"] = userTuple[0]
    user["username"] = userTuple[1]
    user["email"] = userTuple[2]

    return jsonify(user), 200

@app.route('/create-user', methods=['POST'])

def create_user():
    data = request.get_json()

    if data in db:
        return f"el usuario {data['name']} o el correo{data["correo"]} ya existe", 400

    if data not in db:
        db.append(data)
        return f'Bienvenido {data["name"]}', 201
    
@app.route('/reset-pass/<username>', methods=["PATCH"])
def reset_pass(username):
    for user in db:
        if username == user["name"]:
            new_pass = request.get_json()
            user["password"] = new_pass["password"]
            return str(user["password"]), 200
        
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
