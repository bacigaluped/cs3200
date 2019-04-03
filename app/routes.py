from app import app
from requests import get
from flask import render_template, redirect, url_for
from webargs import fields
from webargs.flaskparser import use_kwargs
from json import dumps, encoder

api_headers={
    "X-RapidAPI-Key": "d79033f905mshb7d8af7cc775ed9p15d83ejsn0f48d10e2155"
}

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'ingredients.html',
        pantry_items=['Eggs'],
        shopping_list=['Eggs'],
        recipes=[{'id': 1234, 'title': 'Omelette', 'Link': '#link_to_omelette_recipe'}],
    )


@app.route('/add_to_shopping_list', methods=['POST'])
@use_kwargs({'ingredient': fields.Str()})
def add_to_shopping_list(ingredient):
    print(f'{ingredient} needs to be added to the shopping list')
    return redirect(url_for('index'))


@app.route('/add_to_pantry', methods=['POST'])
@use_kwargs({'ingredient': fields.Str()})
def add_to_pantry(ingredient):
    print(f'{ingredient} needs to be added to the pantry')
    return redirect(url_for('index'))


@app.route('/remove_from_shopping_list', methods=['POST'])
@use_kwargs({'list_item': fields.Str()})
def remove_from_shopping_list(list_item):
    print(f'{list_item} would be removed from the shopping list here')
    return redirect(url_for('index'))


@app.route('/remove_from_pantry', methods=['POST'])
@use_kwargs({'ingredient': fields.Str()})
def remove_from_pantry(ingredient):
    print(f'{ingredient} would be removed from the pantry here')
    return redirect(url_for('index'))


@app.route('/call_api', methods=['POST'])
@use_kwargs({'ingredients': fields.List(fields.Str())})
def call_api(ingredients):
    response = get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients",
        headers=api_headers,
        params={'ingredients': ingredients, 'number': 5, 'ranking': 1}
    )
    return '\n'.join([ f'{recipe["id"]} {recipe["title"]}\n' for recipe in response.json() ])
