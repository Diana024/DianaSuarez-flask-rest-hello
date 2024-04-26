"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_swagger import swagger # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicle, Planet, FavoritePeople, FavoritePlanet, FavoriteVehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# enpoints

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# -----------endpoint para obtener todos los personajes--------------

@app.route('/people', methods=['GET'])
def get_all_people():
    query_results = People.query.all()
    print(query_results)
    # print(results)
    results = list(map(lambda item: item.serialize(), query_results))
    
    if results == []:
        return jsonify({"msg":"People not found"}), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(results), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planet_query = Planet.query.all()
    results_planet = list(map(lambda item: item.serialize(), planet_query))
    
    if results_planet == []:
        return jsonify({"msg":"planet not found"}), 404
    else:
        return jsonify(results_planet), 200

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    vehicle_query = Vehicle.query.all()
    results_vehicle = list(map(lambda item: item.serialize(), vehicle_query))
    
    if results_vehicle == []:
        return jsonify({"msg":"vehicle not found"}), 404
    else:
        return jsonify(results_vehicle), 200
    

# # -------endpoints para obtener todos los personajes------

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):

    people_query =People.query.filter_by(id=people_id).first()
    # print(people_query.serialize())

    if people_query is None:
        return jsonify({"msg":"People info not found"}), 404
    else:
        return jsonify(people_query.serialize()), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    planet_query =Planet.query.filter_by(id=planet_id).first()
    # print(planet_query.serialize())

    if planet_query is None:
        return jsonify({"msg":"Planet info not found"}), 404
    else:
        return jsonify(planet_query.serialize()), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):

    vehicle_query =Vehicle.query.filter_by(id=vehicle_id).first()
    # print(vehicle_query.serialize())

    if vehicle_query is None:
        return jsonify({"msg":"Vehicle info not found"}), 404
    else:
        return jsonify(vehicle_query.serialize()), 200

# # -------endpoints para obtener usuarios y favoritos------

@app.route('/user', methods=['GET'])
def get_user():
    users_query = User.query.all()
    results_users = list(map(lambda item: item.serialize(), users_query))
    
    if results_users == []:
        return jsonify({"msg":"User not found"}), 404
    else:
        return jsonify(results_users), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():

    all_favorite_people =FavoritePeople.query.filter_by(usuario_id=1).all() 
    all_favorite_people_list= list(map(lambda item: item.serialize(), all_favorite_people))
    all_favorite_planet =FavoritePlanet.query.filter_by(usuario_id=1).all() 
    all_favorite_planet_list= list(map(lambda item: item.serialize(), all_favorite_planet))
    all_favorite_vehicle =FavoriteVehicle.query.filter_by(usuario_id=1).all() 
    all_favorite_vehicle_list= list(map(lambda item: item.serialize(), all_favorite_vehicle))


    if all_favorite_people_list == [] and all_favorite_planet_list == [] and all_favorite_vehicle_list:
        return jsonify({"msg":"User not favorites"}), 404
    
    response_body = {
        "msg": "ok",
        "results": [
            all_favorite_people_list,
            all_favorite_planet_list,
            all_favorite_vehicle_list
        ]
    }

    return jsonify(response_body), 200

# # -------[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.------
# Extract user_id from the request
    user_id = request.json.get('user_id')

    # Check if the user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Check if the planet exists
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    # Check if the planet is already a favorite for the user
    existing_favorite = FavoritePlanets.query.filt

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
