from models.game_model import delete_game, get_Game_By_Id, get_games_by_filter, create_game, update_game
from flask import Blueprint, request , jsonify
from database import get_db
import mysql.connector

games_bp = Blueprint("games", __name__)
    
def validar_entero(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None
    
def validar_float(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None

@games_bp.route("/<int:id>", methods=["GET"])
def get_game(id):
    game = get_Game_By_Id(id)
    if not game:
        return jsonify({
            "message": "No encontrado"
        }), 404
    return jsonify(game)

@games_bp.route("/", methods=["GET"])
def get_movies_filter():
    genero = request.args.get("genero")
    year_from_ = validar_entero(request.args.get("year_from"))
    year_to = validar_entero(request.args.get("year_to"))
    min_rating = validar_float(request.args.get("min_rating"))
    order_by = request.args.get("order_by")
    desc = request.args.get("desc") 

    movies = get_games_by_filter(genre=genero, year_from_=year_from_, 
                                  year_to=year_to, min_rating=min_rating, order_by=order_by,
                                  desc=desc)

    return jsonify(movies)

@games_bp.route("/", methods=["POST"])
def add_game():
    data = request.json
    titulo = data.get("titulo")
    genero = data.get("genero")
    anio = validar_entero(data.get("anio"))
    desarrolladora = data.get("desarrolladora")
    rating = validar_float(data.get("rating"))
    imagen = data.get("imagen")

    if anio is None:
        return jsonify({
            "message": "El año debe ser un numero valido"
        }), 400

    if not titulo or not desarrolladora:
        return jsonify({
            "message": "Titulo, genero y año son obligatorios"
        }), 400
    
    if rating is None and rating not in (None, ""):
        return jsonify({
            "message": "El rating debe ser un numero valido"
        }), 400
    
    new_id = create_game(titulo, genero, anio, desarrolladora, rating, imagen)
    return jsonify({
        "message": "Juego creado",
        "id": new_id
    }), 201

@games_bp.route("/<int:id>", methods=["PUT"])
def edit_game(id):
    data = request.json
    game = get_Game_By_Id(id)
    if not game:
        return jsonify({
            "message": "No encontrado"
        }), 404
    
    titulo = data.get("titulo")
    genero = data.get("genero")
    anio = validar_entero(data.get("anio"))
    desarrolladora = data.get("desarrolladora")
    rating = validar_float(data.get("rating"))
    imagen = data.get("imagen")
    
    if anio is None:
        return jsonify({
            "message": "El año debe ser un numero valido"
        }), 400

    if rating is None and rating not in (None, ""):
        return jsonify({
            "message": "El rating debe ser un numero valido"
        }), 400
    
    result = update_game(id, titulo, genero, anio, desarrolladora, rating, imagen)
    if result:
        return jsonify({
            "message": "Juego actualizado"
        })
    else:
        return jsonify({
            "message": "Faltan Valores"
        }), 400

@games_bp.route("/<int:id>", methods=["DELETE"])
def remove_game(id):
    game = get_Game_By_Id(id)
    if not game:
        return jsonify({
            "message": "Juego no encontrado"
        }), 404
    
    if delete_game(id):
        return jsonify({
            "message": "Juego eliminado"
        })
    else:
        return jsonify({
            "message": "Error al eliminar el juego"
        }), 500