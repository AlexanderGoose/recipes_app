from flask import Flask, render_template, request
from test_data import data
import sqlite3

app = Flask(__name__)


# -------------------------------------------- home page
"""
Home screen will be a welcome and possibly a search bar.
User will then navigate via navbar to where they want to go
"""
@app.route('/home')
def home():
    return render_template('index.html')


# -------------------------------------------- view ALL recipes (by name)
"""
This route will simply show a list of all recipes that the user
has access to. When a recipe is clicked, it will take to viewRec
and fill in the <dbName> and <int:recID>
"""
@app.route('/recipes')
def recipes():
    
    ######## TO DO ########
    # impliment SQL to pull all recipe names and their ID's from db
    # within html file, for loop over it all

    recipe_names = None
    recIDs = None

    return render_template('recipes.html', recipe_names=recipe_names, recIDs=recIDs)


# -------------------------------------------- view recipe
"""
Routes to ONE recipe at a time. The URL includes the dbName as well
as the recID (int). Current example: http://127.0.0.1:5000/viewRec/test.db/1
"""
@app.route('/viewRec/<dbName>/<int:recID>', methods=['GET'])
def viewRec(dbName, recID):
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

    conn.close()

    return render_template('viewRecipes.html', recipe_name=recipe_name, 
                           ingredients=ingredients, instructions=instructions)


# -------------------------------------------- add recipe
"""
Will have a form to add new recipe. Function must be able to 
take in the info, add to the db (using dbAPI.py ?????). Once
complete, wipe the page and say complete.
"""
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    pass


# -------------------------------------------- RUNS APP
if __name__ == '__main__':
    app.run(debug=True)


#####################################################
# TO RUN FLASK APP: flask --app app.py run
# TO RUN SQL: sqlite3 test.db
    # to add columns:
        # .headers on
        # .mode column
    # to quite SQL:
        # .quit