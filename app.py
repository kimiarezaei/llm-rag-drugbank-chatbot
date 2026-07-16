import streamlit as st

from config import settings
from utils.logger import get_logger

from data_cache import load_data
from services.retrieval import build_index
from agent.workflow import agent_app



# Logger
logger = get_logger(__name__)

DB_PATH = settings.chroma_path


# Initialize everything (cached)
@st.cache_resource
def initialize_app():
    logger.info("Initializing application...")

    # Load dataset (cached via your JSON cache)
    docs = load_data()

    # Build / load vector index
    build_index(docs)

    logger.info("App initialized successfully")

    return True



# Streamlit App
def run_app():
    st.set_page_config(page_title="DrugBank QA", layout="wide")

    st.header("DrugBank QA Chat")

    # Initialize backend once
    if not st.session_state.get("initialized", False):
        initialize_app()

    # Session state for chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Clear history button
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    # Input
    question = st.text_input("Ask a question:")

    if st.button("Answer"):

        if question.strip():
            logger.info("User question: %s", question)

            # retrieve context 
            result = agent_app.invoke(
                {
                    "question": question
                }
            )
            
            if result["qa_answer"] != "NONE":
                answer = result["qa_answer"]
            else:
                answer = result["pubmed_answer"]

            st.session_state.history.append((question, answer))

    # Chat display
    for q, a in reversed(st.session_state.history):

        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            st.markdown(a)
            st.markdown("---")



# Run app
if __name__ == "__main__":
    run_app()