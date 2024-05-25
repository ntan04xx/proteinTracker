from django import forms

class ApiRequestForm(forms.Form):
    input_food = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "f")
    input_amount = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")