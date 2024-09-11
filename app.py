from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_restful import Resource, Api, reqparse
import requests
import json

from azuresqlconnector import *

# Create the Flask app
app = Flask(__name__)


@app.route('/searchrecipes')
def recipes():
    return render_template('search_recipes.html')

@app.route('/search_recipe_api', methods=['POST'])
def api_search():
    q_string = "https://api.spoonacular.com/recipes/complexSearch?apiKey=b818cf7fb2d74a918fe080c4ff1799ab&instructionsRequired=True&addRecipeInformation=True&fillIngredients=True&query="+str(request.form['query'])

#    for i in data:
#        q_string=q_string+str("&"+i+"="+str(data[i]))

    r = requests.get(q_string).json()

    recipes=[]
    for i in r["results"]:
        name = i["title"]
        image=i['image']
        id = i["id"]
        summary = i["summary"]

        ingredients = []
        for j in i["extendedIngredients"]:
            ingredients.append([j["name"],j["original"]])

        instructions = []
        for j in i["analyzedInstructions"][0]["steps"]:
            instructions.append(j["step"])

        vegetarian=["vegetarian"]
        vegan=["vegan"]
        glutenFree=["glutenFree"]
        dairyFree=["dairyFree"]
        diets=[]
        if vegetarian:
            diets.append(vegetarian)
        if vegan:
            diets.append(vegan)
        if glutenFree:
            diets.append(glutenFree)
        if dairyFree:
            diets.append(dairyFree)


        recipes.append({"RecipeName":name,"image":image,"ID":id,"Summary":summary,"diets":diets,"Ingredients":ingredients,"Instructions":instructions})

    #fix to keep data and render page
    return render_template('search_recipes.html', recipes=recipes)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str, location='args')
        arguments = parser.parse_args()
        id = arguments['userid']

        data = request.json
        recipeID=data['recipeID']

        q_string = "https://api.spoonacular.com/recipes/"+str(recipeID)+"/information?apiKey=b818cf7fb2d74a918fe080c4ff1799ab&instructionsRequired=True&addRecipeInformation=True&number=1&fillIngredients=True"+str(recipeID)
        r = requests.get(q_string).json()

        name=r['results']['title']
        image=r['results']['image']
        summary=r['results']['summary']
        portions=r['results']['servings']
        insturctions=''
        increment=1
        for i in r['results']['analyzedInstructions'][0]['steps']:
            insturctions='Step '+str(increment)+': '+insturctions+i['step']+'\n'
            increment+=1
        ingredients=''
        for i in r['results']['extendedIngredients']:
            ingredients=ingredients+i['original']+'\n'
        
        badges = []
        
        vegetarian=r['results']["vegetarian"]
        vegan=r['results']["vegan"]
        glutenFree=r['results']["glutenFree"]
        dairyFree=r['results']["dairyFree"]
        diets=[]




        # Initialize SQL connection
        conn = SQLConnection()
        conn = conn.getConnection()
        cursor = conn.cursor()

        sql_query = f""
        
        # Execute the SQL Query
        cursor.execute(sql_query)

        # Fetch the query results
        records = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return jsonify({"message":"entry saved"})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adduser')
def addUser():
    return render_template('add_user.html')

@app.route('/updateuser')
def updateUser():
    return render_template('update_user.html')

@app.route('/')
def startpage():
    return render_template('homepage.html')

@app.route('/landing')
def landing():
    return render_template('landing_page.html')

@app.route('/savedrecipes')
def cookbook():
    return render_template('view_recipes.html')

# This function handles adding a user to the database
@app.route('/adduser', methods=['PUT'])
def add_user():
    user = request.form['username']
    secret = request.form['password']
    user_id = request.form[str(hash('username'))]

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        INSERT INTO exampel.table
        VALUES (
        '{user_id}',
        '{user}',
        '{secret}'
        );
        """
    
    cursor.execute(sql_query)

    conn.commit()

    cursor.close()

    # Redirect
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Establish Azure SQL connection
            conn = SQLConnection()
            conn = conn.getConnection()
            cursor = conn.cursor()

            # Query Azure SQL for user credentials
            sql_login = f"""
            SELECT *
            FROM FinalProject.Customer
            WHERE username = '{username}' AND password = '{password}';
            """

            cursor.execute(sql_login)
            result = cursor.fetchone()

            if result:
                # SUCCESS login
                cursor.close()
                flash('User added successfully!', 'success')
                return redirect(url_for('landing')) # Redirect to landing page
            else:
                cursor.close()
                return render_template('login.html', error='Invalid username or password') #Render login page with error message
            
        except Exception as e:
            # handle exceptions
            return render_template('login.html', error='An error occurred. Please try again later.')

    # If GET request, render the login page 
    return render_template('login.html')



# Driver function
if __name__ == '__main__':

	app.run(debug = True)