from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course,
    }
    return render(request, 'course_detail.html', context)

def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    context = {
        'course': course,
        'lesson': lesson,
    }
    return render(request, 'lesson_detail.html', context)
