# 💊 DrugBank QA Chatbot (RAG + Claude Sonnet)

A Retrieval-Augmented Generation (RAG) application for biomedical question answering using the DrugBank dataset. The system retrieves relevant scientific information through semantic search with ChromaDB and generates grounded responses using Anthropic Claude Sonnet.

**Example questions:**

* What are the toxic effects or overdose risks of Lepirudin?
* Give me an overview of the drug Etanercept.

**Live Demo:** https://drugbank-chatbot.streamlit.app

---

## Preview

![App Screenshot](images/app-screenshot.png)

---

## Tech Stack

* **Language:** Python 3.11
* **LLM:** Anthropic Claude Sonnet
* **Vector Database:** ChromaDB
* **Embeddings:** Sentence Transformers
* **Dataset:** Hugging Face DrugBank Dataset
* **Interface:** Streamlit
* **Configuration:** Pydantic Settings
* **Deployment:** Docker + Streamlit Cloud

---

## How It Works

This project implements a Retrieval-Augmented Generation (RAG) pipeline:

1. Loads the DrugBank dataset from **Hugging Face** with local caching for faster startup.
2. Manages application configuration using **Pydantic Settings**.
3. Splits documents into chunks and generates embeddings using **Sentence Transformers**.
4. Stores embeddings in **ChromaDB** for semantic retrieval.
5. Retrieves relevant context for each user query.
6. Generates grounded responses using **Anthropic Claude Sonnet**.
7. Provides an interactive chatbot interface with **Streamlit**.

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
