import os # Hacer funcionar cosas en el sistema operativo
import mysql.connector # Conectar a la base de datos MySQL
from mysql.connector import Error # Manejar errores de MySQL
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  # Cargar variables de entorno desde el archivo .env
def get_db():
    try:
        #Configuracion:
        cfg = {
            "host": os.environ["DB_HOST"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "database": os.environ["DB_NAME"],
            "port": int(os.environ["DB_PORT"])
        }

        #Conexion a la base de datos
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            print("Conexion establecida")
            return conn
    except Error as e:
        print("Error al conectarse ", e)
        return None