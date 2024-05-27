import requests
from django.shortcuts import render, redirect
from .forms import ApiRequestForm
from .models import ApiResponse
import json

app_id = "61bf32f0"
app_key = "786cd82f86f149854c26c1b43178825c"

def value_error_view(request, exception):
    return render(request, 'calorie_count/value_error.html', {'message': str(exception)})

def call_api(input_food, input_amount):
    url = 'https://api.edamam.com/api/nutrition-details'
    params = {'app_id': app_id, 'app_key': app_key}
    payload = {'ingr': [f"{input_food} {input_amount}"]}
    response = requests.post(url, params=params, json=payload)
    if response.status_code == 200:
        result = response.json()
    else:
        raise ValueError("Not found")

    food_nutrients = result.get("totalNutrients")
    protein = food_nutrients.get("PROCNT").get("quantity")
    fat = food_nutrients.get("FAT").get("quantity")
    calories = food_nutrients.get("ENERC_KCAL").get("quantity")

    macros = {
        'Calories (kcal)': calories,
        'Fat (g)': fat,
        'Protein (g)': protein
    }

    return calories, fat, protein, json.dumps(macros)

def api_request_view(request):
    if request.method == 'POST':
        form = ApiRequestForm(request.POST)
        if form.is_valid():
            input_food = form.cleaned_data['input_food']
            input_amount = form.cleaned_data['input_amount']
            calories, fat, protein, api_response = call_api(input_food, input_amount)
            # Store the data
            try:
                latest_response = ApiResponse.objects.latest('timestamp')
                total_protein = latest_response.total_protein + protein
                total_calories = latest_response.total_calories + calories
                total_fat = latest_response.total_fat + fat
            except ApiResponse.DoesNotExist:
                total_protein = protein
                total_calories = calories
                total_fat = fat
            ApiResponse.objects.create(input_data=f"Food: {input_food}, Amount: {input_amount}", 
                                       output_data=api_response,
                                       total_protein=total_protein,
                                       total_calories=total_calories,
                                       total_fat=total_fat)

            # Redirect to a new URL with the output displayed
            total_nutrients = {'Calories (kcal)': total_calories, 'Fat (g)': total_fat, 'Protein (g)': total_protein}
            return render(request, 'calorie_count/api_response.html', {'input_food': input_food, 
                                                                       'input_amount': input_amount, 
                                                                       'nutrition_data': api_response,
                                                                       'totals_data': total_nutrients})
    else:
        form = ApiRequestForm()
    return render(request, 'calorie_count/api_request.html', {'form': form})
