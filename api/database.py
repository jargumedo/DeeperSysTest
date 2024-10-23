from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.3tvwf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client['deepersysdb']  
        return db
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None  
