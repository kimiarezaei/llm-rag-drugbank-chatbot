import json
from typing import Optional, Dict, Any


from .llm import call_llm
from utils.logger import get_logger
from config import settings



logger = get_logger(__name__)

def question_keywords(question: str) -> Optional[Dict[str, Any]]:
    """
    Extracts the drug name and main medical topic from a question using LLM.
    Returns None if no drug name is found.
    """

    logger.info("Extracting main keywords from the question: %s", question)

    prompt = f"""
Extract the drug name and most relevant information from the asked question.

Rules:
- Include the drug name if present.
- Extract the main medical topic.
- Add only 3 relevant synonyms for the main medical topic.
- Prefer clinical terms where appropriate.
- Do not add explanations.
- If no drug is mentioned, set "drugname" to NONE.
- Return a JSON object with this format:

{{
  "drugname": "drug name or NONE",
  "main_topic": "main medical topic",
  "main_topic_synonyms": [
    "synonym1",
    "synonym2",
    "synonym3"
  ]
}}

QUESTION:
{question}
"""

    response = call_llm(
        prompt,
        temperature=settings.keyword_temperature,
        max_tokens=settings.keyword_max_tokens
    )

    logger.info("Extracted keywords: %s", response)

    try:
        response = response.strip()

        # Remove markdown code fences if the LLM adds them
        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        keywords = json.loads(response)

    except json.JSONDecodeError:
        logger.error("Invalid JSON returned by LLM: %s", response)
        return None
    

    # Check the drugname field inside the JSON
    drugname = keywords.get("drugname")

    if not drugname or drugname.strip().upper() == "NONE":
        logger.warning("No drug name found in the question.")
        return "NONE"

    return keywords


