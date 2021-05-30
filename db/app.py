from flask import Flask, request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']='usuario_veterinaria'

mysql = MySQL(app)

@app.route('/')
def index():
    return "Soy index"

@app.route('/consultarDatos')
def consultarDatos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    datos = cursor.fetchall()
    resultado = json.dumps(datos)
    return resultado

@app.route('/consultaDato/<string:dato>', methods=['POST'])
def consultaDato(dato):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT {dato} FROM usuario")
    data = cursor.fetchall()

    if data:
        return str(data)


@app.route('/verificacion', methods=['POST'])
def verficacion():
    json_datos = request.get_json()

    email = json_datos['email']
    contraseña = json_datos['contraseña']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email, contraseña FROM usuario WHERE email=%s AND contraseña=%s",(email,contraseña))
    datos = cursor.fetchone()
    resultadoDatos = json.dumps(datos)

    if email == datos[0] and contraseña == datos[1]:
        return "Bienvenido al servicio"
    
    else:
        return "Lo sentimos, el email y la contraseña son incorrectos, vuelva a intentarlo, por favor."

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id = %s",(id))
    datos = cursor.fetchall()

    if datos:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s",(id))
        cursor.connection.commit()

        return "Datos eliminados con éxito"

    else:
        return "Digite un ID existente"


@app.route('/registrar', methods=['POST'])
def registrar():
    json_datos = request.get_json()
    nuevoNombre = json_datos['nuevoNombre']
    nuevoApellido = json_datos['nuevoApellido']
    nuevoEmail = json_datos['nuevoEmail']
    nuevaContraseña = json_datos['nuevaContraseña']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuario (nombre, apellido, email, contraseña) VALUES(%s, %s, %s, %s)", (nuevoNombre, nuevoApellido, nuevoEmail, nuevaContraseña))
    cursor.connection.commit()

    return "Usuario registrado con éxito "



if __name__ == '__main__':
    app.run(debug=True)