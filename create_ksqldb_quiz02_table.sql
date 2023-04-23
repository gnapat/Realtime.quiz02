CREATE STREAM quiz02_raw (
index int,
GPA varchar,
Gender int,
breakfast int,
calories_chicken int,
calories_day double,
calories_scone double,
coffee int,
comfort_food varchar,
comfort_food_reasons varchar,
comfort_food_reasons_coded double,
cook double,
comfort_food_reasons_coded_1 int,
cuisine double,
diet_current varchar,
diet_current_coded int,
drink double,
eating_changes varchar,
eating_changes_coded int,
eating_changes_coded1 int,
eating_out int,
employment double,
ethnic_food int,
exercise double,
father_education double,
father_profession varchar,
fav_cuisine varchar,
fav_cuisine_coded int,
fav_food double,
food_childhood varchar,
fries int,
fruit_day int,
grade_level int,
greek_food int,
healthy_feeling int,
healthy_meal varchar,
ideal_diet varchar,
ideal_diet_coded int,
income double,
indian_food int,
italian_food int,
life_rewarding double,
marital_status double,
meals_dinner_friend varchar,
mother_education double,
mother_profession varchar,
nutritional_check int,
on_off_campus double,
parents_cook int,
pay_meal_out int,
persian_food double,
self_perception_weight double,
soup double,
sports double,
thai_food int,
tortilla_calories double,
turkey_calories int,
type_sports varchar,
veggies_day int,
vitamins int,
waffle_calories int,
weight varchar )  WITH (KAFKA_TOPIC='quiz02_raw',VALUE_FORMAT='AVRO');