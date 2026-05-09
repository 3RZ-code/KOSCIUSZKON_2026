from django.urls import path
from . import views

urlpatterns = [
    path('kurs<int:course_id>/', views.course_detail, name='course_detail'),
    path('kurs<int:course_id>/lekcja<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]