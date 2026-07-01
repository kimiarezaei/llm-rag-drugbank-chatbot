from anthropic import Anthropic
from config import settings
from dotenv import load_dotenv
from utils.logger import get_logger

client = Anthropic(api_key=settings.anthropic_api_key)

logger = get_logger(__name__)
def call_llm(
    prompt: str,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> str:
    
    """
    Generic LLM call wrapper.
    Keeps API logic isolated from business logic.
    """

    try:
        logger.info("Calling Claude API")

        response = client.messages.create(
            model=settings.model_name,
            temperature=settings.temperature if temperature is None else temperature,
            max_tokens=settings.max_tokens if max_tokens is None else max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.content[0].text

        logger.info("Claude response received successfully")

        return result

    except Exception as e:
        logger.exception("Claude API call failed")
        raise



