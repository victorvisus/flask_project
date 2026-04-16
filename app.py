import os  # importar el módulo del sistema operativo

import certifi
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Base de datos MongoDB
ca = certifi.where()
MONGO_URI = os.environ.get("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi("1"), tlsCAFile=ca)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

# CREAR BASE DE DATOS: db = client["thirty_days_of_python"]
db = client.thirty_days_of_python  # la primera vez se crea la base de datos

# CREAR COLECCIONES/TABLAS: students e insertar un documento
"""
db.students.insert_one({"name": "Asabeneh", "country": "Finland", "city": "Helsinki", "age": 250})
print("Despues de crear tablas: ", client.list_database_names())
"""
# AÑADIR REGISTROS
""" students = [
    {"name": "David", "country": "UK", "city": "London", "age": 34},
    {"name": "John", "country": "Sweden", "city": "Stockholm", "age": 28},
    {"name": "Sami", "country": "Finland", "city": "Helsinki", "age": 25},
]
for student in students:
    db.students.insert_one(student)
 """

# AÑADIR COLECCION teachers
"""
teachers = [
    {"name": "Mr. Johnson", "country": "USA", "city": "New York", "age": 45},
    {"name": "Ms. Rodriguez", "country": "Mexico", "city": "Mexico City", "age": 38},
    {"name": "Mr. Lee", "country": "South Korea", "city": "Seoul", "age": 42},
    {"name": "Ms. Brown", "country": "UK", "city": "London", "age": 40},
    {"name": "Mr. Patel", "country": "India", "city": "Mumbai", "age": 35},
]
try:
    for teacher in teachers:
        db.teachers.insert_one(teacher)

    print("teachers creado e insertados varios registros")
    print("Despues de crear tablas: ", client.list_database_names())
except Exception as e:
    print(e)
"""

# CONSULTAS de datos:
"""
student = db.students.find_one(
    {"_id": ObjectId("69de2961a08894a7eb124015")}
)  # consulta por ID
print(student)

students = db.students.find()  # todos los registros
print("registros con find(), con todos los campos -------------------")
for student in students:
    print(student)

students = db.students.find(
    {}, {"_id": 0, "name": 1, "country": 1}
)  # 0 excluir, 1 incluir
print("registros con find(), con campos seleccionados -------------------")
for student in students:
    print(student)
"""
# ACTUALIZAR REGISTROS
"""
db.students.update_one(
    {"name": "Asabeneh"}, {"$set": {"country": "Finland"}}
)  # actualizar un registro, segun el FILTER/WHERE
"""
# ELIMINAR REGISTROS
"""
db.students.delete_one({"name": "David"})  # eliminar un registro
db.students.delete_many({"name": "Asabeneh"})  # eliminar varios
"""
#
# CONSULTAS de datos, WHERE "name": "Asabeneh"
"""
consulta = {"name": "Asabeneh"}
students = db.students.find(
    consulta, {"_id": 0, "name": 1, "country": 1}
)  # 0 excluir, 1 incluir
print(
    "registros con find(), name: Asabeneh con campos seleccionados -------------------"
)
for student in students:
    print(student)
"""
cadena = {"age": {"$gt": 30, "$lt": 42}}
teachers = db.teachers.find(cadena, {"_id": 0, "name": 1, "country": 1, "age": 1}).sort(
    "age", -1
)  # 0 excluir, 1 incluir, -1 descendente, 1 ascendente
for teacher in teachers:
    print(teacher)
#
#
#
##############################################################################################3

app = Flask(__name__)


@app.route("/")  # este decorador crea la ruta de inicio
def home():
    techs = ["HTML", "CSS", "Flask", "Python"]
    name = "30 días de desafío de programación en Python"
    return render_template(
        "home.html", techs=techs, name=name, title="Página principal"
    )


@app.route("/about")
def about():
    name = "30 días de desafío de programación en Python"
    return render_template("about.html", name=name, title="Acerca de nosotros")


@app.route("/post")
def post():
    name = "Artículos"
    return render_template("post.html", name=name, title="Artículos")


@app.route("/result", methods=["POST"])
def result():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    old_job = request.form["old_job"]
    current_job = request.form["current_job"]
    country = request.form["country"]
    print(first_name, last_name, old_job, current_job, country)
    result_data = {
        "first_name": first_name,
        "last_name": last_name,
        "old_job": old_job,
        "current_job": current_job,
        "country": country,
    }
    return render_template("result.html", result_data=result_data, title="Resultado")


if __name__ == "__main__":
    # usamos variables de entorno para despliegue
    # funciona tanto para producción como para desarrollo
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
    # con use_reloader=False para aplicar los cambios hay que reiniciar a mano el servidor
