import io
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from gtts import gTTS

from .ai_service import GeminiConfigurationError, generate_course_with_gemini
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


def ai_course_detail(request, course_id):
    generated_courses = request.session.get('generated_courses', [])
    course = next((item for item in generated_courses if item.get('id') == course_id), None)

    if course is None:
        return render(request, 'course_not_available.html', status=404)

    return render(request, 'ai_course_detail.html', {
        'course': course,
    })


@require_POST
def generate_ai_course(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Niepoprawny format żądania.',
        }, status=400)

    topic = payload.get('topic', '').strip()

    if not topic:
        return JsonResponse({
            'success': False,
            'error': 'Podaj temat kursu.',
        }, status=400)

    if len(topic) > 150:
        return JsonResponse({
            'success': False,
            'error': 'Temat kursu jest zbyt długi. Maksymalnie 150 znaków.',
        }, status=400)

    try:
        course = generate_course_with_gemini(topic)
    except GeminiConfigurationError as error:
        return JsonResponse({
            'success': False,
            'error': str(error),
        }, status=503)
    except Exception as error:
        return JsonResponse({
            'success': False,
            'error': f'Nie udało się wygenerować kursu: {error}',
        }, status=500)

    generated_courses = request.session.get('generated_courses', [])
    generated_courses.insert(0, course)
    request.session['generated_courses'] = generated_courses[:5]
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'course_id': course['id'],
        'title': course['title'],
    })

def speak_view(request):
    text = request.GET.get('text','')
    
    if not text:
        return HttpResponse("Brak tekstu do przeczytania", status = 400)
    
    tts = gTTS(text=text, lang='pl')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")
