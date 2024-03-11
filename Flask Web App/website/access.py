import sqlite3 as sq
import os

class DbAccessSingleton(object):
    _instance = None
    
    def __init__(cls): # If there is no DbAccessSingleton class already, create a new one. Otherwise, return the old one.
        raise RuntimeError("call get_instance() instead")
    
    # Class declaration    
    # newclass = DbAccessSingleton.get_instance()
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    
    
    # .search() has 4 inputs: (table, return, column searched, keyword)
    # search() inputs a search query to the database
    
    # This call to search is returning the MuscleGroup of the entire table for Exercises.
    # newclass.search('Exercises', 'MuscleGroup', None, None)

    # This call to search is returning all the information of Exercises that have the Name 'Push-ups'
    # newclass.search('Exercises', '*', 'Name', "'Push-ups'")
    
    # It is to note that searches looking for a specific text entry need to have double quotes
    def search(self, table, column, query_col, query):
        # Get the absolute path of the current script
        current_script_path = os.path.abspath(__file__)
        # Define the base directory as the parent of the 'tests' directory
        base_dir = os.path.dirname(os.path.dirname(current_script_path))
        # Construct the absolute path to the database file
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        con = sq.connect(db_path)
        cur = con.cursor()
    
        if query is None: # Select a column
            result = cur.execute(f"SELECT {column} FROM {table}").fetchall()
        else: # Specific Query
            result = cur.execute(f"SELECT {column} FROM {table} WHERE {query_col} = {query}").fetchall()
        
        con.close()  # Close the connection
        return result
    
    
    
    # .custom_query() has only one input: (text)
    # I made a separate search function for this under the idea that we might need to input more complicated queries outside of the format presented within .search() 
    # This function will not work for custom inserts
    
    # This call to custom_query is essentially the same as the second example above
    # newclass.custom_query("SELECT * FROM Exercises WHERE Name = 'Push-ups'")
    def custom_query(self, text):
        # Connect to database and add cursor

        # Get the absolute path of the current script
        current_script_path = os.path.abspath(__file__)
        # Define the base directory as the parent of the 'tests' directory
        base_dir = os.path.dirname(os.path.dirname(current_script_path))
        # Construct the absolute path to the database file
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        con = sq.connect(db_path)
        cur = con.cursor()
        
        result = cur.execute(text).fetchall()
        con.close()  # Close the connection
        return result
    
    
    
    # .insert has 2 inputs: (table, values)
    
    # This call is to insert is inputting a new entry in the database
    # newclass.insert('SavedWorkouts', "(3, 'a123', 'My Workout', 'Push-ups', 2, 'Until failure', 'None')")
    def insert(self, table, values):
        # Connect to database and add cursor
        # Get the absolute path of the current script
        current_script_path = os.path.abspath(__file__)
        # Define the base directory as the parent of the 'tests' directory
        base_dir = os.path.dirname(os.path.dirname(current_script_path))
        # Construct the absolute path to the database file
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        con = sq.connect(db_path)
        cur = con.cursor()
        
        # Run insert query
        cur.execute(f"INSERT INTO {table} VALUES {values}")
        con.commit()
        con.close()  # Close the connection


    # This call is to update an existing row in the database with new values
    #*********************** EXAMPLE FUNCTION CALL *************************#
    # # Specify the update parameters
    # table_name = "SavedWorkouts"
    # set_values = 'NumberOfSets = ?, NumberOfReps = ?, Weights = ?'
    # where_condition = 'UserID = ? AND WorkoutName = ? AND ExerciseName = ?'
    # new_sets = 3
    # new_reps = "8, 7, 6"
    # new_weights = "225, 205, 185"
    # username = "ryansolanki"
    # workout_name = "Ryan Chest Day"
    # exercise_name = "Bench Press"

    # # Update the record in the database
    # db_instance.update(table_name, set_values, where_condition, (new_sets, new_reps, new_weights, username, workout_name, exercise_name))
        
    def update(self, table, set_values, where_condition,values):
        # Get the absolute path of the current script
        current_script_path = os.path.abspath(__file__)
        # Define the base directory as the parent of the 'tests' directory
        base_dir = os.path.dirname(os.path.dirname(current_script_path))
        # Construct the absolute path to the database file
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        con = sq.connect(db_path)
        # Run update query with parameterized query
        cur = con.cursor()
        cur.execute(f"UPDATE {table} SET {set_values} WHERE {where_condition}", values)
        con.commit()
        con.close()  # Close the connection
       
