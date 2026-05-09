from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Pobranie ewentualnie wybranej lekcji (domyślnie pierwsza)
    lesson_id = request.GET.get('lekcja')
    if lesson_id:
        active_lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    else:
        active_lesson = course.lessons.first()

    context = {
        'course': course,
        'active_lesson': active_lesson,
    }
    return render(request, 'course_detail.html', context)