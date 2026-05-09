from django.db import models

# Create your models here.

class course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=100)
    description = models.TextField()
    predicted_time = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)