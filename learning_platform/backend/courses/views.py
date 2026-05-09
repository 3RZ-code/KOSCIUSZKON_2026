from django.shortcuts import render

# Create your views here.

def course_detail(request, course_id):
    return render(request, 'course_detail.html', {'course_id': course_id})