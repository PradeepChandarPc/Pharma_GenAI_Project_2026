from Bio import Entrez

# Configure your email (NCBI requires this)
Entrez.email = "your_email@example.com"

def fetch_pubmed_data(query: str, max_results: int = 20):
    """
    Fetch raw PubMed XML records for a given query.
    """
    # Search papers
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    search_results = Entrez.read(handle)
    handle.close()

    ids = search_results["IdList"]
    print(f"Found {len(ids)} papers")

    # Fetch paper details
    fetch_handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="xml")
    papers_data = Entrez.read(fetch_handle)
    fetch_handle.close()

    return papers_data
