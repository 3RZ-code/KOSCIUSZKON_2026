from django.db import migrations

def add_more_courses(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    # Kurs 1: Poziom Podstawowy (Idealny dla początkujących i dzieci)
    course_basic, _ = Course.objects.get_or_create(
        title='Cyber-higiena na co dzień',
        defaults={
            'description': 'Poziom: Podstawowy. Proste, codzienne nawyki, które uchronią Twoje dane, prywatność i pieniądze. Dowiedz się, na co uważać w portalach społecznościowych.',
        }
    )
    Lesson.objects.get_or_create(course=course_basic, title='Zasada ograniczonego zaufania', defaults={'category': 'Teoria', 'expected_time': 10, 'short_description': 'Podstawowe zasady poruszania się po internecie.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 1})
    Lesson.objects.get_or_create(course=course_basic, title='Bezpieczne zakupy online', defaults={'category': 'Praktyka', 'expected_time': 15, 'short_description': 'Jak sprawdzić, czy sklep internetowy nie jest oszustwem.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 2})

    # Kurs 2: Poziom Średniozaawansowany
    course_inter, _ = Course.objects.get_or_create(
        title='Ochrona sieci domowej i Wi-Fi',
        defaults={
            'description': 'Poziom: Średniozaawansowany. Zabezpiecz swój domowy router, sieć Wi-Fi oraz urządzenia Smart Home przed nieautoryzowanym dostępem sąsiadów i hakerów.',
        }
    )
    Lesson.objects.get_or_create(course=course_inter, title='Konfiguracja bezpiecznego routera', defaults={'category': 'Sieci', 'expected_time': 20, 'short_description': 'Wyłączanie WPS i zmiana domyślnych haseł.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 1})
    Lesson.objects.get_or_create(course=course_inter, title='Pułapki publicznego Wi-Fi', defaults={'category': 'Zagrożenia', 'expected_time': 15, 'short_description': 'Dlaczego darmowe Wi-Fi w kawiarni to zły pomysł i jak używać VPN.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 2})
    Lesson.objects.get_or_create(course=course_inter, title='Bezpieczeństwo IoT', defaults={'category': 'Sprzęt', 'expected_time': 25, 'short_description': 'Czy Twoja inteligentna żarówka lub telewizor mogą Cię szpiegować?', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 3})

    # Kurs 3: Poziom Zaawansowany
    course_adv, _ = Course.objects.get_or_create(
        title='Podstawy kryptografii i szyfrowania',
        defaults={
            'description': 'Poziom: Zaawansowany. Zajrzyj pod maskę internetu. Poznaj matematyczne zasady szyfrowania danych, dzięki którym Twoje połączenie z bankiem jest bezpieczne.',
        }
    )
    Lesson.objects.get_or_create(course=course_adv, title='Szyfrowanie symetryczne vs asymetryczne', defaults={'category': 'Teoria', 'expected_time': 30, 'short_description': 'Zrozum, czym różnią się algorytmy AES i RSA.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 1})
    Lesson.objects.get_or_create(course=course_adv, title='Certyfikaty SSL/TLS i HTTPS', defaults={'category': 'Sieci', 'expected_time': 35, 'short_description': 'Co technicznie oznacza kłódka w Twojej przeglądarce.', 'content': '<p>Lekcja w przygotowaniu...</p>', 'order': 2})


def remove_more_courses(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Course.objects.filter(title__in=['Cyber-higiena na co dzień', 'Ochrona sieci domowej i Wi-Fi', 'Podstawy kryptografii i szyfrowania']).delete()


class Migration(migrations.Migration):

    dependencies = [
        # Zależność od pliku 0004_alter_course_id_alter_lesson_id, 
        # upewnij się, że taka nazwa zgadza się z Twoim poprzednim plikiem migracji
        ('courses', '0004_alter_course_id_alter_lesson_id'),
    ]

    operations = [
        migrations.RunPython(add_more_courses, reverse_code=remove_more_courses),
    ]