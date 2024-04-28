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

# -------[POST] /favorite/people/<int:planet_id> Añade un nuevo people favorito al usuario actual con el id = people_id.------
@app.route("/favorite/people/<int:people_id>", methods=["POST"])
# @jwt_required()
def add_favorite_people(people_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    people_exist = People.query.filter_by(id=people_id).first()
    if people_exist is None:
        return ({"msg": "This people doesn't exist"}), 400
    else:
        exist_favorite_people = FavoritePeople.query.filter_by(people_id=people_id, usuario_id=user_id).first()
        if exist_favorite_people is None:
            new_favorite_people = FavoritePeople(people_id=people_id, usuario_id=user_id)
            db.session.add(new_favorite_people)
            db.session.commit()
            return jsonify({"msg": "People added to favorites"}), 201
        else:  
            return jsonify({'msg': 'People has already exist in favorites'}), 400
        
# -------[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.------
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
# @jwt_required()
def add_favorite_planet(planet_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    planet_exist = Planet.query.filter_by(id=planet_id).first()
    if planet_exist is None:
        return ({"msg": "This planet doesn't exist"}), 400
    else:
        exist_favorite_planet = FavoritePlanet.query.filter_by(planet_id=planet_id, usuario_id=user_id).first()
        if exist_favorite_planet is None:
            new_favorite_planet = FavoritePlanet(planet_id=planet_id, usuario_id=user_id)
            db.session.add(new_favorite_planet)
            db.session.commit()
            return jsonify({"msg": "Planet added to favorites"}), 201
        else:  
            return jsonify({'msg': 'Planet has already exist in favorites'}), 400
        
# -------[POST] /favorite/planet/<int:vehicle_id> Añade un nuevo vehiculo favorito al usuario actual con el id = vehicle_id.------
@app.route("/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
# @jwt_required()
def add_favorite_vehicle(vehicle_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return ({"msg": "This vehicle doesn't exist"}), 400
    else:
        exist_favorite_vehicle = FavoriteVehicle.query.filter_by(vehicle_id=vehicle_id, usuario_id=user_id).first()
        if exist_favorite_vehicle is None:
            new_favorite_vehicle = FavoriteVehicle(vehicle_id=vehicle_id, usuario_id=user_id)
            db.session.add(new_favorite_vehicle)
            db.session.commit()
            return jsonify({"msg": "vehicle added to favorites"}), 201
        else:  
            return jsonify({'msg': 'vehicle has already exist in favorites'}), 400
        

# -------[DELETE] /favorite/people/<int:planet_id> Borra el people favorito al usuario actual con el id = people_id.------
@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
# @jwt_required()
def delete_favorite_people(people_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    people_exist = People.query.filter_by(id=people_id).first()
    if people_exist is None:
        return ({"msg": "There are not favorites peoples"}), 400
    else:
        exist_favorite_people = FavoritePeople.query.filter_by(people_id=people_id, usuario_id=user_id).first()
        if exist_favorite_people:
            db.session.delete(exist_favorite_people)
            db.session.commit()
            return jsonify({"msg": "People delete to favorites"}), 200
        else:  
            return jsonify({'msg': "People doesn't exist in favorites"}), 400


# -------[DELETE] /favorite/planet/<int:planet_id> Borra el planet favorito al usuario actual con el id = planet_id.------
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
# @jwt_required()
def delete_favorite_planet(planet_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    planet_exist = Planet.query.filter_by(id=planet_id).first()
    if planet_exist is None:
        return ({"msg": "There are not favorites planets"}), 400
    else:
        exist_favorite_planet = FavoritePlanet.query.filter_by(planet_id=planet_id, usuario_id=user_id).first()
        if exist_favorite_planet:
            db.session.delete(exist_favorite_planet)
            db.session.commit()
            return jsonify({"msg": "Planet delete to favorites"}), 200
        else:  
            return jsonify({'msg': "Planet doesn't exist in favorites"}), 400


# -------[DELETE] /favorite/vehicle/<int:vehicle_id> Borra el vehiculo favorito al usuario actual con el id = vehicle_id.------
@app.route("/favorite/vehicle/<int:vehicle_id>", methods=["DELETE"])
# @jwt_required()
def delete_favorite_vehicle(vehicle_id): 
    # email = get_jwt_identity()
    # user_exist = User.query.filter_by(email=email).first()
    # user_id = user_exist.id
    user_id = 1
    vehicle_exist = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_exist is None:
        return ({"msg": "There are not favorites vehicles"}), 400
    else:
        exist_favorite_vehicle = FavoriteVehicle.query.filter_by(vehicle_id=vehicle_id, usuario_id=user_id).first()
        if exist_favorite_vehicle:
            db.session.delete(exist_favorite_vehicle)
            db.session.commit()
            return jsonify({"msg": "Vehicle delete to favorites"}), 200
        else:  
            return jsonify({'msg': "Vehicle doesn't exist in favorites"}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
