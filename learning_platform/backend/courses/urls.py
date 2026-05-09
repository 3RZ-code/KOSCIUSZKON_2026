from django.urls import path
from . import views

urlpatterns = [
    path('kurs<int:course_id>/', views.course_detail, name='course_detail'),
]