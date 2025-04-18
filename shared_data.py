# ----------------------------
    # Shared Data + Setup
    # ----------------------------
meals = {
"Breakfast": [
    "Eggs Benedict, Orange",
    "Oatmeal with Berries",
    "Scrambled Eggs and Toast",
    "Greek Yogurt Parfait",
    "Pancakes with Banana"
],
"Lunch": [
    "Tuna Salad, Brussel Sprouts",
    "Chicken Fajitas",
    "Turkey Sandwich",
    "Grilled Chicken and Salad",
    "Tofu Stir-Fry",
    "Bone Broth Soup"
],
"Dinner": [
    "Shrimp Linguine and Jello",
    "Japanese Curry",
    "Baked Salmon with Quinoa",
    "Spaghetti and Meatballs",
    "Vegetable Stir-Fry"
]
}

meal_nutrition = {
"Eggs Benedict, Orange": {
    "Calories": 400,
    "Protein": "18g",
    "Total Fat": "25g",
    "Carbs": "25g",
    "Image": "https://www.allrecipes.com/thmb/QVMaPhXnj1HQ70C7Ka9WYtuipHg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/17205-eggs-benedict-DDMFS-4x3-a0042d5ae1da485fac3f468654187db0.jpg"
},
"Oatmeal with Berries": {
    "Calories": 300,
    "Protein": "6g",
    "Total Fat": "4g",
    "Carbs": "50g",
    "Image": "https://media.post.rvohealth.io/wp-content/uploads/2024/06/oatmeal-bowl-blueberries-strawberries-breakfast-732x549-thumbnail.jpg"
},
"Scrambled Eggs and Toast": {
    "Calories": 350,
    "Protein": "15g",
    "Total Fat": "20g",
    "Carbs": "30g",
    "Image": "https://whereismyspoon.co/wp-content/uploads/2019/07/scrambled-eggs-on-toast-1.jpg"
},
"Greek Yogurt Parfait": {
    "Calories": 180,
    "Protein": "12g",
    "Sugar": "10g",
    "Fat": "3g",
    "Image": "https://i1.wp.com/www.kiwiandcarrot.com/wp-content/uploads/2018/01/BLOG-4-4.jpg?fit=680%2C958&ssl=1"
},
"Pancakes with Banana": {
    "Calories": 350,
    "Protein": "9g",
    "Carbs": "60g",
    "Total Fat": "7g",
    "Image": "https://www.allrecipes.com/thmb/6x0Lw9L4MEU8INHnK4tXGRV9XWI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20334-banana-pancakes-i-DDMFS-4x3-9f291f03044247d48c9ec26917952402.jpg"
},
"Tuna Salad, Brussel Sprouts": {
    "Calories": 450,
    "Protein": "30g",
    "Total Fat": "22g",
    "Carbs": "20g",
    "Image": "https://starkist.com/wp-content/uploads/2019/09/recipes_lemon_tuna_shaved_brussel_sprout_salad_910x445.jpg"
},
"Chicken Fajitas": {
    "Calories": 500,
    "Protein": "30g",
    "Total Fat": "4g",
    "Carbs": "10g",
    "Image": "https://www.everydayfamilycooking.com/wp-content/uploads/2022/03/chicken-fajita-wrap11.jpg"
},
"Turkey Sandwich": {
    "Calories": 420,
    "Protein": "26g",
    "Carbs": "40g",
    "Total Fat": "15g",
    "Image": "https://www.eatingonadime.com/wp-content/uploads/2022/03/eod-turkey-sandwich-5-2.jpg"
},
"Grilled Chicken and Salad": {
    "Calories": 380,
    "Protein": "35g",
    "Total Fat": "10g",
    "Carbs": "15g",
    "Image": "https://www.eatingbirdfood.com/wp-content/uploads/2023/06/grilled-chicken-salad-hero.jpg"
},
"Tofu Stir-Fry": {
    "Calories": 350,
    "Protein": "18g",
    "Carbs": "30g",
    "Fat": "15g",
    "Image": "https://www.wellplated.com/wp-content/uploads/2022/03/Tofu-Broccoli-Stir-Fry-Recipe.jpg"
},
"Bone Broth Soup": {
    "Calories": 200,
    "Protein": "14g",
    "Fat": "5g",
    "Carbs": "10g",
    "Image": "https://freshwaterpeaches.com/wp-content/uploads/2022/01/Chicken-Bone-Broth-Soup-6.jpg"
},
"Shrimp Linguine and Jello": {
    "Calories": 600,
    "Protein": "25g",
    "Carbs": "50g",
    "Fat": "20g",
    "Image": "https://www.melskitchencafe.com/wp-content/uploads/2023/02/creamy-garlic-shrimp-pasta12-640x878.jpg"
},
"Japanese Curry": {
    "Calories": 550,
    "Protein": "22g",
    "Carbs": "60g",
    "Fat": "18g",
    "Image": "https://sudachirecipes.com/wp-content/uploads/2022/08/Japanese-curry-using-roux-thumbnail.jpg"
},
"Baked Salmon with Quinoa": {
    "Calories": 520,
    "Protein": "35g",
    "Fat": "25g",
    "Carbs": "30g",
    "Image": "https://www.jessicagavin.com/wp-content/uploads/2016/02/mediterranean-spiced-salmon-over-vegetable-quinoa-1200.jpg"
},
"Spaghetti and Meatballs": {
    "Calories": 640,
    "Protein": "30g",
    "Fat": "28g",
    "Carbs": "60g",
    "Image": "https://embed.widencdn.net/img/beef/lkfopyh4v0/1120x630px/classic%20spaghetti%20&%20meatballs%2002.tif?keep=c&u=nvwl20"
},
"Vegetable Stir-Fry": {
    "Calories": 320,
    "Protein": "10g",
    "Fat": "12g",
    "Carbs": "40g",
    "Image": "https://www.dinneratthezoo.com/wp-content/uploads/2019/02/vegetable-stir-fry-3.jpg"
}
}

gluten_meals = [
"Pancakes with Banana",
"Spaghetti and Meatballs",
"Scrambled Eggs and Toast"
]

status_colors = {
"Scheduled": "gray",
"Past": "gray",
"Completed": "green",
"Skipped": "red"
}
meal_allergens = {
"Pancakes with Banana": ["Gluten", "Eggs"],
"Spaghetti and Meatballs": ["Gluten"],
"Scrambled Eggs and Toast": ["Gluten", "Eggs"],
"Tuna Salad, Brussel Sprouts": ["Eggs"],
"Bone Broth Soup": ["Shellfish"],
"Greek Yogurt Parfait": ["Dairy"],
# Add more mappings as needed
}