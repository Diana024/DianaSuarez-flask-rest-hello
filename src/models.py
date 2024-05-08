from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    birth_year = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    # films = db.Column(db.String(250), unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    favorites_people = db.relationship("FavoritePeople", backref="peoples", lazy=True )

    def __repr__(self):
            return '<People %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "birth_year": self.birth_year, 
                "eye_color": self.eye_color,
                # "films": self.films,
                "hair_color":self.hair_color
                # do not serialize the password, its a security breach
            }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)	
    created	= db.Column(db.String(250), unique=False, nullable=False)
    diameter = db.Column(db.String(250), unique=False,nullable=False)
    edited	= db.Column(db.String(250), unique=False, nullable=False)
    favorites_planet = db.relationship("FavoritePlanet", backref="planets", lazy=True )

    def __repr__(self):
            return '<Planet %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "climate":self.climate,
                "created":self.created,
                "diameter":self.diameter,
                "edited":self.edited
                # do not serialize the password, its a security breach
            }
    
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)	
    name = db.Column(db.String(250), nullable=False)	
    properties	= db.Column(db.String(250), nullable=False)
    cargo_capacity = db.Column(db.String(250), nullable=False)	
    consumables	= db.Column(db.String(250), nullable=False)
    cost_in_credits	= db.Column(db.String(250), nullable=False)
    favorites_vehicle = db.relationship("FavoriteVehicle", backref="vehicles", lazy=True )
    
    def __repr__(self):
            return '<Vehicle %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "properties":self.properties,
                "cargo_capacity":self.cargo_capacity,
                "consumables":self.consumables,	
                "cost_in_credits":self.cost_in_credits
                # do not serialize the password, its a security breach
            }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    # favorites_people = db.relationship("FavoritePeople", backref="user", lazy=True) 
    # favorites_planet = db.relationship("FavoritePlanet", backref="user", lazy=True)
    # favorites_vehicle = db.relationship("FavoriteVehicle", backref="user", lazy=True)
    favorite= db.relationship("Favorite", backref="user", lazy=True)
    def __repr__(self):
            return '<User %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                # do not serialize the password, its a security breach
            }
    
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(250), unique=False, nullable=False)
    

    def __repr__(self):
            return '<Favorite %r>' % self.id

    def serialize(self):
            # result = Favorite.query.filter_by(id=self.name).first()
            # print(result)
            return {
                "id": self.id,
                "name": self.name,
                "usuario_id": self.usuario_id
                
                # do not serialize the password, its a security breach
            }
    
class FavoritePeople(db.Model):
    __tablename__ = 'favoritepeople'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    

    def __repr__(self):
            return '<FavoritePeople %r>' % self.id

    def serialize(self):
            result = FavoritePeople.query.filter_by(id=self.people_name).first()
            # print(result)
            return {
                "id": self.id,
                "people_name": result.serialize()["name"],
                "user_id": self.user_id
                
                # do not serialize the password, its a security breach
            }

class FavoritePlanet(db.Model):
    __tablename__ = 'favoriteplanet'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    

    def __repr__(self):
            return '<FavoritePlanet %r>' % self.id

    def serialize(self):
            return {
                "id": self.id,
                "user_id": self.userid,
                "planet_id": self.planet_id, 
                # do not serialize the password, its a security breach
            }

class FavoriteVehicle(db.Model):
    __tablename__ = 'favoritevehicle'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"))
    

    def __repr__(self):
            return '<FavoriteVehicle %r>' % self.id

    def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "vehicle_id": self.vehicle_id, 
                # do not serialize the password, its a security breach
            }

#  def to_dict(self):
#         return {}

# ## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')