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


def _parse_int(value, default=None):
    if value is None:
        return default

    if isinstance(value, str):
        value = value.strip()
        if value.endswith('%'):
            value = value[:-1].strip()
        if not value:
            return default

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def _normalize_evaluation_response(data):
    if not isinstance(data, dict):
        return {
            'overall_score': 0,
            'overall_percentage': '0%',
            'feedback': '',
            'topic_mastery': [],
            'recommendations': [],
        }

    overall_score = _parse_int(data.get('overall_score'))
    overall_percentage = data.get('overall_percentage')
    percent_score = None

    if isinstance(overall_percentage, str):
        percent_match = re.search(r"(\d+)", overall_percentage)
        if percent_match:
            percent_score = int(percent_match.group(1))

    if overall_score is None:
        overall_score = percent_score

    if overall_score is None and isinstance(data.get('topic_mastery'), list):
        topic_scores = []
        for topic in data['topic_mastery']:
            score = _parse_int(topic.get('score'))
            if score is not None:
                topic_scores.append(score)
        if topic_scores:
            average_score = sum(topic_scores) / len(topic_scores)
            overall_score = int(round(average_score * 10)) if average_score <= 10 else int(round(average_score))

    if overall_score is None:
        overall_score = 0

    if percent_score is not None and percent_score != overall_score:
        overall_score = percent_score
    elif overall_score <= 10:
        overall_score = overall_score * 10

    overall_score = max(0, min(100, overall_score))
    overall_percentage = f"{overall_score}%"

    topic_mastery = []
    if isinstance(data.get('topic_mastery'), list):
        for topic in data['topic_mastery']:
            if not isinstance(topic, dict):
                continue
            score = _parse_int(topic.get('score'), 0)
            if score <= 10:
                score = score
            status = str(topic.get('status', '')).strip().lower()
            if status not in ('known', 'needs_review', 'needs review'):
                status = 'known' if score >= 7 else 'needs_review'
            feedback = topic.get('feedback', '') or ''
            topic_mastery.append({
                'topic': topic.get('topic', ''),
                'score': max(0, min(10, score)),
                'status': status,
                'feedback': feedback,
            })

    recommendations = []
    if isinstance(data.get('recommendations'), list):
        recommendations = [str(item) for item in data['recommendations'] if item is not None]

    return {
        'overall_score': overall_score,
        'overall_percentage': overall_percentage,
        'feedback': data.get('feedback', '') or '',
        'topic_mastery': topic_mastery,
        'recommendations': recommendations,
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


def generate_assessment_questions(course_title, course_content):
    """
    Generate assessment questions for a course using Gemini.
    Returns a list of 6-7 questions about the course content.
    """
    if genai is None:
        raise GeminiConfigurationError(
            "Generator ocen jest niedostępny, bo brakuje biblioteki google-genai."
        )

    if not settings.GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "Generator ocen jest niedostępny. Brakuje GEMINI_API_KEY w pliku backend/.env."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
Wygeneruj zestaw oceniających pytań o wiedzy dla kursu edukacyjnego.

Tytuł kursu: {course_title}

Treść kursu:
{course_content}

Zasady:
- Wygeneruj dokładnie 6-7 pytań otwartych po polsku
- Pytania powinny być zróżnicowane - od podstawowych do bardziej zaawansowanych
- Każde pytanie powinno sprawdzać zrozumienie konkretnego aspektu kursu
- Pytania powinny być sformułowane w taki sposób, aby można było ocenić poziom wiedzy
- Zwróć wyłącznie poprawny JSON

Format JSON:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Tekst pytania",
      "topic": "Główny temat, który pytanie sprawdza"
    }},
    {{
      "id": 2,
      "question": "Tekst pytania",
      "topic": "Główny temat, który pytanie sprawdza"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    data = _extract_json_from_text(response.text)
    return data.get("questions", [])


def evaluate_assessment(course_title, course_content, questions, answers):
    """
    Evaluate student answers using Gemini.
    Returns evaluation with score, feedback, and topic mastery levels.
    """
    if genai is None:
        raise GeminiConfigurationError(
            "Ewaluator AI jest niedostępny, bo brakuje biblioteki google-genai."
        )

    if not settings.GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "Ewaluator AI jest niedostępny. Brakuje GEMINI_API_KEY w pliku backend/.env."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Format questions and answers for evaluation
    q_a_pairs = []
    for q in questions:
        q_id = str(q.get("id", ""))
        answer = answers.get(q_id, "")
        q_a_pairs.append({
            "question": q.get("question", ""),
            "topic": q.get("topic", ""),
            "answer": answer
        })

    prompt = f"""
Oceń odpowiedzi studentów do pytań oceniających. Oceń ich poziom wiedzy na temat kursu.

Tytuł kursu: {course_title}

Treść kursu:
{course_content}

Pytania i odpowiedzi:
{json.dumps(q_a_pairs, ensure_ascii=False, indent=2)}

Zadania:
1. Oceń każdą odpowiedź na skali 0-10 (gdzie 0 = brak wiedzy, 10 = ekspercka wiedza)
2. Dla każdego tematu (topic) określ czy student już ma o tym wiedzę, czy potrzebuje nauki
3. Wylicz ogólny procent opanowanej wiedzy
4. Podaj konkretne rekomendacje, które sekcje kursu student powinien przejrzeć
5. Napisz ogólną zwrotną informację dla studenta
6. W wyniku JSON podaj ogólny wynik jako liczbę 0-100 oraz procentową reprezentację w formacie "xx%"
7. Jeśli podasz wynik 0-10 zamiast 0-100, przeskaluj go do 0-100
8. Zwróć wyłącznie poprawny JSON

Format JSON:
{{
  "overall_score": 65,
  "overall_percentage": "65%",
  "feedback": "Ogólna zwrotna informacja dla studenta",
  "topic_mastery": [
    {{
      "topic": "Nazwa tematu",
      "score": 7,
      "status": "known" lub "needs_review",
      "feedback": "Konkretna zwrotna dla tego tematu"
    }}
  ],
  "recommendations": [
    "Rekomendacja 1",
    "Rekomendacja 2"
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    data = _extract_json_from_text(response.text)
    return _normalize_evaluation_response(data)