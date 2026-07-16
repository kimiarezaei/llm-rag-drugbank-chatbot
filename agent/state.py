from typing import TypedDict


class AgentState(TypedDict):
    question: str
    drug_name: str
    main_topic: str
    main_topic_synonyms: list
    qa_answer: str
    pubmed_answer: str
    



