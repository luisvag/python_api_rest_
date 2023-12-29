from faker import Faker
from faker.providers import phone_number, internet
from flask import Flask, jsonify, request
from flask_cors import CORS

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

# db = ['luisito', 
# 'ledgermayne']

# db = []

#creo funcion para obtener la data de un usuario(2007)
@app.route("/get-user/<username>")
def get_user(username):

    for user in db:
        if username == user["name"]:
            return jsonify(user), 200

    #query parameter,valor extra
    # extra = request.args.get('extra')
    # if extra:
    #     usuario_data['extra'] = extra

    # return jsonify(usuario_data), 200


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

@app.route('/get-users')
def get_users():
    return db, 200
        
if __name__=="__main__":
    app.run(debug=True)
