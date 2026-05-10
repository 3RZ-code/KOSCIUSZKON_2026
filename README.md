# HACKADEMIA
Projekt Django do nauki bezpieczeństwa i kursów generowanych przez AI.

## Opis

Aplikacja pozwala na wyświetlanie kursów z bazy danych oraz tworzenie kursów generowanych dynamicznie przez AI. Wygenerowane kursy są przechowywane w sesji użytkownika i mogą zostać odtworzone jako audio przy pomocy usługi TTS.

## Funkcje

- Lista kursów 
- Widok szczegółowy kursu i lekcji
- Generowanie kursu AI na podstawie tematu wpisanego przez użytkownika
- Przechowywanie wygenerowanych kursów w sesji przeglądarki
- Odtwarzanie treści wygenerowanych kursów jako dźwięk za pomocą gTTS

## Struktura repozytorium

- `learning_platform/backend/` - główny katalog aplikacji Django
  - `courses/` - aplikacja kursów i AI
  - `mainpage/` - widok strony głównej
  - `templates/` - szablony HTML aplikacji
  - `static/` - pliki CSS i JavaScript
  - `learning_platform/` - ustawienia projektu, URL-e, ASGI/WGSI

## Wymagania

- Python 3.11 lub nowszy
- Django 6.x
- `gtts`
- `beautifulsoup4`
- `google-genai` (jeśli włączasz generowanie kursów AI)

## Instalacja

1. Utwórz i aktywuj środowisko wirtualne:

```bash
python -m venv venv
venv\Scripts\Activate.ps1  # PowerShell
# lub
venv\Scripts\activate.bat   # Windows CMD
```

2. Zainstaluj zależności:

```bash
pip install django gtts beautifulsoup4 google-genai
```

3. Utwórz plik `.env` w katalogu `learning_platform/backend/` lub w katalogu głównym projektu:

```text
GEMINI_API_KEY=<twoj_klucz_gemini>
```

4. Jeśli chcesz, możesz uruchomić migracje (jeśli chcesz używać modeli Django):

```bash
cd learning_platform/backend
python manage.py migrate
```

## Uruchomienie

W katalogu `learning_platform/backend/` uruchom serwer:

```bash
python manage.py runserver
```

Następnie otwórz w przeglądarce:

```
http://127.0.0.1:8000/
```

## Generowanie kursu AI

Na stronie głównej znajduje się okienko AI Agenta. Po wpisaniu tematu i wygenerowaniu kursu, kurs zostanie zapisany w sesji przeglądarki i wyświetlony na stronie głównej.

## TTS dla kursów AI

W widoku `ai_course_detail.html` znajduje się przycisk do odczytu treści kursu na głos. Aplikacja wysyła zapytanie do endpointu:

```
/courses/listen/?text=...
```

który generuje audio za pomocą `gTTS` i zwraca plik MP3.

## Sesje i wygasanie kursów AI

Wygenerowane kursy AI są przechowywane w sesji Django (`request.session['generated_courses']`). Oznacza to, że kursy:

- są dostępne tylko dla tego samego użytkownika/przeglądarki,
- mogą zniknąć po wyczyszczeniu ciasteczek lub wygaśnięciu sesji.

## Uwaga

Aby funkcja generowania kursów AI działała, potrzebny jest poprawny klucz `GEMINI_API_KEY` w pliku `.env`. Jeśli nie jest ustawiony, funkcja zwróci błąd konfiguracji.
