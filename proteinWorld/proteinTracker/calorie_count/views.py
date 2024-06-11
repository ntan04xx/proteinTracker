import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ApiRequestForm, SignUpForm, TargetRequestForm
from .models import ApiResponse, UserDetails
from .user import UserProfile
import datetime
import json
import re

app_id = "61bf32f0"
app_key = "786cd82f86f149854c26c1b43178825c"

def home_page(request):
    return render(request, 'calorie_count/home.html')

@login_required
def main_page(request):
    return render(request, 'calorie_count/main.html')

def call_api(input_food, input_amount):
    url = 'https://api.edamam.com/api/nutrition-details'
    params = {'app_id': app_id, 'app_key': app_key}
    payload = {'ingr': [f"{input_food} {input_amount}"]}
    response = requests.post(url, params=params, json=payload)
    if response.status_code == 200:
        result = response.json()
    else:
        return redirect('value_error')

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

@login_required
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

def get_target_strings(response, calorie_target, protein_target, fat_target):
    calorie_diff = abs(response.total_calories - calorie_target)
    calorie_msg = f"You have met today's calorie target by {calorie_diff}kJ" if response.total_calories else f"You still have {calorie_diff}kJ until you meet today's target."

    protein_diff = abs(response.total_protein - protein_target)
    protein_msg = f"You have met today's protein target by {protein_diff}kJ" if response.total_protein else f"You still have {protein_diff}kJ until you meet today's target."

    fat_diff = abs(response.total_fat - fat_target)
    fat_msg = f"You have met today's fat target by {fat_diff}kJ" if response.total_fat else f"You still have {fat_diff}kJ until you meet today's target."

    return (calorie_msg, protein_msg, fat_msg)

def is_password_strong(password):
    min_length = 8
    if re.search("\d", password) == None or re.search("[~`!@#$%^&*()-_+={}[]|\;:\"<>,./?]", password) == None or len(password) < min_length:
        return False
    return True

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if UserDetails.objects.filter(username = username).exists():
                return redirect('used_username')
            password = form.cleaned_data['password']
            if is_password_strong(password) == False:
                return redirect('weak_password')

            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            gender = form.cleaned_data['gender']
            activity = form.cleaned_data['activity']
            goal = form.cleaned_data['goal']

            userProfile = UserProfile(age, weight, height, gender, activity, goal)
            calorie_target, protein_target, fat_target = userProfile.find_targets()

            User.objects.create_user(username = username, password = password)
            UserDetails.objects.create(
                                    username=username,
                                    age=age,
                                    weight=weight,
                                    height=height,
                                    gender=gender,
                                    activity=activity,
                                    goal=goal,
                                    calorie_target=calorie_target,
                                    protein_target=protein_target,
                                    fat_target=fat_target)
            user = authenticate(username = username, password = password)
            if user is not None:
                login(user)
                return redirect('main')
        else:
            form = SignUpForm()
    return render(request, 'calorie_count/sign_up.html', {'form': form})

@login_required
def target_request_view(request):
    if request.method == 'POST':
        form = TargetRequestForm(request.POST)
        if form.is_valid():
            username = request.cleaned_data['username']
            user_object = UserDetails.objects.filter(username = username).exists()
            calorie_target, protein_target, fat_target = user_object.calorie_target, user_object.protein_target, user_object.fat_target
            latest_response = ApiResponse.objects.latest('timestamp')
            calorie_msg, protein_msg, fat_msg = get_target_strings(latest_response, calorie_target, protein_target, fat_target)
            return render(request, 'calorie_count/target_response.html', {'calories': calorie_msg,
                                                                            'protein': protein_msg,
                                                                            'fat': fat_msg})
        else:
            form = TargetRequestForm()
    return render(request, 'calorie_count/target_request.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = request.cleaned_data['username']
            password = request.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(user)
                return redirect('main')
            else:
                return redirect('wrong_login')
    else:
        form = AuthenticationForm()
    return render(request, 'calorie_count/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'calorie_count/logout.html')
