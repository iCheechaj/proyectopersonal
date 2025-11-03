from flask import Flask
from flask_cors import CORS
from routes.games import games_bp
from database import get_db

#Instancia de Flask
app = Flask(__name__)
CORS(app)

#Endpoint root
@app.route("/")
def hello():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT NOW()")
        result = cursor.fetchone()
        return{ "time": str(result[0]) }
    except Exception as e:
        return{"error": str(e)}

#Registro de blueprints
app.register_blueprint(games_bp, url_prefix="/games")


#Punto de partida
if __name__ == "__main__":
    app.run(debug=True)
