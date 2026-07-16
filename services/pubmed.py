import requests

from utils.logger import get_logger


logger = get_logger(__name__)


def search_pubmed(drug_name: str, main_topic: str, main_topic_synonyms: list, max_results: int = 3) -> str:
    """
    Search PubMed for papers related to the drug mentioned.
    Returns up to `max_results` PubMed URLs.
    """

    logger.info("Searching PubMed for %s", drug_name)

    # pubmed search API endpoint
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # parameters for the API request
    topic_terms = " OR ".join(
    [f'"{main_topic}"'] + [f'"{s}"' for s in main_topic_synonyms]
    )

    term = f'"{drug_name}" AND ({topic_terms})'

    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": max_results,
        "sort": "relevance"
        }
    
    # Make the API request to PubMed
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.exception("PubMed API request failed")
        return f"Error searching PubMed: {e}"

    # Extract PubMed IDs from the response
    ids = response.json().get("esearchresult", {}).get("idlist", [])

    if not ids:
        logger.warning("No PubMed results found for %s", drug_name)
        return f"No PubMed results found for {drug_name}"

    logger.info("Found PubMed results for %s: %s", drug_name, ids)
    
    return (
    f"**{drug_name}** was not found in the dataset.\n\n"
    "You may want to check these PubMed publications:\n\n"
    + "\n".join(
        f"- [PubMed PMID {pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)"
        for pmid in ids
    )
)