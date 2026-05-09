from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from gtts import gTTS
import io
from .models import Course, Lesson
# Create your views here.

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

def speak_view(request):
    text = request.GET.get('text','')
    
    if not text:
        return HttpResponse("Brak tekstu do przeczytania", status = 400)
    
    tts = gTTS(text=text, lang='pl')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")