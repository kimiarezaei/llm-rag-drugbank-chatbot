import chromadb
from utils.logger import get_logger
from chromadb.utils import embedding_functions
from config import settings


logger = get_logger(__name__)

# Initialize embedding function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=settings.embedding_model_name
)

# Persistant ChromaDB client
client = chromadb.PersistentClient(path=settings.chroma_path)

collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

# Chunking
def chunk_document(text: str) -> list[str]:
    return [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

# Build index
def build_index(documents: list[str], batch_size: int = 100, force_rebuild: bool = False):
    if collection.count() > 0 and not force_rebuild:
        logger.info("Index already exists. Skipping rebuild.")
        return


    logger.info("Building ChromaDB index...")

    all_chunks = []
    all_ids = []

    # Split document into chunks
    for doc_id, doc in enumerate(documents):
        chunks = chunk_document(doc)

        # Create chunk IDs and collect data
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{doc_id}_{i}")
    
    # Batch insert into ChromaDB
    for i in range(0, len(all_chunks), batch_size):
        # Store in ChromaDB
        collection.add(
            documents=all_chunks[i:i+batch_size],
            ids=all_ids[i:i+batch_size]
        )
    logger.info(f"Index built with {len(all_chunks)} chunks.")

# Search
def search(query: str, k: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results.get("documents", [[]])[0]