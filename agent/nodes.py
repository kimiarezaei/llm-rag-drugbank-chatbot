from .state import AgentState
from services.keywords import question_keywords
from services.qa import answer_question
from services.pubmed import search_pubmed


def node_keywords(state: AgentState):
    """
    Node that extracts the drug name and main medical topic from the question.
    """

    question = state["question"]
    keywords = question_keywords(question)

    if keywords is None:
        return {
            "drug_name": None,
            "main_topic": None,
            "main_topic_synonyms": []
        }

    return {
        "drug_name": keywords.get("drugname"),
        "main_topic": keywords.get("main_topic"),
        "main_topic_synonyms": keywords.get("main_topic_synonyms", [])
    }


def node_qa(state: AgentState):
    """
    Node that answers a question using the answer_question function using RAG.
    """

    question = state["question"]
    drug_name = state["drug_name"]
    result = answer_question(question, drug_name)

    return {
        "qa_answer": result
    }


def node_search_pubmed(state: AgentState):
    """
    Node that searches PubMed for the given question.
    """

    drug_name = state["drug_name"]
    main_topic = state["main_topic"]
    main_topic_synonyms = state["main_topic_synonyms"]
    results = search_pubmed(drug_name, main_topic, main_topic_synonyms)

    return {
        "pubmed_answer": results   
    }





