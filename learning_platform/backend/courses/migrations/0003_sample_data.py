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
            content='W tej lekcji zapoznasz się z celem kursu, jego zawartością oraz sposobem nauki. Czym jest spoofing? Spoofing to jedna z najpopularniejszych technik manipulacji stosowana przez cyberprzestępców. Polega ona na podszywaniu się pod zaufane osoby, firmy lub urządzenia w celu wyłudzenia danych, pieniędzy lub zainfekowania komputera złośliwym oprogramowaniem. Kluczem do sukcesu atakującego jest wzbudzenie w ofierze fałszywego poczucia bezpieczeństwa. Najpopularniejsze rodzaje spoofingu: 1. Caller ID Spoofing: na ekranie Twojego smartfona wyświetla się nazwa Twojego banku lub numer policji, mimo że w rzeczywistości dzwoni oszust. 2. Email Spoofing: otrzymujesz wiadomość, która wygląda identycznie jak oficjalny komunikat od dostawcy poczty, ale linki prowadzą do fałszywych stron. 3. IP Spoofing: atakujący modyfikuje pakiety danych tak, aby systemy sieciowe myślały, że pochodzą one z bezpiecznego źródła. Pamiętaj o zasadzie ograniczonego zaufania: zawsze weryfikuj tożsamość rozmówcy i nigdy nie podawaj haseł przez telefon.',   
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
