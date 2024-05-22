import requests
from django.shortcuts import render, redirect
from .forms import ApiRequestForm
from .models import ApiResponse

app_id = "61bf32f0"
app_key = "786cd82f86f149854c26c1b43178825c"

def call_api(input_data):
    url = 'https://api.edamam.com/api/nutrition-details'
    params = {'app_id': app_id, 'app_key': app_key}
    payload = {'ingr': [f"{input_data}"]}
    response = requests.post(url, params=params, json=payload)
    return response.json()

def api_request_view(request):
    if request.method == 'POST':
        form = ApiRequestForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['input_data']
            api_response = call_api(input_data)
            # Store the data
            ApiResponse.objects.create(input_data=input_data, output_data=api_response)
            # Redirect to a new URL with the output displayed
            return render(request, 'calorie_count/api_response.html', {'input_data': input_data, 'output_data': api_response})
    else:
        form = ApiRequestForm()
    return render(request, 'calorie_count/api_request.html', {'form': form})
