from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from .access import DbAccessSingleton

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

class Exercises(db.Model):
    __tablename__ = 'Exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, name='Name')
    muscleGroup = db.Column(db.String(100), nullable=False, name='MuscleGroup')
    equipType = db.Column(db.String(100), nullable=False, name='EquipType')  

    def __repr__(self):
        return (f"Exercises(name={self.name}, muscleGroup={self.muscleGroup}," + 
                f"equipType={self.equipType})")
    
class UserExercise():
    def __init__(self, exercise_data):
        self.exerciseName = exercise_data['name']
        self.sets = exercise_data['sets']
        self.reps = exercise_data['reps']
        self.weight = exercise_data['weights']
    
    def printExercise(self):
        print("Exercise Name:", self.exerciseName)
        print("Sets:", self.sets)
        print("Reps:", self.reps)
        print("Weight:", self.weight)
        print("")        

    def updateExercise(self, exerciseName, sets, reps, weight):
        self.exerciseName = exerciseName
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def updateExerciseName(self, exerciseName):
        self.exerciseName = exerciseName

    def updateSets(self, sets):
        self.sets = sets

    def updateReps(self, reps):
        self.reps = reps

    def updateWeight(self, weight):
        self.weight = weight

class UserWorkout():
    def __init__(self, workout_data):
        self.workoutName = workout_data['name']
        self.exerciseList = []

        for workout in workout_data['exercises']:
            self.exerciseList.append(UserExercise(workout))
            
    
    def printWorkout(self):
        print("Workout Name:", self.workoutName)
        for exercise in self.exerciseList:
            exercise.printExercise()

    def saveWorkoutDB(self):
        # Connect to the database access singleton
        db_instance = DbAccessSingleton.get_instance()
        # Get the current id for the saved workouts
        currentId = db_instance.custom_query("SELECT MAX(id) FROM SavedWorkouts")[0][0] + 1
        # Iterate through the exercises in the workout
        for exercise in self.exerciseList:
            # Convert each integer in the list to a string
            reps_as_strings = [str(rep) for rep in exercise.reps]
            # Join the strings with a separator (e.g., comma)
            reps_string = ', '.join(reps_as_strings)

            # Convert each integer in the list to a string
            weight_as_strings = [str(weight) for weight in exercise.weight]
            # Join the strings with a separator (e.g., comma)
            weight_string = ', '.join(weight_as_strings)

            # Insert the workout into the database
            db_instance.insert('SavedWorkouts', f"({currentId}, '{current_user.email}', '{self.workoutName}',  '{exercise.exerciseName}', {exercise.sets}, '{reps_string}', '{weight_string}')")
            currentId += 1

class ScheduledWorkouts(db.Model):
    __tablename__ = 'ScheduledWorkouts'
    date = db.Column(db.String, primary_key=True)
    workoutName = db.Column(db.String)

    def __init__(self, date, workoutName):
        self.date = date
        self.workoutName = workoutName

class SavedWorkouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.TEXT)
    WorkoutName = db.Column(db.TEXT)
    ExerciseName = db.Column(db.TEXT)
    NumberOfSets = db.Column(db.INTEGER)
    NumberOfReps = db.Column(db.TEXT)
    Weights = db.Column(db.TEXT)
