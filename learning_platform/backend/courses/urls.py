from django.urls import path
from . import views

urlpatterns = [
    path('generate-ai-course/', views.generate_ai_course, name='generate_ai_course'),
    path('ai/<str:course_id>/', views.ai_course_detail, name='ai_course_detail'),
    path('ai/<str:course_id>/assessment/', views.generate_assessment, name='generate_assessment'),
    path('ai/<str:course_id>/evaluate/', views.evaluate_assessment_view, name='evaluate_assessment'),
    path('kurs<int:course_id>/', views.course_detail, name='course_detail'),
    path('kurs<int:course_id>/lekcja<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('listen/', views.speak_view, name = 'listen'),
]
