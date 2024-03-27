from flask import Flask, render_template, request, jsonify
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/save_to_database', methods=['POST'])
def save_to_database():
    data = request.json
    name_list = data['name']

    # add the ingredients to the db

    return jsonify({"message": "data received and processed"})
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

# debugger ON
if __name__ == '__main__':
    app.run(debug=True)