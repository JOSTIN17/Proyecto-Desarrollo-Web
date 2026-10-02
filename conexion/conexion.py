import os
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():

    conexion = psycopg2.connect(
        os.environ.get("DATABASE_URL")
    )

    return conexion
