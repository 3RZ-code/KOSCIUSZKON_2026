import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .ai_service import generate_course_with_gemini
from .models import Course


def course_detail(request, course_id):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    course = get_object_or_404(Course, id=course_id)

    if course.is_ai_generated and course.session_key != session_key:
        return render(request, "course_not_available.html", status=403)

    return render(request, "course_detail.html", {
        "course": course,
    })


@require_POST
def generate_ai_course(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    try:
        payload = json.loads(request.body)
        topic = payload.get("topic", "").strip()

        if not topic:
            return JsonResponse({
                "success": False,
                "error": "Podaj temat kursu."
            }, status=400)

        if len(topic) > 150:
            return JsonResponse({
                "success": False,
                "error": "Temat kursu jest zbyt długi. Maksymalnie 150 znaków."
            }, status=400)

        course_data = generate_course_with_gemini(topic)

        course = Course.objects.create(
            title=course_data["title"],
            category=course_data["category"],
            description=course_data["description"],
            content=course_data["content"],
            estimated_time=course_data["estimated_time"],
            level=course_data["level"],
            is_ai_generated=True,
            session_key=session_key,
        )

        return JsonResponse({
            "success": True,
            "course_id": course.id,
            "title": course.title,
            "message": "Kurs został wygenerowany."
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Niepoprawny format żądania."
        }, status=400)

    except Exception as e:
        import traceback
        traceback.print_exc()

        return JsonResponse({
            "success": False,
            "error": f"Błąd backendu: {str(e)}"
        }, status=500)