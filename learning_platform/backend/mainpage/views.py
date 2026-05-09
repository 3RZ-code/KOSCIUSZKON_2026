from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from courses.models import Course


@ensure_csrf_cookie
def home(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    courses = Course.objects.filter(is_ai_generated=False).order_by("created_at")
    generated_courses = Course.objects.filter(
        is_ai_generated=True,
        session_key=session_key
    ).order_by("-created_at")

    return render(request, "home.html", {
        "courses": courses,
        "generated_courses": generated_courses,
    })