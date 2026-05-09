from django.db import models

# Create your models here.

class course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    predicted_time = models.IntegerField() # in minutes 
    pub_date = models.DateTimeField(auto_now_add=True)
    directory = models.CharField(max_length=255)