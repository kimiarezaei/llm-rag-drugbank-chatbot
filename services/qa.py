from .llm import call_llm
from .retrieval import search
from utils.logger import get_logger
from config import settings



logger = get_logger(__name__)

def answer_question(question: str, drug_name: str) -> str:
    """
    Answers a question using RAG (retrieval-augmented generation).
    """

    logger.info(f"QA question and drug name received: {question}, {drug_name}")

    # Check if drug exists in database
    drug_chunks = search(drug_name)

    if not drug_chunks:
        logger.info(
            "Drug '%s' not found in database",
            drug_name
        )
        return "NONE"


    # Retrieve relevant chunks regarding the question
    relevant_chunks = search(question)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are a precise question-answering assistant for a biomedical and pharmaceutical knowledge base.

You must follow these rules strictly:

1. Use ONLY the provided context to answer.
2. Do NOT use any external knowledge or assumptions.
3. If the answer is not explicitly stated in the context, say:
   "Not found in the provided context."
4. Be concise and factual.
5. If relevant, quote short exact phrases from the context to support your answer.


CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = call_llm(prompt, temperature=settings.qa_temperature, max_tokens=settings.qa_max_tokens)

    logger.info("QA response generated using RAG")

    return response.strip()

