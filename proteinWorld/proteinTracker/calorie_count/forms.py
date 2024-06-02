from django import forms

class ApiRequestForm(forms.Form):
    input_food = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    input_amount = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")

class TargetRequestForm(forms.Form):
    age = forms.IntegerField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    height = forms.FloatField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")
    weight = forms.FloatField(widget = forms.Textarea(attrs = {'placeholder': 'Enter Data Here '}), label = "")

    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = forms.ChoiceField(choice = GENDER, widget = forms.RadioSelect)

    ACTIVITY = [
        ('None', '0 times per week'),
        ('Low', '1-2 times per week'),
        ('Medium', '3-4 times per week'),
        ('High', '>5 times per week')
    ]
    activity = forms.ChoiceField(choice = ACTIVITY, widget = forms.RadioSelect)

    GOAL = [
        ('Cut', 0.1)
        ('Cut', 0.2),
        ('Bulk', 0.1),
        ('Bulk', 0.2)
    ]
    goal = forms.ChoiceField(choice = GOAL, widget = forms.RadioSelect)