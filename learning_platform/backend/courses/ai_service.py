import json
import re

from django.conf import settings
from google import genai


def _extract_json_from_text(text: str) -> dict:
    """
    Gemini czasem zwraca JSON w bloku ```json ... ```.
    Ta funkcja próbuje wyciągnąć czysty JSON z odpowiedzi.
    """
    text = text.strip()

    # Usunięcie bloku markdown ```json ... ```
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    return json.loads(text)


def generate_course_with_gemini(topic: str) -> dict:
    if not settings.GEMINI_API_KEY:
        raise ValueError("Brakuje GEMINI_API_KEY w pliku .env")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
Wygeneruj krótki kurs edukacyjny po polsku dla początkujących użytkowników.
Temat kursu: {topic}

Kurs dotyczy cyberbezpieczeństwa albo bezpiecznego korzystania z Internetu.

Zasady:
- pisz prostym językiem,
- kurs ma być odpowiedni dla początkujących,
- nie używaj trudnych pojęć bez wyjaśnienia,
- dodaj praktyczne przykłady,
- nie obiecuj stuprocentowej ochrony,
- treść ma być edukacyjna i bezpieczna.

Zwróć odpowiedź WYŁĄCZNIE jako poprawny JSON, bez markdown i bez dodatkowego komentarza.

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

    required_fields = ["title", "category", "description", "estimated_time", "level", "content"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Brakuje pola w odpowiedzi Gemini: {field}")

    data["estimated_time"] = int(data["estimated_time"])

    return data