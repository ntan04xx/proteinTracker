import requests
from django.shortcuts import render, redirect
from .forms import ApiRequestForm
from .forms import TargetRequestForm
from .models import ApiResponse
import datetime
import json

app_id = "61bf32f0"
app_key = "786cd82f86f149854c26c1b43178825c"

def home_page(request):
    return render(request, 'calorie_count/home.html')

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
                latest_date = latest_response.timestamp.date()
                current_date = datetime.datetime.now().date()

                if latest_date == current_date:
                    total_protein = latest_response.total_protein + protein
                    total_calories = latest_response.total_calories + calories
                    total_fat = latest_response.total_fat + fat
                else:
                    total_protein = protein
                    total_calories = calories
                    total_fat = fat
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

class UserProfile:
    def __init__(self, age, weight, height, gender, activity, goal):
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.activity = activity
        self.goal = goal

    def find_targets(self):
        if self.gender == 'M':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.33 * self.age)
        
        if self.activity == 'None':
            bmr *= 1.2
        elif self.activity == 'Low':
            bmr *= 1.375
        elif self.activity == 'Medium':
            bmr *= 1.55
        elif self.activity == 'High':
            bmr *= 1.725

        goal = self.goal.split(" ")
        style = goal[0]
        percent = float(goal[1])

        if style == 'Cut':
            calorie_target = bmr * (1 - percent)
            protein_target = calorie_target * 0.3 # based on https://www.bulk.com/uk/the-core/how-to-decide-your-own-macro-split/
            fat_target = calorie_target * 0.3
        elif style == 'Bulk':
            calorie_target = bmr * (1 + percent)
            protein_target = calorie_target * 0.25
            fat_target= calorie_target * 0.25
        
        return (calorie_target, protein_target, fat_target)

def get_target_strings(response, calorie_target, protein_target, fat_target):
    calorie_diff = abs(response.total_calories - calorie_target)
    calorie_msg = f"You have met today's calorie target by {calorie_diff}kJ" if response.total_calories else f"You still have {calorie_diff}kJ until you meet today's target."

    protein_diff = abs(response.total_protein - protein_target)
    protein_msg = f"You have met today's protein target by {protein_diff}kJ" if response.total_protein else f"You still have {protein_diff}kJ until you meet today's target."

    fat_diff = abs(response.total_fat - fat_target)
    fat_msg = f"You have met today's fat target by {fat_diff}kJ" if response.total_fat else f"You still have {fat_diff}kJ until you meet today's target."

    return (calorie_msg, protein_msg, fat_msg)

def target_request_view(request):
    if request.method == 'POST':
        form = TargetRequestForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            gender = form.cleaned_data['gender']
            activity = form.cleaned_data['activity']
            goal = form.cleaned_data['goal']
            user = UserProfile(age, weight, height, gender, activity, goal)
            calorie_target, protein_target, fat_target = user.find_targets()

            latest_response = ApiResponse.objects.latest('timestamp')
            calorie_msg, protein_msg, fat_msg = get_target_strings(latest_response, calorie_target, protein_target, fat_target)
            return render(request, 'calorie_count/target_response.html', {'calories': calorie_msg,
                                                                          'protein': protein_msg,
                                                                          'fat': fat_msg})
    else:
        form = TargetRequestForm()
    return render(request, 'calorie_count/target_request.html', {'form': form})
