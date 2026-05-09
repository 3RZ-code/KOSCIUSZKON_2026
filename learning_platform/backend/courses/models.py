from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    estimated_time = models.IntegerField(help_text="Czas ukończenia w minutach")
    level = models.CharField(max_length=50, default="Poziom 1")

    is_ai_generated = models.BooleanField(default=False)
    session_key = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title