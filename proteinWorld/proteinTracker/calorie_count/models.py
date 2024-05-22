from django.db import models

# Create your models here.
class ApiResponse(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)