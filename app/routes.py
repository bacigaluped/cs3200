from app import app
from requests import get
from flask import render_template
from webargs import fields
from webargs.flaskparser import use_kwargs
from json import dumps

api_headers={
    "X-RapidAPI-Key": "d79033f905mshb7d8af7cc775ed9p15d83ejsn0f48d10e2155"
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('ingredients.html')


@app.route('/call_api', methods=['POST'])
@use_kwargs({'ingredients': fields.List(fields.Str())})
def call_api(ingredients):
    response = get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients",
        headers=api_headers,
        params={'ingredients': ingredients, 'number': 5, 'ranking': 1}
    )
    return dumps(response.json())
