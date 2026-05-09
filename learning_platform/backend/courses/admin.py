from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "estimated_time", "level", "is_ai_generated", "created_at")
    list_filter = ("category", "level", "is_ai_generated")
    search_fields = ("title", "description", "content")