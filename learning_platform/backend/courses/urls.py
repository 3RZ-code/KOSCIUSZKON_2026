from django.urls import path
from . import views

urlpatterns = [
    path("<int:course_id>/", views.course_detail, name="course_detail"),
    path("generate-ai-course/", views.generate_ai_course, name="generate_ai_course"),
]