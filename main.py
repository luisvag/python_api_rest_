from flask import Flask, jsonify, request

"""
GET = OBTENER INFO
POST = CREAR INFO
PUT = ACTUALIZAR INFO
DELETE = DELETE

"""

#empizo mi server
app = Flask(__name__)

#creo funcion para obtener la data de un usuario(2007)
@app.route("/get-usuario/<usuario_id>")
def get_user(usuario_id):
#/get-usuario/2007  
    usuario_data = {
        'usuario_id': usuario_id,
        'name' : 'Antonio Banderas',
        'correo': 'antonioban@outlook.com'
        }

    #query parameter,valor extra
    extra = request.args.get('extra')
    if extra:
        usuario_data['extra'] = extra

    return jsonify(usuario_data), 200

if __name__=="__main__":
    app.run(debug=True)