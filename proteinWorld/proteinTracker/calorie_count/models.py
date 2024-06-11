from django.db import models

# Create your models here.
class ApiResponse(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()
    total_protein = models.IntegerField(default = 0)
    total_calories = models.IntegerField(default = 0)
    total_fat = models.IntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserDetails(models.Model):
    username = models.TextField()
    age = models.IntegerField(default = 21)
    weight = models.FloatField(default = 69.5)
    height = models.FloatField(default = 185)
    gender = models.CharField(max_length = 1)
    activity = models.TextField()
    goal = models.TextField()
    calorie_target = models.FloatField(default=0)
    protein_target = models.FloatField(default=0)
    fat_target = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

