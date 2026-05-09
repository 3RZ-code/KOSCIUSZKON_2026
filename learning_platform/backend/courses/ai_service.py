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

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            json_text = text[start:end + 1]
            return json.loads(json_text)

        raise


def _normalize_course(data, topic):
    return {
        "id": uuid.uuid4().hex,
        "title": data.get("title", f"Kurs: {topic}"),
        "category": data.get("category", "AI"),
        "description": data.get(
            "description",
            "Spersonalizowany kurs wygenerowany przez AI."
        ),
        "estimated_time": int(data.get("estimated_time", 8)),
        "level": data.get("level", "Poziom 1"),
        "content": data.get("content", ""),
    }


def generate_course_with_gemini(topic):
    if genai is None:
        raise GeminiConfigurationError(
            "Generator AI jest niedostępny, bo brakuje biblioteki google-genai."
        )

    if not settings.GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "Generator AI jest niedostępny. Brakuje GEMINI_API_KEY w pliku backend/.env."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
Wygeneruj krótki kurs edukacyjny po polsku dla początkujących użytkowników.
Temat kursu: {topic}

Kurs dotyczy cyberbezpieczeństwa albo bezpiecznego korzystania z Internetu.

Zasady:
- pisz prostym językiem,
- kurs ma być jednym spójnym materiałem, a nie listą lekcji,
- nie twórz pola "lessons",
- dodaj praktyczne przykłady,
- nie używaj trudnych pojęć bez wyjaśnienia,
- nie obiecuj stuprocentowej ochrony,
- treść powinna być podzielona na krótkie sekcje z nagłówkami,
- zwróć wyłącznie poprawny JSON.

Format JSON:
{{
  "title": "Tytuł kursu",
  "category": "Kategoria",
  "description": "Krótki opis kursu, maksymalnie 2 zdania",
  "estimated_time": 8,
  "level": "Poziom 1",
  "content": "Pełna treść kursu z nagłówkami i sekcjami"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    data = _extract_json_from_text(response.text)
    return _normalize_course(data, topic)