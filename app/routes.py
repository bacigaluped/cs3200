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

def image_url(image_extension):
    return f'https://spoonacular.com/cdn/ingredients_100x100/{image_extension}'

def get_food_image(food_item):
    response = get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/autocomplete",
        headers=api_headers,
        params={'query': food_item, 'number': 1}
    )

    if response.json():
        extention = response.json()[0]['image']
        return image_url(extention)
    else:
        return None


pantry_id = 1
user_id = 1

@app.route('/')
@app.route('/index')
def index():

    cursor.execute(
        f'''select food_item
        from pantry_has_food_item
        join food_item on pantry_has_food_item.food_item_id=food_item.food_item_id
        where pantry_has_food_item.pantry_id={pantry_id};'''
    )

    pantry_items = list()
    for row in cursor:
        pantry_items.append(row[0])

    cursor.execute(
        f'''select food_item.food_item_id, food_item, cost
        from user_shops_for_food_item
        join food_item on food_item.food_item_id=user_shops_for_food_item.food_item_id
        where user_id={user_id};'''
    )
    shopping_list = list()

    for row in cursor:

        # TODO add cost and other attributes maybe
        shopping_list.append(
            {
                'food_item_id': row[0],
                'food_item': row[1],
                'cost': row[2]
            }
        )

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
        recipes=recipes
        # recipes=[{'id': 1234, 'title': 'Omelette', 'link': '#link_to_omelette_recipe'}]
    )


@app.route('/add_to_shopping_list', methods=['POST'])
@use_kwargs({'ingredient': fields.Str(), 'ingredient_id': fields.Int()})
def add_to_shopping_list(ingredient, ingredient_id):
    print(f'{ingredient} needs to be added to the shopping list')

    return redirect(url_for('index'))


@app.route('/add_to_pantry', methods=['POST'])
@use_kwargs({'ingredient': fields.Str(), 'ingredient_id': fields.Int()})
def add_to_pantry(ingredient, ingredient_id):
    # print(f'{ingredient} needs to be added to the pantry')
    while ingredient_id < 0:
        cursor.execute(f'''select food_item_id from food_item where food_item="{ingredient}";''')

        existing_ingredient_list = list(cursor)

        if not existing_ingredient_list:
            photo_url = get_food_image(ingredient)
            if photo_url:
                cursor.execute(f'''insert into food_item (food_item, photo_url) values ("{ingredient}", "{photo_url}");''')
            else:
                cursor.execute(f'''insert into food_item (food_item) values ("{ingredient}");''')

            cnx.commit()

            from IPython import embed
            embed()
        else:
            for row in existing_ingredient_list:
                ingredient_id = row[0]

    cursor.execute(
        f'''select * from pantry_has_food_item where pantry_id={pantry_id} and food_item_id={ingredient_id};'''
    )

    if not list(cursor):
        cursor.execute(
            f'''insert into pantry_has_food_item (pantry_id, food_item_id) values ({pantry_id}, {ingredient_id});'''
        )

        cnx.commit()

    return redirect(url_for('index'))


@app.route('/remove_from_shopping_list', methods=['POST'])
@use_kwargs({'list_item_id': fields.Int()})
def remove_from_shopping_list(list_item_id):
    # print(f'{list_item} would be removed from the shopping list here')
    cursor.execute(
        f'''delete from user_shops_for_food_item where user_id={user_id} and food_item_id={list_item_id};'''
    )
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
