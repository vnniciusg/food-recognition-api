import re
from flask import Flask, request, jsonify
from controller.format_read_image import analisyImage
from database.db import connection
from dotenv import load_dotenv

load_dotenv()

collection = connection()

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error: ", "Nenhuma imagem encontrado"})
    file = request.files["file"]
    try:
        result = analisyImage(file)

        regex = re.compile(result, re.IGNORECASE)

        consulta = collection.find_one({"Nome": {"$regex": regex}})
        resultado = {"Nome": consulta["Nome"], "Calorias": consulta["Calorias"]}

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error: ", str(e)})


if __name__ == "__main__":
    app.run(port=5003, debug=True)
