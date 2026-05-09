from django.db import migrations


def create_sample_data(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    course, created = Course.objects.get_or_create(
        title='Podstawy bezpieczeństwa',
        defaults={
            'description': 'Kompleksowy kurs wprowadzający w świat cyberbezpieczeństwa. Nauczysz się, jak chronić swoje dane, rozpoznawać zagrożenia i dbać o swoje bezpieczeństwo w sieci.',
        }
    )

    if created or not course.lessons.exists():
        Lesson.objects.create(
            course=course,
            title='Wprowadzenie do cyberbezpieczeństwa',
            category='Teoria',
            expected_time=7,
            short_description='Dowiedz się, czym jest cyberbezpieczeństwo i dlaczego jest tak ważne w dzisiejszym cyfrowym świecie.',
            content='<p>Witaj w pierwszej lekcji kursu "Podstawy bezpieczeństwa". Cieszymy się, że postanowiłeś zgłębić z nami świat cyberbezpieczeństwa. W dzisiejszej lekcji odpowiemy na fundamentalne pytanie: czym właściwie jest cyberbezpieczeństwo i dlaczego dotyczy każdego z nas?</p><br><p>Wyobraź sobie swój cyfrowy świat jako dom. Przechowujesz w nim cenne przedmioty, prywatne dokumenty, pamiątkowe zdjęcia, a także prowadzisz poufne rozmowy. Cyberbezpieczeństwo to po prostu system zamków, alarmów i rolet, które chronią ten dom przed włamaniem. W ujęciu technicznym jest to zbiór technologii, procesów i dobrych praktyk, których celem jest ochrona sieci, urządzeń, programów i danych przed atakami, uszkodzeniami lub nieautoryzowanym dostępem.</p><br><p>Aby lepiej zrozumieć, co dokładnie staramy się chronić, eksperci do spraw cyberbezpieczeństwa posługują się tak zwaną triadą CIA. Nie ma ona nic wspólnego z amerykańską agencją wywiadowczą. Skrót ten pochodzi od pierwszych liter angielskich słów: Confidentiality, Integrity oraz Availability, co w tłumaczeniu na język polski oznacza: Poufność, Integralność i Dostępność. Przyjrzyjmy się im bliżej.</p><br><p>Poufność oznacza, że dostęp do informacji mają tylko osoby do tego uprawnione. Twoje hasła, wiadomości e-mail czy dane bankowe muszą pozostać prywatne i niedostępne dla osób trzecich.</p><br><p>Integralność to gwarancja, że informacje nie zostały w żaden sposób zmienione lub sfałszowane. Wyobraź sobie, że przelewasz komuś sto złotych. Integralność zapewnia, że kwota ta nie zostanie po drodze zmieniona przez hakera na tysiąc złotych, a numer konta odbiorcy pozostanie nienaruszony.</p><br><p>Dostępność oznacza, że systemy i dane są dostępne dla uprawnionych użytkowników zawsze, gdy tego potrzebują. Ataki w sieci bardzo często celują właśnie w dostępność – na przykład blokując działanie ważnych stron internetowych banków czy szpitali.</p><br><p>Zastanówmy się teraz, z kim właściwie mamy do czynienia. Kto próbuje złamać nasze zabezpieczenia? Cyberprzestępcy to zróżnicowana grupa. Ich główną motywacją najczęściej są pieniądze. Wykradają dane, by je sprzedać, lub blokują dostęp do plików, by żądać okupu. Inni atakują z powodów politycznych, biznesowych lub po prostu dla zyskania sławy w hakerskim podziemiu.</p><br><p>Wielu ludzi uważa: "Nie jestem prezesem wielkiej korporacji, nikt nie będzie mnie atakował, nie mam nic do ukrycia". To bardzo niebezpieczny mit. Dzisiejsze ataki w dużej mierze są całkowicie zautomatyzowane. Hakerzy nie wybierają pojedynczych osób; zarzucają w sieci szeroką sieć pułapek, licząc na to, że ktoś popełni błąd i w nią wpadnie. Ponadto, Twoje dane osobowe, dostęp do skrzynki pocztowej czy konta na portalu społecznościowym to dla przestępców niezwykle cenny towar. Mogą one posłużyć do oszukania Twoich znajomych lub rodziny, na przykład niezwykle popularną w Polsce metodą wyłudzania pieniędzy przez komunikatory internetowe.</p><br><p>Podsumowując, bezpieczeństwo w sieci to nie tylko zaawansowane systemy informatyczne wielkich firm. To przede wszystkim nasza codzienna, ludzka uważność. Zrozumienie fundamentów, takich jak ochrona poufności, integralności i dostępności, to Twój pierwszy krok do stania się świadomym i bezpiecznym użytkownikiem internetu.</p><br><p>W następnej lekcji przejdziemy do praktyki. Zajmiemy się tym, jak tworzyć silne hasła, jak wygodnie korzystać z menedżerów haseł oraz dlaczego uwierzytelnianie dwuskładnikowe jest dziś absolutną koniecznością. Dziękuję za wysłuchanie dzisiejszej lekcji i zapraszam do kolejnej!</p>',
            order=1,
        )
        Lesson.objects.create(
            course=course,
            title='Bezpieczeństwo haseł i uwierzytelnianie',
            category='Praktyka',
            expected_time=20,
            short_description='Zrozum, jak tworzyć silne hasła i dlaczego uwierzytelnianie dwuskładnikowe (2FA) jest kluczowe.',
            content='<p>Hasła to często Twoja pierwsza i jedyna linia obrony w cyfrowym świecie. Słabe hasła, takie jak <em>"123456"</em>, <em>"qwerty"</em> czy imię psa, mogą zostać złamane przez hakerów w ułamku sekundy przy użyciu ataków słownikowych lub <i>brute-force</i>.</p><br><p>W tej lekcji nauczysz się, jak poprawnie tworzyć silne, unikalne dla każdej witryny hasła za pomocą <strong>menedżerów haseł</strong> (np. Bitwarden, 1Password). Omówimy techniki tworzenia <i>passphrases</i> (fraz hasłowych), które są łatwe do zapamiętania dla człowieka, ale niesamowicie trudne do złamania dla komputera.</p><br><p>Ponadto dogłębnie przeanalizujemy mechanizm <strong>uwierzytelniania dwuskładnikowego (2FA/MFA)</strong>. Dowiesz się, dlaczego kody SMS bywają zawodne, jak działają aplikacje autentykujące (np. Google Authenticator) oraz w jaki sposób fizyczne klucze sprzętowe (np. YubiKey) zapewniają najwyższy standard bezpieczeństwa.</p>',
            order=2,
        )
        Lesson.objects.create(
            course=course,
            title='Rozpoznawanie phishingu i socjotechniki',
            category='Zagrożenia',
            expected_time=25,
            short_description='Naucz się identyfikować fałszywe wiadomości e-mail oraz psychologiczne manipulacje socjotechniczne.',
            content='<p><strong>Socjotechnika (social engineering)</strong> to sztuka manipulacji ludźmi w celu skłonienia ich do ujawnienia poufnych informacji. Często technologia nie ma tu znaczenia – najsłabszym ogniwem w łańcuchu bezpieczeństwa jest sam człowiek. Atakujący wykorzystują emocje: strach, pośpiech, ciekawość, a nawet współczucie.</p><br><p><strong>Phishing</strong> to najpopularniejsza forma socjotechniki, realizowana zazwyczaj poprzez fałszywe e-maile i SMSy udające wiadomości od zaufanych instytucji, banków, czy kurierów. W tej lekcji dowiesz się, na co zwracać szczególną uwagę: ukryte adresy nadawców, fałszywe subdomeny, literówki w adresach URL (np. <i>rnBank.com</i> zamiast <i>mBank.com</i>) oraz wywieranie sztucznej presji czasu.</p><br><p>Przeanalizujemy przykłady z życia wzięte oraz nauczymy Cię, jak bezpiecznie weryfikować podejrzane komunikaty. Zrozumiesz złote zasady, takie jak "Nigdy nie klikaj w linki do płatności w wiadomościach z nieznanego źródła" i jak mądrze korzystać z internetu.</p>',
            order=3,
        )


def remove_sample_data(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    courses = Course.objects.filter(title='Podstawy bezpieczeństwa')
    courses.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_short_description_alter_lesson_content'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, reverse_code=remove_sample_data),
    ]