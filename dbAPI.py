import sqlite3
from test_data import data
import psycopg2
from psycopg2 import Error


# CONSISTENCIES
# - ID is always capitalized
# - Cammel case is used


class DataBaseAPI():
    # --------------------------------- create table
    """
    Creates three new tables, Recipe, Ingredient, Instruction
    """
    #def create(self, dbName):
    def create(self):
        try:
            #conn = sqlite3.connect(dbName)
            conn = psycopg2.connect("postgres://xvwhmevsifgbur:1ded6238d2e4c0f2fa5b574f43bb82c47c7d899ddb39f222874a90d872907d1a@ec2-52-72-109-141.compute-1.amazonaws.com:5432/d3o4h6fng8cunu")
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

        #except sqlite3.Error as e:
        except Error as e:   
            print(f'Error creating tables: {e}')
        
        finally:
            conn.close() 


    # --------------------------------- fill table
    """
    Given the intake parameters, inserts relavent info into correct tables.
    """
    #def fill(self, dbName, recName, ingredients, instructions):
    def fill(self, recName, ingredients, instructions):
        try:
            #conn = sqlite3.connect(dbName)
            conn = psycopg2.connect("postgres://xvwhmevsifgbur:1ded6238d2e4c0f2fa5b574f43bb82c47c7d899ddb39f222874a90d872907d1a@ec2-52-72-109-141.compute-1.amazonaws.com:5432/d3o4h6fng8cunu")
            cur = conn.cursor()

            #cur.execute("INSERT INTO Recipe (recName) VALUES(?)", (recName,))
            cur.execute("INSERT INTO Recipe (recName) VALUES(%s)", (recName,))
            recID = cur.lastrowid

            for ing in ingredients:
                #cur.execute("INSERT INTO Ingredient (recID, ing) VALUES(?, ?)", (recID, ing))
                cur.execute("INSERT INTO Ingredient (recID, ing) VALUES(%s, %s)", (recID, ing))

            for instruction in instructions:
                #cur.execute("INSERT INTO Instruction (recID, instruction) VALUES(?, ?)", (recID, instruction))
                cur.execute("INSERT INTO Instruction (recID, instruction) VALUES(%s, %s)", (recID, instruction))
            conn.commit()
        
        #except sqlite3.Error as e:
        except Error as e:
            print(f'Error filling tables: {e}')
        
        finally:
            conn.close() 

    
    # --------------------------------- tear down
    """
    used to delete all tables so that they can be restarted. 
    use case is for testing the db and deleting after testing.
    """
    def teardown(self, dbName):
        try:
            conn = sqlite3.connect(dbName)
            cur = conn.cursor()

            # Disable foreign key constraints
            cur.execute("PRAGMA foreign_keys = OFF;")

            cur.execute("DROP TABLE IF EXISTS Recipe;")
            cur.execute("DROP TABLE IF EXISTS Ingredient;")
            cur.execute("DROP TABLE IF EXISTS Instruction;")

            conn.commit()

        except sqlite3.Error as e:
            print(f'Error dropping tables: {e}')
        
        finally:
            if conn is not None:
                conn.close() 


    # --------------------------------- fetch recipe name
    """
    Queries the DB for the name and ID. Gets sent to /recipes so that
    each name can be a list item as a link to the full recipe
    """
    #def fetchRecipeNames(self, dbName):
    def fetchRecipeNames(self):
        try:
            #conn = sqlite3.connect(dbName)
            conn = psycopg2.connect("postgres://xvwhmevsifgbur:1ded6238d2e4c0f2fa5b574f43bb82c47c7d899ddb39f222874a90d872907d1a@ec2-52-72-109-141.compute-1.amazonaws.com:5432/d3o4h6fng8cunu")
            cur = conn.cursor()

            # grab all recipe names
            cur.execute("SELECT recName, recID FROM Recipe")
            recipes = cur.fetchall()

            return recipes
        
        #except sqlite3.Error as e:
        except Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            conn.close() 


    # --------------------------------- get full recipe
    """
    Grabs recipe name, all ingredients, and instructions from
    all three tables. 
    """
    #def getFullRecipe(self, dbName, recID):
    def getFullRecipe(self, recID):
        try:
            # first, retrieve recipes from db
            # conn = sqlite3.connect(dbName)
            conn = psycopg2.connect("postgres://xvwhmevsifgbur:1ded6238d2e4c0f2fa5b574f43bb82c47c7d899ddb39f222874a90d872907d1a@ec2-52-72-109-141.compute-1.amazonaws.com:5432/d3o4h6fng8cunu")
            cur = conn.cursor()

            # grabs recipe name
            #cur.execute("SELECT recName FROM Recipe WHERE recID = ?", (recID,))
            cur.execute("SELECT recName FROM Recipe WHERE recID = %s", (recID,))
            recipe_name = cur.fetchone()[0]

            # grabs all ingredients
            #cur.execute("SELECT * FROM Ingredient WHERE recID = ?", (recID,))
            cur.execute("SELECT * FROM Ingredient WHERE recID = %s", (recID,))
            ingredients = [row[2] for row in cur.fetchall()]

            # grabs all instructions
            #cur.execute("SELECT * FROM Instruction WHERE recID = ?", (recID,))
            cur.execute("SELECT * FROM Instruction WHERE recID = %s", (recID,))
            instructions = [row[2] for row in cur.fetchall()]

            return recipe_name, ingredients, instructions
        
        #except sqlite3.Error as e:
        except Error as e:
            print(f'Error retrieving full recipe: {e}')
        
        finally:
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
