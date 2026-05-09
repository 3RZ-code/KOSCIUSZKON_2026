from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł kursu")
    description = models.TextField(verbose_name="Opis")
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Tytuł lekcji")
    category = models.CharField(max_length=100, verbose_name="Kategoria", blank=True)
    expected_time = models.IntegerField(help_text="Przewidywany czas (w minutach)", verbose_name="Czas ukończenia")
    short_description = models.TextField(verbose_name="Krótki opis (zajawka)", blank=True, null=True)
    content = models.TextField(verbose_name="Główna, pełna treść lekcji")
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.expected_time} min)"

