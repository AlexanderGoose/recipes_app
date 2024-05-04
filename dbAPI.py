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
