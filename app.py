from flask import Flask, render_template, request
from dbAPI import DataBaseAPI

app = Flask(__name__)

# testing push issue by making this change

# -------------------------------------------- home page
"""
Home screen will be a welcome and possibly a search bar.
User will then navigate via navbar to where they want to go
"""
@app.route('/')
def home():
    # if DB doesn't exist, create it!
    dbAPI = DataBaseAPI()
    dbAPI.create()
    return render_template('index.html')



# -------------------------------------------- view ALL recipes (by name)
"""
This route will simply show a list of all recipes that the user
has access to. When a recipe is clicked, it will take to viewRec
and fill in the <dbName> and <int:recID>
"""
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():

    # here we grab the recipe names
    dbAPI = DataBaseAPI()
    recipes = dbAPI.fetchRecipeNames()

    return render_template('recipes.html', recipes=recipes)



# -------------------------------------------- view recipe
"""
Routes to ONE recipe at a time. The URL includes the dbName as well
as the recID (int). Current example: http://127.0.0.1:5000/viewRec/test.db/1
"""
#@app.route('/viewRec/<dbName>/<int:recID>', methods=['GET'])
@app.route('/viewRec/<int:recID>', methods=['GET', 'POST'])
def viewRec(recID):

    dbAPI = DataBaseAPI()
    recipe_name, ingredients, instructions = dbAPI.getFullRecipe(recID)

    if recipe_name is None:
        return "Recipe not found :(", 404

    return render_template('viewRecipes.html', recipe_name=recipe_name, 
                           ingredients=ingredients, instructions=instructions, recID=recID)

    

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

        # creating an instance of the class
        dbAPI = DataBaseAPI()
        dbAPI.fill(recipe_name, ingredients, instructions)

        recID = dbAPI.getID(recipe_name)
        
        return render_template('viewRecipes.html', recID=recID, recipe_name=recipe_name, 
                               ingredients=ingredients, instructions=instructions)

    return render_template('addRecipe.html')



# -------------------------------------------- begin edit recipe
"""
renders recipe data into a form. allows for editing. form send to editRecipe
"""
@app.route('/beginEditRecipe/<int:recID>', methods=['POST'])
def beginEditRecipe(recID):
    if request.method == 'POST':
        dbAPI = DataBaseAPI()
        recipe_name, ingredients, instructions = dbAPI.getFullRecipe(recID)
        return render_template('editRecipe.html', recID=recID, recipe_name=recipe_name,
                               ingredients=ingredients, instructions=instructions)



# -------------------------------------------- edit recipe
"""
retrieves form data. sends data to db editRecipe func, then
reloads new recipe data to be viewed.
"""
@app.route('/editRecipe/<int:recID>', methods=['GET', 'POST'])
def editRecipe(recID):
    if request.method == 'POST':

        dbAPI = DataBaseAPI()

        original_recipe_name = request.form.get('original_recipe_name')
        recID = request.form.get('recID')

        recipe_name = request.form.get('edit_recipe_name')

        ingredients = request.form.getlist('ingredient')
        ingredients = [ing for ing in ingredients if ing.strip()] # filter out empty entries

        instructions = request.form.getlist('instruction')
        instructions = [inst for inst in instructions if inst.strip()] # filter out empty entries

        dbAPI.editRecipe(original_recipe_name, recipe_name, ingredients, instructions)

        # pull new info after edit
        recipe_name, ingredients, instructions = dbAPI.getFullRecipe(recID)
        # render new recipe details
        return render_template('viewRecipes.html', recipe_name=recipe_name,
                               ingredients=ingredients, instructions=instructions, recID=recID)


@app.route('/deleteRecipe/<int:recID>', methods=['POST'])
def deleteRecipe(recID):
    if request.method == 'POST':
        dbAPI = DataBaseAPI()
        dbAPI.deleteRecipe(recID)

        recipes = dbAPI.fetchRecipeNames()

        return render_template('recipes.html', recipes=recipes)
        #return render_template('recipes.html')

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