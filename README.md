# DrugBank QA Chat

A Streamlit-based question answering app for DrugBank content. The app uses retrieval-augmented generation (RAG): it loads DrugBank documents, builds a persistent ChromaDB index, retrieves relevant chunks, and asks Anthropic Claude to generate a concise answer from the retrieved context.

## Features

- Chat-style question and answer interface built with Streamlit
- RAG pipeline using ChromaDB for retrieval
- Cached dataset loading to avoid repeated downloads
- Persistent vector store so the index can be reused between runs
- Optional command-line script for quick local testing

## App Screenshot

Add your screenshot here before publishing to GitHub:

![DrugBank QA Chat screenshot](images/app-screenshot.png)

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Anthropic Claude
- Hugging Face Datasets
- Pydantic Settings

## Project Structure

- `app.py` - Streamlit UI entrypoint
- `main.py` - simple command-line runner
- `config.py` - environment and app settings
- `data_cache.py` - dataset download and local caching
- `services/retrieval.py` - ChromaDB indexing and search
- `services/qa.py` - RAG prompt and answer generation
- `services/llm.py` - Anthropic API wrapper
- `utils/logger.py` - logging setup
- `cache/` - cached dataset file
- `chromadb/` - persistent vector database
- `logs/` - application logs

## Requirements

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with:

```env
anthropic_api_key=your_anthropic_api_key
hf_token=your_hugging_face_token
```

`hf_token` is optional, but it may be needed if the dataset requires authentication.

## Run Locally

Start the Streamlit app with:

```bash
streamlit run app.py
```

If you want to test the command-line version:

```bash
python main.py
```

## How It Works

1. The app loads DrugBank text data from the local cache, or downloads it from Hugging Face if the cache is empty.
2. The documents are split into chunks and stored in a persistent ChromaDB collection.
3. When you ask a question, the app retrieves the most relevant chunks.
4. Claude generates an answer using only the retrieved context.

## Deploy on Streamlit Cloud

1. Push this project to GitHub.
2. Make sure `app.py` is the Streamlit entrypoint.
3. In Streamlit Cloud, select the repository and branch.
4. Set the secret values for:
   - `anthropic_api_key`
   - `hf_token` if needed
5. Deploy the app.

If your Streamlit Cloud app cannot read a local `.env` file, add the same values in the app's deployment secrets or environment settings.

## Notes

- The first launch may take longer because the dataset and Chroma index need to be created.
- The folders `cache/`, `chromadb/`, and `logs/` are generated at runtime and do not need to be edited manually.
- You can replace the screenshot path in this README with your own image after adding it to the repository.
