DROP DATABASE IF EXISTS meal_planner;
CREATE DATABASE meal_planner;
USE meal_planner;


-- PANTRY
DROP TABLE IF EXISTS pantry;
CREATE TABLE pantry (
	pantry_id int PRIMARY KEY AUTO_INCREMENT,
    pantry_name varchar(64) UNIQUE NOT NULL);


-- USER
DROP TABLE IF EXISTS user;
CREATE TABLE user (
	user_id int PRIMARY KEY AUTO_INCREMENT,
	username varchar(16) NOT NULL,
    email varchar(255) NULL,
    password varchar(32) NOT NULL,
    pantry_id int NOT NULL,
    CONSTRAINT fk_user_pantry FOREIGN KEY (pantry_id) REFERENCES pantry (pantry_id));



-- RECIPE
DROP TABLE IF EXISTS recipe;
CREATE TABLE recipe (
	recipe_id int PRIMARY KEY,
    title varchar(128) NOT NULL,
    recipe_url varchar(255) NOT NULL,
    photo_url varchar(255) NOT NULL);


-- USER_SAVED_RECIPE
DROP TABLE IF EXISTS user_saved_recipe;
CREATE TABLE user_saved_recipe (
	user_id int NOT NULL,
    recipe_id int NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_user_recipe FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id));


-- FOOD_ITEM
DROP TABLE IF EXISTS food_item;
CREATE TABLE food_item (
	food_item_id int PRIMARY KEY AUTO_INCREMENT,
    food_item varchar(45) NOT NULL UNIQUE,
    photo_url varchar(255),
    cost varchar(20) DEFAULT NULL);


-- RECIPE_USES_FOOD_ITME
DROP TABLE IF EXISTS recipe_uses_food_item;
CREATE TABLE recipe_uses_food_item (
	recipe_id int NOT NULL,
    food_item_id int NOT NULL,
    quantity varchar(25) DEFAULT NULL,
    CONSTRAINT fk_recipe FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id),
    CONSTRAINT fk_food_item FOREIGN KEY (food_item_id) REFERENCES food_item (food_item_id));



-- PANTRY_HAS_FOOD_ITEM
DROP TABLE IF EXISTS pantry_has_food_item;
CREATE TABLE pantry_has_food_item (
	pantry_id int NOT NULL,
    food_item_id int NOT NULL,
    CONSTRAINT fk_pantry_food FOREIGN KEY (pantry_id) REFERENCES pantry (pantry_id),
    CONSTRAINT fk_food_item_pantry FOREIGN KEY (food_item_id) REFERENCES food_item (food_item_id));



-- USER_SHOPS_FOR_FOOD_ITEM
DROP TABLE IF EXISTS user_shops_for_food_item;
CREATE TABLE user_shops_for_food_item (
	user_id int NOT NULL,
    food_item_id int NOT NULL,
    CONSTRAINT fk_user_shops FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_user_food FOREIGN KEY (food_item_id) REFERENCES food_item (food_item_id));


-- DIETARY_RESTRICTION
DROP TABLE IF EXISTS dietary_restriction;
CREATE TABLE dietary_restriction (
	dietary_restriction_id int PRIMARY KEY AUTO_INCREMENT,
    restriction varchar(45) NOT NULL);



-- USER_HAS_DIETARY_RESTRICTION
DROP TABLE IF EXISTS user_has_dietary_restriction;
CREATE TABLE user_has_dietary_restriction (
	user_id int NOT NULL,
    dietary_restriction_id int NOT NULL,
    CONSTRAINT fk_user_restriction FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_dietary_restriction FOREIGN KEY (dietary_restriction_id) REFERENCES dietary_restriction (dietary_restriction_id));
