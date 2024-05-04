import sqlite3
import sys
from test_data import data

#############################################
# 

# CONSISTENCIES
# - ID is always capitalized


class DataBaseAPI():
    # --------------------------------- create table
    def create(self, dbName):
        conn = sqlite3.connect(dbName)
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Recipe(
                    recID INTEGER PRIMARY KEY, 
                    recName VARCHAR(20)
                    );""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Ingredient(
                    ingID INTEGER PRIMARY KEY, 
                    recID INTEGER, 
                    ing VARCHAR(100),
                    FOREIGN KEY (recID) REFERENCES Recipe(recID)
                    );""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Instruction(
                    instructionID INTEGER PRIMARY KEY, 
                    recID INTEGER, 
                    instruction VARCHAR(100),
                    FOREIGN KEY (recID) REFERENCES Recipe(recID)
                    );""")


        conn.commit()
        conn.close()


    # --------------------------------- fill table
    def fill(self, dbName, recName, ingredients, instructions):
        conn = sqlite3.connect(dbName)
        cur = conn.cursor()

        cur.execute("INSERT INTO Recipe (recName) VALUES(?)", (recName,))
        recID = cur.lastrowid

        for ing in ingredients:
            cur.execute("INSERT INTO Ingredient (recID, ing) VALUES(?, ?)", (recID, ing))

        for instruction in instructions:
            cur.execute("INSERT INTO Instruction (recID, instruction) VALUES(?, ?)", (recID, instruction))

        conn.commit()
        conn.close()

    
    # --------------------------------- tear down
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
            conn.close() 


    # --------------------------------- fetch recipe name
    """
    Queries the DB for the name and ID. Gets sent to /recipes so that
    each name can be a list item as a link to the full recipe
    """
    def fetchRecipeNames(self, dbName):
        try:
            conn = sqlite3.connect(dbName)
            cur = conn.cursor()

            # grab all recipe names
            cur.execute("SELECT recName, recID FROM Recipe")
            recipes = cur.fetchall()

            # recipe_names = [recipe[0] for recipe in recipes]
            # recIDs = [recipe[1] for recipe in recipes]
            conn.commit()
            return recipes
        
        except sqlite3.Error as e:
            print(f'Error retrieving names: {e}')
        
        finally:
            conn.close() 


    # --------------------------------- get full recipe
    """
    Grabs recipe name, all ingredients, and instructions from
    all three tables. 
    """
    def getFullRecipe(self, dbName, recID):
        try:
            # first, retrieve recipes from db
            conn = sqlite3.connect(dbName)
            cur = conn.cursor()

            # grabs recipe name
            cur.execute("SELECT recName FROM Recipe WHERE recID = ?", (recID,))
            recipe_name = cur.fetchone()[0]

            # grabs all ingredients
            cur.execute("SELECT * FROM Ingredient WHERE recID = ?", (recID,))
            ingredients = [row[2] for row in cur.fetchall()]

            # grabs all instructions
            cur.execute("SELECT * FROM Instruction WHERE recID = ?", (recID,))
            instructions = [row[2] for row in cur.fetchall()]

            return recipe_name, ingredients, instructions
        
        except sqlite3.Error as e:
            print(f'Error retrieving full recipe: {e}')
        
        finally:
            conn.close() 
        
# --------------------------------- testing 
    
if __name__ == "__main__":
    dbName = 'test.db'

    newDB = DataBaseAPI()
    newDB.create(dbName)

    for recipe in data['recipes']:
        # recID = recipe['recID']
        recName = recipe['recName']
        recIngredients = recipe['recIngredients']
        recInstructions = recipe['recInstructions']
        newDB.fill(dbName, recName, recIngredients, recInstructions)
