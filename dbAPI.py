from test_data import data
import psycopg2
from psycopg2 import Error
import os


class DataBaseAPI():
    # --------------------------------- create table
    """
    Creates three new tables, Recipe, Ingredient, Instruction
    """
    def create(self):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            cur = conn.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS Recipe(
                        recID SERIAL PRIMARY KEY, 
                        recName VARCHAR(255)
                        );""")
            
            cur.execute("""CREATE TABLE IF NOT EXISTS Ingredient(
                        ingID SERIAL PRIMARY KEY, 
                        recID INTEGER, 
                        ing VARCHAR(255),
                        FOREIGN KEY (recID) REFERENCES Recipe(recID)
                        );""")
            
            cur.execute("""CREATE TABLE IF NOT EXISTS Instruction(
                        instructionID SERIAL PRIMARY KEY, 
                        recID INTEGER, 
                        instruction TEXT,
                        FOREIGN KEY (recID) REFERENCES Recipe(recID)
                        );""")

            conn.commit()

        except Error as e:   
            print(f'Error creating tables: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- fill table
    """
    Given the intake parameters, inserts relavent info into correct tables.
    """
    def fill(self, recName, ingredients, instructions):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            
            cur = conn.cursor()

            cur.execute("INSERT INTO Recipe (recName) VALUES(%s) RETURNING recID", (recName,))
            recID = cur.fetchone()[0]  # Fetch the returned recID from the INSERT
            print(f"Generated recID: {recID}")

            for ing in ingredients:
                cur.execute("INSERT INTO Ingredient (recID, ing) VALUES(%s, %s)", (recID, ing))

            for instruction in instructions:
                cur.execute("INSERT INTO Instruction (recID, instruction) VALUES(%s, %s)", (recID, instruction))
            conn.commit()
        
        except Error as e:
            print(f'Error filling tables: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- fetch recipe name
    """
    Queries the DB for the name and ID. Gets sent to /recipes so that
    each name can be a list item as a link to the full recipe
    """
    def fetchRecipeNames(self):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            cur = conn.cursor()

            # grab all recipe names
            cur.execute("SELECT recName, recID FROM Recipe")
            recipes = cur.fetchall()

            return recipes
        
        except Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- get full recipe
    """
    Grabs recipe name, all ingredients, and instructions from
    all three tables. 
    """
    def getFullRecipe(self, recID):
        conn = None
        try:
            # first, retrieve recipes from db
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            
            cur = conn.cursor()

            # grabs recipe name
            cur.execute("SELECT recName FROM Recipe WHERE recID = %s", (recID,))
            recipe_name = cur.fetchone()[0]

            # grabs all ingredients
            cur.execute("SELECT * FROM Ingredient WHERE recID = %s", (recID,))
            ingredients = [row[2] for row in cur.fetchall()]

            # grabs all instructions
            cur.execute("SELECT * FROM Instruction WHERE recID = %s", (recID,))
            instructions = [row[2] for row in cur.fetchall()]

            return recipe_name, ingredients, instructions
        
        except Error as e:
            print(f'Error retrieving full recipe: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- edit          
    def editRecipe(self, origName, recName, ingredients, instructions):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            
            cur = conn.cursor()

            # grab recID using name (FIGURE OUT HOW TO SEND IT VIA ROUTE)
            # use original name to avoid conflicts after changing the name.
            cur.execute("SELECT recID from Recipe WHERE recName=%s", (origName,))
            result = cur.fetchone()
            if result is None:
                raise Exception("RECIPE NOT FOUND.")
            else:
                recID = result[0]

            # update name
            cur.execute("UPDATE Recipe SET recName=%s WHERE recID=%s", (recName, recID))

            # Delete old ingredients and instructions and insert new ones
            cur.execute("DELETE FROM Ingredient WHERE recID=%s", (recID,))
            for ing in ingredients:
                cur.execute("INSERT INTO Ingredient (recID, ing) VALUES (%s, %s)", (recID, ing))
            
            cur.execute("DELETE FROM Instruction WHERE recID=%s", (recID,))
            for instr in instructions:
                cur.execute("INSERT INTO Instruction (recID, instruction) VALUES (%s, %s)", (recID, instr))

            conn.commit()

        except Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- delete
    def deleteRecipe(self, recID):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            
            cur = conn.cursor()

            cur.execute("DELETE FROM Ingredient WHERE recID=%s", (recID,))

            cur.execute("DELETE FROM Instruction WHERE recID=%s", (recID,))

            cur.execute("DELETE FROM Recipe WHERE recID=%s", (recID,))

            conn.commit()
        except Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            if conn is not None:
                conn.close() 
        

        
    # --------------------------------- delete
    def getID(self, recName):
        conn = None
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                raise Exception("DATABASE_URL not found. Check your Heroku configuration.")
            conn = psycopg2.connect(database_url)
            
            cur = conn.cursor()

            cur.execute("SELECT recID FROM Recipe WHERE recName=%s", (recName,))
            result = cur.fetchone()
            recID = result[0]

            return recID

        except Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            if conn is not None:
                conn.close() 
# --------------------------------- testing 
    
# if __name__ == "__main__":
#     dbName = 'test.db'

#     newDB = DataBaseAPI()
#     newDB.create(dbName)

#     for recipe in data['recipes']:
#         # recID = recipe['recID']
#         recName = recipe['recName']
#         recIngredients = recipe['recIngredients']
#         recInstructions = recipe['recInstructions']
#         newDB.fill(dbName, recName, recIngredients, recInstructions)
