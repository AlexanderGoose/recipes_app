from flask import Flask, render_template, request, redirect, url_for
from test_data import data
import sqlite3
import psycopg2
from dbAPI import DataBaseAPI

app = Flask(__name__)



# -------------------------------------------- home page
"""
Home screen will be a welcome and possibly a search bar.
User will then navigate via navbar to where they want to go
"""
@app.route('/')
def home():
    # if DB doesn't exist, create it!
    # dbAPI = DataBaseAPI()
    # dbName = 'recipe.db'
    # dbAPI.create(dbName)
    conn = psycopg2.connect("postgres://xvwhmevsifgbur:1ded6238d2e4c0f2fa5b574f43bb82c47c7d899ddb39f222874a90d872907d1a@ec2-52-72-109-141.compute-1.amazonaws.com:5432/d3o4h6fng8cunu")
    conn.close()
    return "Database connection successful."
    # return render_template('index.html')



# -------------------------------------------- view ALL recipes (by name)
"""
This route will simply show a list of all recipes that the user
has access to. When a recipe is clicked, it will take to viewRec
and fill in the <dbName> and <int:recID>
"""
@app.route('/recipes/<dbName>', methods=['GET', 'POST'])
def recipes(dbName):
    
    # teardown
    if request.method == 'POST':
        dbAPI = DataBaseAPI()
        # delete all tables to get rid of the db
        dbAPI.teardown(dbName)

        # recreate tables, now should be empty
        # dbAPI.create(dbName)
        return redirect(url_for('home'))

    # here we grab the recipe names
    dbAPI = DataBaseAPI()
    recipes = dbAPI.fetchRecipeNames(dbName)

    recipe_names = [recipe[0] for recipe in recipes]
    recIDs = [recipe[1] for recipe in recipes]

    # return render_template('recipes.html', recipe_names=recipe_names,
    #                        recIDs=recIDs)
    return render_template('recipes.html', recipes=recipes)


# -------------------------------------------- view recipe
"""
Routes to ONE recipe at a time. The URL includes the dbName as well
as the recID (int). Current example: http://127.0.0.1:5000/viewRec/test.db/1
"""
@app.route('/viewRec/<dbName>/<int:recID>', methods=['GET'])
def viewRec(dbName, recID):

    dbAPI = DataBaseAPI()
    recipe_name, ingredients, instructions = dbAPI.getFullRecipe(dbName, recID)

    if recipe_name is None:
        return "Recipe not found :(", 404

    return render_template('viewRecipes.html', recipe_name=recipe_name, 
                           ingredients=ingredients, instructions=instructions)



# -------------------------------------------- add recipe
"""
Will have a form to add new recipe. Function must be able to 
take in the info, add to the db (using dbAPI.py ?????). Once
complete, wipe the page and say complete.
"""
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():

    # when form data is sent, 
    if request.method == 'POST':
        recipe_name = request.form.get('new_recipe_name')

        ingredients = request.form.getlist('ingredient')
        ingredients = [ing for ing in ingredients if ing.strip()] # filter out empty entries

        instructions = request.form.getlist('instruction')
        instructions = [inst for inst in instructions if inst.strip()] # filter out empty entries

        rec_id = 100
        dbName = 'recipe.db'

        # creating an instance of the class
        dbAPI = DataBaseAPI()
        dbAPI.fill(dbName, recipe_name, ingredients, instructions)

        return render_template('viewRecipes.html', recipe_name=recipe_name, 
                               ingredients=ingredients, instructions=instructions,
                               rec_id=rec_id)

    return render_template('addRecipe.html')


@app.route('/about')
def about():
    return render_template('about.html')



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
# TO RUN VIRTUAL ENVIRONMENT: source venv/bin/activate