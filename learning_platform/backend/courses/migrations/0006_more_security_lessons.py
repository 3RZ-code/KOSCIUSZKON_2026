from django.db import migrations

def add_more_lessons(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    # Szukamy głównego kursu o bezpieczeństwie
    course = Course.objects.filter(title='Podstawy bezpieczeństwa').first()

    if course:
        # Lekcja 4: Wi-Fi i VPN
        Lesson.objects.create(
            course=course,
            title='Publiczne sieci Wi-Fi i VPN',
            category='Praktyka',
            expected_time=20,
            short_description='Dowiedz się, dlaczego darmowe Wi-Fi w kawiarni może być pułapką i jak VPN chroni Twoje połączenie.',
            content='''<p>Większość z nas chętnie korzysta z darmowego Wi-Fi w kawiarni, pociągu czy hotelu. Jednak publiczne hotspoty to jedno z najniebezpieczniejszych miejsc w sieci. Atakujący mogą stworzyć fałszywy punkt dostępu o nazwie łudząco podobnej do tej kawiarnianej (tzw. atak Evil Twin), aby przechwytywać wszystko, co robisz – Twoje hasła, wiadomości, a nawet dane karty płatniczej.</p><br>
            <p>Najlepszą ochroną w takich sytuacjach jest <strong>VPN (Virtual Private Network)</strong>. Wyobraź sobie VPN jako bezpieczny, całkowicie zaszyfrowany tunel, którym Twoje dane podróżują przez internet. Nawet jeśli haker "podejrzy" Twoją aktywność w sieci publicznej, zobaczy jedynie nieczytelny szyfr. W tej lekcji nauczysz się, jak rozpoznać bezpieczny punkt dostępu i jak w prosty sposób uruchomić VPN na swoim smartfonie.</p>''',
            order=4
        )

        # Lekcja 5: Prywatność i ślady cyfrowe
        Lesson.objects.create(
            course=course,
            title='Prywatność i ślad cyfrowy',
            category='Bezpieczeństwo',
            expected_time=20,
            short_description='Co internet wie o Tobie? Dowiedz się, jak ograniczyć informacje udostępniane w mediach społecznościowych.',
            content='''<p>Każde polubienie, zdjęcie czy komentarz zostawia po sobie trwały <strong>ślad cyfrowy</strong>. Te informacje tworzą Twój cyfrowy portret, który może być wykorzystany przez firmy marketingowe, a w najgorszym przypadku – przez oszustów do personalizowania ataków. Popularne zjawisko nadmiernego dzielenia się szczegółami z życia (oversharing) to częsta błąd użytkowników sieci.</p><br>
            <p>W tej lekcji dowiesz się, jak skonfigurować ustawienia prywatności na platformach takich jak Facebook czy Instagram. Zrozumiesz, dlaczego publikowanie zdjęć biletów lotniczych czy drogiego sprzętu domowego jest zaproszeniem dla przestępców. Dowiesz się również, czym są metadane w zdjęciach i jak mogą one zdradzić Twoją dokładną lokalizację nawet bez włączonego modułu GPS.</p>''',
            order=5
        )

        # Lekcja 6: Aktualizacje i kopie zapasowe
        Lesson.objects.create(
            course=course,
            title='Aktualizacje i kopie zapasowe',
            category='Profilaktyka',
            expected_time=25,
            short_description='Twoja ostatnia linia obrony: dlaczego systematyczność ratuje Twoje dane przed utratą.',
            content='''<p>Cyberbezpieczeństwo to nie tylko unikanie podejrzanych linków, to także dbanie o kondycję Twoich urządzeń. Powiadomienia o aktualizacji systemu czy aplikacji to często najważniejsza tarcza ochronna. Zawierają one tzw. <strong>łatki bezpieczeństwa</strong>, które naprawiają nowo odkryte luki, zanim hakerzy zdążą je wykorzystać.</p><br>
            <p>Równie ważna jest <strong>kopia zapasowa (backup)</strong>. W dobie wirusów szyfrujących dane (ransomware), backup to jedyny sposób na odzyskanie cennych pamiątek bez płacenia okupu. Nauczymy Cię zasady 3-2-1: miej 3 kopie danych, przechowuj je na 2 różnych nośnikach (np. chmura i dysk zewnętrzny), a 1 kopię trzymaj w innej lokalizacji fizycznej. To najprostsza polisa ubezpieczeniowa dla Twojego cyfrowego życia.</p>''',
            order=6
        )

def remove_lessons(apps, schema_editor):
    Lesson = apps.get_model('courses', 'Lesson')
    Lesson.objects.filter(title__in=['Publiczne sieci Wi-Fi i VPN', 'Prywatność i ślad cyfrowy', 'Aktualizacje i kopie zapasowe']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0005_more_courses_data'),
    ]
    operations = [
        migrations.RunPython(add_more_lessons, reverse_code=remove_lessons),
    ]