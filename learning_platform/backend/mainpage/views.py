from django.shortcuts import render
from courses.models import Course

# Create your views here.

def home(request):
    courses = Course.objects.prefetch_related('lessons').all()
    return render(request, 'home.html', {'courses': courses})
