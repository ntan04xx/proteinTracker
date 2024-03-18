import requests

# Parameters for requests to Nutrition Analysis API
app_id = "61bf32f0"
app_key = "786cd82f86f149854c26c1b43178825c"

url = 'https://api.edamam.com/api/nutrition-details'
params = {
    'app_id': app_id,
    'app_key': app_key
}

class Food:
    # Note that each macro would be passed in as tuple of amount
    def __init__(self, name, protein, fat, calories):
        self.name = name
        self.protein = protein # in grams
        self.fat = fat # in grams
        self.calories = calories # in kcal

# Function that returns object of class Food when given string
def get_macros(food_size, food_name):
    data = {
        'ingr': [f"{food_size} {food_name}"]
    }

    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
    else:
        raise ValueError("Food not found")
    
    food_nutrients = result.get("totalNutrients")
    protein = food_nutrients.get("PROCNT").get("quantity")
    fat = food_nutrients.get("FAT").get("quantity")
    calories = food_nutrients.get("ENERC_KCAL").get("quantity")

    return Food(food_name, protein, fat, calories)