import os
from pymongo.mongo_client import MongoClient

MONGO_URL = os.getenv("MONGO_URL")


def connection():
    try:
        client = MongoClient(MONGO_URL)
        if client is not None:
            print("Conexão estabelecida com sucesso")
        db = client["api-node"]
        collection = db["Alimentos"]
        return collection
    except Exception as e:
        print("Ocorreu um erro ao conectar ao banco : ", str(e))
