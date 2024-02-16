from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db. ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Workouts(db.Model):
    __tablename__ = 'Workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, name='Name')
    muscleGroup = db.Column(db.String(100), nullable=False, name='Muscle Group')
    equipType = db.Column(db.String(100), nullable=False, name='EquipType')  

    def __repr__(self):
        return (f"Workouts(name={self.name}, muscleGroup={self.muscleGroup}," + 
                f"equipType={self.equipType})")
