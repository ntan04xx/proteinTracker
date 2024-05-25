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

    return json.dumps(macros)

def api_request_view(request):
    if request.method == 'POST':
        form = ApiRequestForm(request.POST)
        if form.is_valid():
            input_food = form.cleaned_data['input_food']
            input_amount = form.cleaned_data['input_amount']
            api_response = call_api(input_food, input_amount)
            # Store the data
            ApiResponse.objects.create(input_data=f"Food: {input_food}, Amount: {input_amount}", output_data=api_response)
            # Redirect to a new URL with the output displayed
            return render(request, 'calorie_count/api_response.html', {'input_food': input_food, 'input_amount': input_amount, 'output_data': api_response})
    else:
        form = ApiRequestForm()
    return render(request, 'calorie_count/api_request.html', {'form': form})
