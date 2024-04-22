from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    birth_year = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    films = db.Column(db.String(250), unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    # favorites_user = db.relationship("Favorites", backref="vehicles", lazy=True )

def __repr__(self):
        return '<People %r>' % self.Peoples

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "birth_year": self.birth_year, 
            "eye_color": self.eye_color,
            "films": self.films,
            "hair_color":self.hair_color
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)	
    created	= db.Column(db.String(250), unique=False, nullable=False)
    diameter = db.Column(db.String(250), unique=False,nullable=False)
    edited	= db.Column(db.String(250), unique=False, nullable=False)

def __repr__(self):
        return '<Planet %r>' % self.Planets

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
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)	
    name = db.Column(db.String(250), nullable=False)	
    properties	= db.Column(db.String(250), nullable=False)
    cargo_capacity = db.Column(db.String(250), nullable=False)	
    consumables	= db.Column(db.String(250), nullable=False)
    cost_in_credits	= db.Column(db.String(250), nullable=False)
    
def __repr__(self):
        return '<Vehicle %r>' % self.Vehicles

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
    # favorites_user = db.relationship("Favorites", backref="user", lazy=True )

def __repr__(self):
        return '<User %r>' % self.username

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

