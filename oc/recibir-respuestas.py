from flask import Flask, request, jsonify
from flask_cors import CORS


# app = Flask(__name__)
# # Esto permite que CUALQUIER página envíe datos. 
# # En producción, puedes limitar esto a tu dominio de GitHub.
# CORS(app)


@app.route('/recibir-respuestas', methods=['POST'])
def recibir_respuestas():
    # Recibimos los datos del formulario
    datos = request.form


    pregunta1 = datos.get('pregunta1')
    pregunta2 = datos.get('pregunta2')
    
    # Aquí puedes guardar los datos en una base de datos o un archivo de texto
    print(f"Respuesta 1: {pregunta1}, Respuesta 2: {pregunta2}")
    
    # Redirigimos al usuario o le enviamos un mensaje de éxito
    return jsonify({"mensaje": "¡Tus respuestas fueron recibidas con éxito!"})
