from django.db import models

# Create your models here.
class ApiResponse(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()
    total_protein = models.IntegerField(default = 0)
    total_calories = models.IntegerField(default = 0)
    total_fat = models.IntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)