use meal_planner;

select food_item
from pantry_has_food_item
join food_item on pantry_has_food_item.food_item_id=food_item.food_item_id
where pantry_id=1;

SELECT 
    food_item, cost
FROM
    user_shops_for_food_item
        JOIN
    food_item ON food_item.food_item_id = user_shops_for_food_item.food_item_id
WHERE
    user_id = 1;


select recipe.recipe_id, title, recipe_url, photo_url
from user_saved_recipe
join recipe on recipe.recipe_id=user_saved_recipe.recipe_id
where user_id=1;


insert into food_item (food_item, photo_url)
values ('Eggs', 'https://c.o0bg.com/rf/image_371w/Boston/2011-2020/2017/09/27/BostonGlobe.com/Magazine/Images/tip1008cooking.jpg');


insert into pantry (pantry_name) values ('Example Pantry');

insert into user (username, password, pantry_id)
values ('Person', 'thisisapassword', 1);

insert into pantry_has_food_item (pantry_id, food_item_id)
values (1,1);

insert into user_shops_for_food_item (user_id, food_item_id)
values (1,1);

select * from recipe;

insert into recipe (title, recipe_url, photo_url)
values ('Omelette', 'https://www.incredibleegg.org/recipe/basic-french-omelet/', 'https://x9wsr1khhgk5pxnq1f1r8kye-wpengine.netdna-ssl.com/wp-content/uploads/basic-french-omelet-930x550.jpg');

insert into user_saved_recipe (user_id, recipe_id)
values (1,1);

delete from user_shops_for_food_item where user_id=1 and food_item_id=1;
