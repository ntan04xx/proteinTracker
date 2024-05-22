from django import forms

class ApiRequestForm(forms.Form):
    input_data = forms.CharField(widget = forms.Textarea, label = "Input Data")