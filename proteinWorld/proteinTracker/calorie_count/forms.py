from django import forms
from django.contrib.auth.models import User

class ApiRequestForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    input_food = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    input_amount = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    age = forms.IntegerField(widget = forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    height = forms.FloatField(widget = forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    weight = forms.FloatField(widget = forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")

    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = forms.ChoiceField(choices = GENDER, widget = forms.RadioSelect)

    ACTIVITY = [
        ('None', '0 times per week'),
        ('Low', '1-2 times per week'),
        ('Medium', '3-4 times per week'),
        ('High', '>5 times per week')
    ]
    activity = forms.ChoiceField(choices = ACTIVITY, widget = forms.RadioSelect)

    GOAL = [
        ('Cut 0.2', 'Heavy Cut'),
        ('Cut 0.1', 'Light Cut'),
        ('Bulk 0.1', 'Light Bulk'),
        ('Bulk 0.2', 'Heavy Bulk')
    ]
    goal = forms.ChoiceField(choices = GOAL, widget = forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username','password')

class TargetRequestForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), label = "")

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs = {'placeholder': 'Enter Data Here '}), 
        label = ""
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs = {'placeholder': 'Enter Data Here '}), 
        label = ""
    )
