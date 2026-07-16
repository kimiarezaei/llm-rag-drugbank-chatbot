# 💊 DrugBank QA Agent (LLM-powered RAG + PubMed Search using LangGraph)

A Retrieval-Augmented Generation (RAG) application for biomedical question answering using the DrugBank dataset. The system retrieves relevant scientific information through semantic search with ChromaDB and generates grounded responses using Anthropic Claude Sonnet. If the requested drug information is not available in the DrugBank dataset, the application automatically searches **PubMed** and recommends relevant scientific publications.

**Example questions:**

- What are the toxic effects or overdose risks of Lepirudin?
- Give me an overview of the drug Etanercept.
- Is Ozempic useful for weight loss?


**Live Demo:** https://drugbank-chatbot.streamlit.app

---

## Preview

![App Screenshot](images/app-screenshot.png)

---

## Tech Stack

- **Language:** Python 3.11
- **Framework:** LangGraph
- **LLM:** Anthropic Claude Sonnet
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Dataset:** Hugging Face DrugBank Dataset
- **External API:** PubMed E-Utilities API
- **Interface:** Streamlit
- **Configuration:** Pydantic Settings
- **Deployment:** Docker + Streamlit Cloud

---

## How It Works

This project implements a Retrieval-Augmented Generation (RAG) pipeline and fallback workflow:

1. Loads the DrugBank dataset from **Hugging Face** with local caching.
2. Splits documents into chunks and generates embeddings using **Sentence Transformers**.
3. Stores embeddings in **ChromaDB** for semantic retrieval.
4. Uses **LangGraph** to orchestrate the application workflow.
5. Extracts the drug name and research topic from the user's question.
6. Searches the DrugBank knowledge base for relevant information.
7. If relevant information is found, **Claude Sonnet** generates a grounded response.
8. If no matching DrugBank entry is found, the application automatically searches **PubMed** for relevant scientific publications.
9. Presents either the DrugBank answer or links to relevant PubMed papers through the **Streamlit interface**.


---
## Project Workflow

```text
User Question
      │
      ▼
Extract Drug & Topic
      │
      ▼
Search DrugBank (ChromaDB)
      │
      ├── Match found
      │      ▼
      │   Generate Answer (Claude)
      │
      └── No match
             ▼
      Search PubMed
             ▼
      Return Relevant Publications
```

---

## How to Run

### Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Docker

```bash
docker build -t drugbank-chatbot .
docker run -p 8501:8501 --env-file .env drugbank-chatbot
```
