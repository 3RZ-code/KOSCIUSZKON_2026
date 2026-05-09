from django.db import migrations


def create_sample_data(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    course, created = Course.objects.get_or_create(
        title='Testowy kurs',
        defaults={
            'description': 'To jest przykładowy kurs testowy do sprawdzenia działania strony kursu oraz text to speech.',
        }
    )

    if created or not course.lessons.exists():
        Lesson.objects.create(
            course=course,
            title='Wprowadzenie do kursu',
            category='Wstęp',
            expected_time=5,
            short_description='Poznaj strukturę kursu i podstawowe informacje.',
            content='W tej lekcji zapoznasz się z celem kursu, jego zawartością oraz sposobem nauki.',
            order=1,
        )
        Lesson.objects.create(
            course=course,
            title='Podstawy języka',
            category='Nauka',
            expected_time=10,
            short_description='Pierwsze kroki z językiem i najważniejsze wyrażenia.',
            content='W tej lekcji uczymy się podstawowych zwrotów, powitań oraz prostych zdań.',
            order=2,
        )
        Lesson.objects.create(
            course=course,
            title='Ćwiczenia praktyczne',
            category='Ćwiczenia',
            expected_time=8,
            short_description='Sprawdź wiedzę w praktycznych przykładach.',
            content='Przećwiczysz poznane wyrażenia i nauczysz się stosować je w krótkich dialogach.',
            order=3,
        )


def remove_sample_data(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    courses = Course.objects.filter(title='Testowy kurs')
    courses.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_short_description_alter_lesson_content'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, reverse_code=remove_sample_data),
    ]
