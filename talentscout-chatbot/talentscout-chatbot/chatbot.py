import json
import os
from typing import List, Dict, Any, Optional
from prompts import SYSTEM_PROMPT, QUESTION_PROMPT, FALLBACK_PROMPT

# Optional OpenAI
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _openai_client():
    try:
        from openai import OpenAI
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        return OpenAI()
    except Exception:
        return None

# Minimal, hand-curated fallback bank for common techs
FALLBACK_QUESTION_BANK = {
    "python": [
        "Explain list vs tuple and when you would use each.",
        "What are decorators and a common use-case?",
        "How does list comprehension work? Provide an example.",
        "What is a virtual environment and why is it useful?",
        "How do generators differ from regular functions?"
    ],
    "django": [
        "Explain the role of models, views, and templates in Django.",
        "How do Django migrations work and when do you create one?",
        "What is the difference between ForeignKey and ManyToManyField?",
        "How do you secure sensitive settings like SECRET_KEY?",
        "What is the ORM query to filter users by email domain?"
    ],
    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How would you find duplicate rows in a table?",
        "Explain indexing and a scenario where it helps performance.",
        "What is normalization and why is it important?",
        "How do transactions ensure consistency?"
    ],
    "javascript": [
        "Explain var vs let vs const.",
        "What is event delegation and why is it useful?",
        "How do promises differ from async/await?",
        "What is a closure and a common use-case?",
        "How does the DOM event loop affect rendering?"
    ],
    "react": [
        "What are React hooks and why were they introduced?",
        "Explain useEffect's dependency array with an example.",
        "How do you memoize expensive computations in React?",
        "What is the difference between state and props?",
        "How would you handle forms and validation in React?"
    ]
}

def _openai_json_completion(system: str, user: str, json_mode: bool = True) -> Optional[str]:
    client = _openai_client()
    if not client:
        return None
    try:
        # Use Chat Completions and ask for JSON content
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=0.4,
            max_tokens=800,
            response_format={ "type": "json_object" } if json_mode else None
        )
        return resp.choices[0].message.content
    except Exception:
        return None

def generate_questions_for_stack(tech_stack: List[str]) -> List[Dict[str, Any]]:
    tech_stack_clean = [t.strip() for t in tech_stack if str(t).strip()]
    if not tech_stack_clean:
        return []

    # Try OpenAI JSON generation first
    content = _openai_json_completion(
        SYSTEM_PROMPT,
        QUESTION_PROMPT.format(tech_stack=", ".join(tech_stack_clean)),
        json_mode=True
    )
    if content:
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "technologies" in data:
                return data["technologies"]
        except Exception:
            pass

    # Fallback: build from hand-curated bank or generic questions
    technologies = []
    for tech in tech_stack_clean:
        key = tech.lower()
        qs = FALLBACK_QUESTION_BANK.get(key)
        if not qs:
            # Ask OpenAI for a plain JSON list (best-effort)
            content = _openai_json_completion(
                SYSTEM_PROMPT,
                FALLBACK_PROMPT.format(tech=tech),
                json_mode=False  # may return plain text; we'll try to parse
            )
            parsed = None
            if content:
                try:
                    parsed = json.loads(content)
                except Exception:
                    # Attempt to extract lines starting with "- " or similar
                    lines = [l.strip("- •\t ") for l in content.splitlines() if l.strip()]
                    parsed = [l for l in lines if len(l) > 6][:5] if lines else None
            qs = parsed or [
                f"What are the core components or primitives in {tech}?",
                f"Explain a common performance pitfall in {tech} and how to avoid it.",
                f"How do you test {tech} code in CI?",
                f"Describe a debugging workflow you would use in {tech}.",
                f"What security considerations are important when using {tech}?",
            ]
        technologies.append({"name": tech, "questions": qs[:5]})
    return technologies
