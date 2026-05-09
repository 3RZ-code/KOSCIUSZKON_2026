from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from courses.models import Course

# Create your views here.

@ensure_csrf_cookie
def home(request):
    courses = Course.objects.prefetch_related('lessons').all()
    generated_courses = request.session.get('generated_courses', [])

    return render(request, 'home.html', {
        'courses': courses,
        'generated_courses': generated_courses,
    })
