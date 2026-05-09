import json
import re
import uuid

from django.conf import settings

try:
    from google import genai
except ImportError:
    genai = None


class GeminiConfigurationError(RuntimeError):
    pass


def _extract_json_from_text(text):
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)

    if match:
        text = match.group(1).strip()

    return json.loads(text)


def _normalize_course(data, topic):
    lessons = data.get('lessons') or []

    if not lessons:
        lessons = [
            {
                'title': 'Wprowadzenie',
                'category': 'Podstawy',
                'expected_time': 5,
                'short_description': f'Krótki start z tematem: {topic}.',
                'content': data.get('content', ''),
            }
        ]

    normalized_lessons = []
    for index, lesson in enumerate(lessons, start=1):
        normalized_lessons.append({
            'id': f'lesson-{index}',
            'title': lesson.get('title', f'Lekcja {index}'),
            'category': lesson.get('category', 'AI'),
            'expected_time': int(lesson.get('expected_time', 6)),
            'short_description': lesson.get('short_description', ''),
            'content': lesson.get('content', ''),
        })

    return {
        'id': uuid.uuid4().hex,
        'title': data.get('title', f'Kurs: {topic}'),
        'category': data.get('category', 'AI'),
        'description': data.get('description', 'Spersonalizowany kurs wygenerowany przez AI.'),
        'level': data.get('level', 'Poziom 1'),
        'lessons': normalized_lessons,
    }


def generate_course_with_gemini(topic):
    if genai is None:
        raise GeminiConfigurationError(
            'Generator AI jest niedostępny, bo brakuje biblioteki google-genai.'
        )

    if not settings.GEMINI_API_KEY:
        raise GeminiConfigurationError(
            'Generator AI jest niedostępny. Brakuje GEMINI_API_KEY w pliku backend/.env.'
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
Wygeneruj krótki kurs edukacyjny po polsku dla początkujących użytkowników.
Temat kursu: {topic}

Kurs dotyczy cyberbezpieczeństwa albo bezpiecznego korzystania z Internetu.

Zasady:
- pisz prostym językiem,
- kurs ma mieć dokładnie 3 lekcje,
- każda lekcja ma mieć praktyczny, bezpieczny charakter,
- nie używaj trudnych pojęć bez wyjaśnienia,
- nie obiecuj stuprocentowej ochrony,
- zwróć wyłącznie poprawny JSON.

Format JSON:
{{
  "title": "Tytuł kursu",
  "category": "Kategoria",
  "description": "Krótki opis kursu",
  "level": "Poziom 1",
  "lessons": [
    {{
      "title": "Tytuł lekcji",
      "category": "Kategoria",
      "expected_time": 6,
      "short_description": "Krótki opis lekcji",
      "content": "Pełna treść lekcji"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    data = _extract_json_from_text(response.text)
    return _normalize_course(data, topic)
