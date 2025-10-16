# app.py
from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# ---------------- Ingredients & Recipes ----------------
# Sample dataset (can be extended or loaded from CSV)
recipes = {
    "Chicken Rice": {"rice": 200, "chicken": 150},
    "Cheese Omelette": {"egg": 100, "cheese": 50},
    "Tomato Soup": {"tomato": 200, "milk": 100},
    "Egg Sandwich": {"egg": 50, "bread": 100, "cheese": 20}
}

all_ingredients = ["rice", "chicken", "tomato", "cheese", "egg", "milk", "bread"]

# Calories per 100g
ingredients_cal = {
    "rice": 130, "chicken": 239, "tomato": 18,
    "cheese": 402, "egg": 155, "milk": 42, "bread": 265
}

# ---------------- ML Setup ----------------
# Prepare recipe vectors for cosine similarity
recipe_vectors = []
recipe_names = list(recipes.keys())
for rec in recipes.values():
    vec = [1 if ing in rec else 0 for ing in all_ingredients]
    recipe_vectors.append(vec)
recipe_vectors = np.array(recipe_vectors)

# Prepare regression model for calorie prediction
# Convert recipes to quantities as features
data = pd.DataFrame()
for rec_name, rec in recipes.items():
    row = {ing: rec.get(ing,0) for ing in all_ingredients}
    row["calories"] = sum([rec.get(ing,0)*ingredients_cal[ing]/100 for ing in rec])
    data = pd.concat([data,pd.DataFrame([row])], ignore_index=True)

X = data[all_ingredients]
y = data["calories"]
cal_model = LinearRegression()
cal_model.fit(X, y)

# ---------------- Routes ----------------
@app.route("/", methods=["GET","POST"])
def index():
    result = ""
    calories = ""
    shopping_list = ""
    if request.method == "POST":
        action = request.form.get("action")

        # --- Calculate Calories ---
        if action == "calc_calories":
            recipe_input = request.form.get("recipe_input")
            total = 0
            for line in recipe_input.strip().split("\n"):
                try:
                    item, qty = line.split(",")
                    item = item.strip()
                    qty = float(qty.strip())
                    total += ingredients_cal[item]*qty/100
                except:
                    total = "Error! Format: ingredient, quantity_in_grams"
            calories = f"{total:.2f} kcal" if isinstance(total,float) else total

        # --- Compare Ingredients ---
        elif action == "compare":
            ing1 = request.form.get("ing1").strip()
            ing2 = request.form.get("ing2").strip()
            if ing1 in ingredients_cal and ing2 in ingredients_cal:
                if ingredients_cal[ing1] > ingredients_cal[ing2]:
                    result = f"{ing1} has more calories than {ing2}"
                elif ingredients_cal[ing1] < ingredients_cal[ing2]:
                    result = f"{ing2} has more calories than {ing1}"
                else:
                    result = f"{ing1} and {ing2} have equal calories"
            else:
                result = "Ingredient not found!"

        # --- Shopping List ---
        elif action == "shopping":
            recipes_text = request.form.get("shopping_input")
            shopping = {}
            recipes_list = recipes_text.strip().split("\n\n")
            try:
                for rec in recipes_list:
                    for line in rec.split("\n"):
                        item, qty = line.split(",")
                        item = item.strip()
                        qty = float(qty.strip())
                        shopping[item] = shopping.get(item,0)+qty
                shopping_list = "\n".join([f"{i}: {q}g" for i,q in shopping.items()])
            except:
                shopping_list = "Error! Format: ingredient, quantity_in_grams"

        # --- Suggest Recipe ---
        elif action == "suggest":
            available_input = request.form.get("available")
            available = set([x.strip() for x in available_input.split(",")])
            suggested = []
            for idx, rec_name in enumerate(recipe_names):
                rec_vec = recipe_vectors[idx].reshape(1,-1)
                user_vec = np.array([[1 if ing in available else 0 for ing in all_ingredients]])
                sim = cosine_similarity(user_vec, rec_vec)[0][0]
                if sim > 0:
                    suggested.append(f"{rec_name} (Similarity: {sim:.2f})")
            result = "\n".join(suggested) if suggested else "No matching recipes"

    return render_template("index.html", result=result, calories=calories, shopping_list=shopping_list)

if __name__ == "__main__":
    app.run(debug=True)
