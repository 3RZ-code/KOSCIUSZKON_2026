import io
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from gtts import gTTS
from bs4 import BeautifulSoup

from .ai_service import GeminiConfigurationError, generate_course_with_gemini, generate_assessment_questions, evaluate_assessment
from .models import Course, Lesson, CourseAssessment
# Create your views here.

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lesson_summaries = []
    for lesson in course.lessons.all():
        lesson_text = f"Lekcja: {lesson.title}. {lesson.short_description or ''}."
        if lesson.content:
            lesson_text += f" {lesson.content[:300]}"
        lesson_summaries.append(lesson_text)

    course_content = f"{course.title}\n{course.description}\n" + "\n".join(lesson_summaries)
    context = {
        'course': course,
        'course_content': course_content,
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
    
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator=' ')
    
    tts = gTTS(text=clean_text, lang='pl')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")


@require_POST
def generate_assessment(request, course_id):
    """Generate assessment questions for a course."""
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Niepoprawny format żądania.',
        }, status=400)

    course_title = payload.get('course_title', '')
    course_content = payload.get('course_content', '')

    if not course_title or not course_content:
        course = get_object_or_404(Course, id=course_id)
        course_title = course.title
        lesson_summaries = []
        for lesson in course.lessons.all():
            lesson_text = f"Lekcja: {lesson.title}. {lesson.short_description or ''}."
            if lesson.content:
                lesson_text += f" {lesson.content[:300]}"
            lesson_summaries.append(lesson_text)
        course_content = f"{course.title}\n{course.description}\n" + "\n".join(lesson_summaries)

    if not course_content:
        return JsonResponse({
            'success': False,
            'error': 'Brakuje danych kursu.',
        }, status=400)

    try:
        questions = generate_assessment_questions(course_title, course_content)
    except GeminiConfigurationError as error:
        return JsonResponse({
            'success': False,
            'error': str(error),
        }, status=503)
    except Exception as error:
        return JsonResponse({
            'success': False,
            'error': f'Nie udało się wygenerować pytań: {error}',
        }, status=500)

    # Store in session
    session_id = request.session.session_key or request.session.create()
    assessment = {
        'course_id': str(course_id),
        'course_title': course_title,
        'course_content': course_content,
        'questions': questions,
    }
    request.session[f'assessment_{course_id}'] = assessment
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'questions': questions,
    })


@require_POST
def evaluate_assessment_view(request, course_id):
    """Evaluate user answers and provide feedback."""
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Niepoprawny format żądania.',
        }, status=400)

    answers = payload.get('answers', {})

    if not answers:
        return JsonResponse({
            'success': False,
            'error': 'Brakuje odpowiedzi.',
        }, status=400)

    assessment = request.session.get(f'assessment_{course_id}')
    if not assessment:
        return JsonResponse({
            'success': False,
            'error': 'Ocena nie znaleziona. Wygeneruj pytania ponownie.',
        }, status=400)

    try:
        evaluation = evaluate_assessment(
            assessment['course_title'],
            assessment['course_content'],
            assessment['questions'],
            answers
        )
    except GeminiConfigurationError as error:
        return JsonResponse({
            'success': False,
            'error': str(error),
        }, status=503)
    except Exception as error:
        return JsonResponse({
            'success': False,
            'error': f'Nie udało się ocenić odpowiedzi: {error}',
        }, status=500)

    # Store evaluation in session
    assessment['answers'] = answers
    assessment['evaluation'] = evaluation
    request.session[f'assessment_{course_id}'] = assessment
    request.session.modified = True

    # Optionally store in database for tracking
    try:
        CourseAssessment.objects.create(
            ai_course_id=course_id,
            course_title=assessment['course_title'],
            user_session_id=request.session.session_key,
            questions=assessment['questions'],
            answers=answers,
            evaluation_result=evaluation,
        )
    except Exception:
        pass  # Silently fail if database storage fails

    return JsonResponse({
        'success': True,
        'evaluation': evaluation,
    })
