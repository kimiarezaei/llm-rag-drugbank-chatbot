from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import node_keywords, node_qa, node_search_pubmed


workflow = StateGraph(AgentState)

# Add nodes to the workflow
workflow.add_node(
    "keywords",
    node_keywords
)

workflow.add_node(
    "qa",
    node_qa
)

workflow.add_node(
    "search_pubmed",
    node_search_pubmed
)


# Add edges to the workflow
workflow.add_edge(
    START,
    "keywords"
)

def check_drugname(state: AgentState):
    """
    Check if the drugname was found in the question.
    If not, return "end".
    """
    if state["drug_name"] == "NONE":
        return "end"
    else:
        return "qa_rag"


workflow.add_conditional_edges(
    "keywords",
    check_drugname,
    {
        "qa_rag": "qa",
        "end": END
    }
)


def check_qa_answer(state: AgentState):
    """
    Check if the drugname was found in the database.
    If not, route to PubMed search.
    """
    if state["qa_answer"] == "NONE":
        return "pubmed"
    else:
        return "end"
    

workflow.add_conditional_edges(
    "qa", 
    check_qa_answer,
    {
        "pubmed": "search_pubmed",
        "end": END
    }
)


workflow.add_edge(
    "search_pubmed",
    END
)


agent_app = workflow.compile()

