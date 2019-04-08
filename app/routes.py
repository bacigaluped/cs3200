from app import app, database_password, api_key
from requests import get
from flask import render_template, redirect, url_for
from webargs import fields
from webargs.flaskparser import use_kwargs
from mysql import connector

cnx = connector.connect(
    user='root', password=database_password, host='localhost', database='meal_planner'
)
cursor = cnx.cursor()

api_headers={
    "X-RapidAPI-Key": api_key
}

pantry_id = 1
user_id = 1

@app.route('/')
@app.route('/index')
def index():

    cursor.execute(f'''select food_item
    from pantry_has_food_item
    join food_item on pantry_has_food_item.food_item_id=food_item.food_item_id
    where pantry_has_food_item.pantry_id={pantry_id};''')

    pantry_items = list()
    for row in cursor:
        pantry_items.append(row[0])

    cursor.execute(
        f'''select food_item, cost
        from user_shops_for_food_item
        join food_item on food_item.food_item_id=user_shops_for_food_item.food_item_id
        where user_id={user_id};'''
    )
    shopping_list = list()

    for row in cursor:
        item_name = row[0]
        # TODO add cost and other attributes maybe
        shopping_list.append(item_name)


    cursor.execute(
        f'''select recipe.recipe_id, title, recipe_url, photo_url
        from user_saved_recipe
        join recipe on recipe.recipe_id=user_saved_recipe.recipe_id
        where user_id={user_id};'''
    )

    recipes = list()
    for row in cursor:
        recipes.append(
            {
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'photo_link': row[3]
            }
        )


    return render_template(
        'ingredients.html',
        pantry_items=pantry_items,
        shopping_list=shopping_list,
        recipes=[{'id': 1234, 'title': 'Omelette', 'link': '#link_to_omelette_recipe'}]
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
