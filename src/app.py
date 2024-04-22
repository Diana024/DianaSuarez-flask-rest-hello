"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicle, Planet
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }
@app.route('/user', methods=['GET'])
def get_user():
    users_query = User.query.all()
    results_users = list(map(lambda item: item.serialize(), users_query))
    
    if results_users == []:
        return jsonify({"msg":"User not found"}), 404
    else:
        return jsonify(results_users), 200

# @app.route('/people', methods=['GET'])
# def get_people():
#     people_query = People.query.all()
#     results_people = list(map(lambda item: item.serialize(), people_query))
    
#     if results_people == []:
#         return jsonify({"msg":"People not found"}), 404
#     else:
#         return jsonify(results_people), 200

# @app.route('/vehicle', methods=['GET'])
# def get_vehicle():
#     vehicle_query = Vehicle.query.all()
#     results_vehicle = list(map(lambda item: item.serialize(), vehicle_query))
    
#     if results_vehicle == []:
#         return jsonify({"msg":"vehicle not found"}), 404
#     else:
#         return jsonify(results_vehicle), 200
    
# @app.route('/planet', methods=['GET'])
# def get_planet():
#     planet_query = Planet.query.all()
#     results_planet = list(map(lambda item: item.serialize(), planet_query))
    
#     if results_planet == []:
#         return jsonify({"msg":"planet not found"}), 404
#     else:
#         return jsonify(results_planet), 200
    
# # -------get_por id------

# @app.route('/people/<int:people_id>', methods=['GET'])
# def get_one_people(people_id):

#     people_query =People.query.filter_by(id=people_id).first()
#     # print(people_query.serialize())

#     if people_query is None:
#         return jsonify({"msg":"People info not found"}), 404
#     else:
#         return jsonify(people_query.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
