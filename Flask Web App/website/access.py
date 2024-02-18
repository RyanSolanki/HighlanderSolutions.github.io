import sqlite3 as sq

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
        # Connect to database and add cursor
        con = sq.connect('Flask Web App/instance/database.db')
        cur = con.cursor()
    
        if query is None: # Select a column
            return cur.execute(f"SELECT {column} FROM {table}").fetchall()
        else: # Specific Query
            return cur.execute(f"SELECT {column} FROM {table} WHERE {query_col} = {query}").fetchall()
    
    
    
    # .custom_query() has only one input: (text)
    # I made a separate search function for this under the idea that we might need to input more complicated queries outside of the format presented within .search() 
    # This function will not work for custom
    
    # This call to custom_query is essentially the same as the second example above
    # newclass.custom_query("SELECT * FROM Exercises WHERE Name = 'Push-ups'")
    def custom_query(self, text):
        # Connect to database and add cursor
        con = sq.connect('Flask Web App/instance/database.db')
        cur = con.cursor()
        
        return cur.execute(text).fetchall()
    
    
    
    # .insert has 2 inputs: (table, values)
    
    # This call to insert is inputting a new entry for the SavedWorkouts table
    # newclass.insert('SavedWorkouts', "(3, 'a123', 'My Workout', 'Push-ups', 2, 'Until failure', 'None')")
    def insert(self, table, values):
        # Connect to database and add cursor
        con = sq.connect('Flask Web App/instance/database.db')
        cur = con.cursor()
        
        # Run insert query
        cur.execute(f"INSERT INTO {table} VALUES {values}")
        con.commit()
       