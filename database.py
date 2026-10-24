import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def conectar_db():
    try:
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
if __name__ == "__main__":
    conexion = conectar_db()
    if conexion:
        conexion.close()
        print("Conexion cerrada de forma segura.")
