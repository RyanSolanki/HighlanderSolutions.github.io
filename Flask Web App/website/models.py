from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from .access import DbAccessSingleton

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userId = db.Column(db.Integer, db. ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150), name='first_name')
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
    def __init__(self, exerciseData):
        self.exerciseName = exerciseData['name']
        self.sets = exerciseData['sets']
        self.reps = exerciseData['reps']
        self.weight = exerciseData['weights']
    
    def print_exercise(self):
        print("Exercise Name:", self.exerciseName)
        print("Sets:", self.sets)
        print("Reps:", self.reps)
        print("Weight:", self.weight)
        print("")        

    def update_exercise(self, exerciseName, sets, reps, weight):
        self.exerciseName = exerciseName
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def update_exercise_name(self, exerciseName):
        self.exerciseName = exerciseName

    def update_sets(self, sets):
        self.sets = sets

    def update_reps(self, reps):
        self.reps = reps

    def update_weight(self, weight):
        self.weight = weight

class UserWorkout():
    def __init__(self, workoutData):
        self.workoutName = workoutData['name']
        self.exerciseList = []

        for workout in workoutData['exercises']:
            self.exerciseList.append(UserExercise(workout))

    def to_dict(self):
        tempDict = {}
        tempDict['name'] = self.workoutName
        tempDict['exercises'] = [exercise.__dict__ for exercise in self.exerciseList]
        for exercise in tempDict['exercises']:
            exercise['reps'] = [int(rep) for rep in exercise['reps']]
            exercise['weight'] = [int(weight) for weight in exercise['weight']]

        return tempDict   
    
    def print_workout(self):
        print("Workout Name:", self.workoutName)
        for exercise in self.exerciseList:
            exercise.print_exercise()

    def save_workout_db(self):
        # Connect to the database access singleton
        dbInstance = DbAccessSingleton.get_instance()
        # Get the current id for the saved workouts
        currentId = dbInstance.custom_query("SELECT MAX(id) FROM SavedWorkouts")[0][0] + 1
        # Iterate through the exercises in the workout
        for exercise in self.exerciseList:
            # Convert each integer in the list to a string
            repsAsStrings = [str(rep) for rep in exercise.reps]
            # Join the strings with a separator (e.g., comma)
            repsString = ', '.join(repsAsStrings)

            # Convert each integer in the list to a string
            weightAsStrings = [str(weight) for weight in exercise.weight]
            # Join the strings with a separator (e.g., comma)
            weightString = ', '.join(weightAsStrings)

            # Insert the workout into the database
            dbInstance.insert('SavedWorkouts', f"({currentId}, '{current_user.email}', '{self.workoutName}',  '{exercise.exerciseName}', {exercise.sets}, '{repsString}', '{weightString}')")
            currentId += 1

    def get_workout_db(self):
        # Connect to the database access singleton
        dbInstance = DbAccessSingleton.get_instance()
        # Get the workout from the database
        workout = dbInstance.custom_query(f"SELECT * FROM SavedWorkouts WHERE WorkoutName = " +
                                           f"'{self.workoutName}' AND UserID = '{current_user.email}'")
        # Iterate through the exercises in the workout
        for exercise in workout:
            # Check if the value is a string before splitting
            if isinstance(exercise[5], str):
                reps = [int(rep) for rep in exercise[5].split(',')]
            else:
                # Handle the case where the value is not a string
                reps = []  # or any other appropriate default value
            if isinstance(exercise[6], str):
                weights = [int(weight) for weight in exercise[6].split(',')]
            else:
                weights = []  # or any other appropriate default value
            #print(f"exercise[1] = {exercise[1]}, exercise[2] = {exercise[2]}, exercise[3] = {exercise[3]}, exercise[4] = {exercise[4]}, exercise[5] = {exercise[5]}, exercise[6] = {exercise[6]}")
            #print(f"Name: {exercise[3]}, Sets: {exercise[4]}, Reps: {reps}, Weights: {weights} ")
            userExercise = UserExercise({'name': exercise[3], 'sets': exercise[4], 
                                         'reps': reps, 'weights': weights})
            #userExercise.printExercise()
            self.exerciseList.append(userExercise)

class ScheduledWorkouts(db.Model):
    __tablename__ = 'ScheduledWorkouts'
    date = db.Column(db.String, primary_key=True)
    workoutName = db.Column(db.String)
    userID = db.Column(db.String)

    def __init__(self, date, workoutName, userID):
        self.date = date
        self.workoutName = workoutName
        self.userID = userID 
