import os
import pandas as pd
from src.ingestion.pubmedloader import fetch_pubmed_data
from src.ingestion.parser import extract_papers, extract_authors
from src.ingestion.cleaner import remove_empty_abstracts, remove_duplicates

def run_ingestion(query="diabetes treatment", max_results=200):
    papers_data = fetch_pubmed_data(query, max_results=max_results)
    papers_df = extract_papers(papers_data)
    authors_df = extract_authors(papers_data)

    papers_df = remove_empty_abstracts(papers_df)
    papers_df = remove_duplicates(papers_df)

    os.makedirs("data/processed", exist_ok=True)
    papers_df.to_excel("data/processed/pubmed_papers.xlsx", index=False)
    authors_df.to_excel("data/processed/pubmed_authors.xlsx", index=False)

    print("Ingestion complete. Files saved in data/processed/")

if __name__ == "__main__":
    run_ingestion()
