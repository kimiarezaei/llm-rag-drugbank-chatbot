import os
import json
from datasets import load_dataset
from config import settings
from utils.logger import get_logger


CACHE_FILE = settings.cache_file
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

logger = get_logger(__name__)
def load_data():

    # If cached, load locally
    if os.path.exists(CACHE_FILE):
        logger.info("Loading dataset from cache...")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    logger.info("Downloading dataset from Hugging Face...")

    dataset = load_dataset(
        "Oduwo/drugbank-clean",
        token=settings.hf_token if settings.hf_token else None
    )

    train = dataset["train"]  

    docs = [row["output"] for row in train]

    # Save cache
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f)

    return docs