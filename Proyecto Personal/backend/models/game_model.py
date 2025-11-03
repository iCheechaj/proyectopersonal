from database import get_db
import mysql.connector

# obtener un juego por id
def get_Game_By_Id(id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM juegos WHERE id = %s", (id,))
        row = cursor.fetchone()
        return row
    except mysql.connector.Error as err:
        print("Error al obtener el juego ", err)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Obtener juegos con filtros personalizados
def get_games_by_filter(genre=None, year_from_=None, year_to=None,
                         min_rating=None, order_by=None, desc=None):
    conn = None
    cursor = None
    try:
        conn = get_db()
        query = "SELECT * FROM juegos"
        cursor = conn.cursor(dictionary=True)
        parts = [] #Filtros
        params = [] #Parametros

        if genre:
            parts.append("genero = %s")
            params.append(genre)
        if year_from_:
            parts.append("anio >= %s")
            params.append(year_from_)
        if year_to:
            parts.append("anio <= %s")
            params.append(year_to)
        if min_rating:
            parts.append("rating >= %s")
            params.append(min_rating)
        
        # Si vienen filtros del WHERE
        if parts:
            query += " WHERE " + " AND ".join(parts)
        if order_by in ["titulo", "anio", "rating", "genero", "desarrolladora"]:
            if bool(desc) == True:
                query += f" ORDER BY {order_by} DESC"
            else:
                query += f" ORDER BY {order_by}" 

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print("Error con los filtros ", err)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

#Crear juegos

def create_game(titulo, genero, anio, desarrolladora, rating, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO juegos (titulo, genero, anio, desarrolladora, rating, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (titulo, genero, anio, desarrolladora, rating, imagen)
        )
        conn.commit()
        last_id = cursor.lastrowid # devuelve el ultimo id
        return last_id
    except mysql.connector.Error as err:
        print("Error al crear el juego ", err)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_game(id, titulo, genero, anio, desarrolladora, rating, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE juegos
            SET titulo = %s, genero = %s, anio = %s, desarrolladora = %s, rating = %s, imagen = %s
            WHERE id = %s
            """,
            (titulo, genero, anio, desarrolladora, rating, imagen, id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al actualizar el juego ", err)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
            
def delete_game(id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al eliminar el juego ", err)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()