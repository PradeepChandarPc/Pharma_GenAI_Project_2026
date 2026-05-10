import pandas as pd
import requests
import time
from tqdm import tqdm

def get_citation_count(doi: str):
    """
    Fetch citation count from OpenAlex API using DOI.
    """
    if not doi or pd.isna(doi):
        return None
    try:
        doi = doi.strip()
        url = f"https://api.openalex.org/works/https://doi.org/{doi}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("cited_by_count", 0)
        return None
    except Exception as e:
        print("Citation error:", e)
        return None


def extract_papers(papers_data, enrich_citations: bool = True):
    """
    Extract paper metadata (title, abstract, journal, year, doi, citation_count).
    """
    papers = []
    #for article in papers_data["PubmedArticle"]:
    for article in tqdm(papers_data["PubmedArticle"], desc="Parsing papers"):
        try:
            article_data = article["MedlineCitation"]["Article"]
            pmid = str(article["MedlineCitation"]["PMID"])
            title = article_data.get("ArticleTitle", "")
            abstract = " ".join(article_data.get("Abstract", {}).get("AbstractText", []))
            journal = article_data["Journal"]["Title"]
            pub_date = article_data["Journal"]["JournalIssue"]["PubDate"]
            year = pub_date.get("Year", "Unknown")

            # Extract DOI
            doi = ""
            for article_id in article["PubmedData"]["ArticleIdList"]:
                if article_id.attributes["IdType"] == "doi":
                    doi = str(article_id)

            # Citation count
            citation_count = None
            if enrich_citations and doi:
                citation_count = get_citation_count(doi)
                time.sleep(1)  # avoid API rate limits

            papers.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "year": year,
                "doi": doi,
                "citation_count": citation_count
            })
        except Exception as e:
            print("Paper parsing error:", e)

    return pd.DataFrame(papers)


def extract_authors(papers_data):
    """
    Extract author metadata (name, role, affiliation).
    """
    authors_data = []
    for article in papers_data["PubmedArticle"]:
        try:
            article_data = article["MedlineCitation"]["Article"]
            pmid = str(article["MedlineCitation"]["PMID"])
            title = article_data.get("ArticleTitle", "")
            journal = article_data["Journal"]["Title"]
            pub_date = article_data["Journal"]["JournalIssue"]["PubDate"]
            year = pub_date.get("Year", "Unknown")

            authors_list = article_data.get("AuthorList", [])
            total_authors = len(authors_list)

            for idx, author in enumerate(authors_list):
                last_name = author.get("LastName", "")
                fore_name = author.get("ForeName", "")
                full_name = f"{fore_name} {last_name}".strip()

                affiliation = ""
                if "AffiliationInfo" in author and len(author["AffiliationInfo"]) > 0:
                    affiliation = author["AffiliationInfo"][0].get("Affiliation", "")

                # Author role
                if idx == 0:
                    role = "Primary Author"
                elif idx == total_authors - 1:
                    role = "Senior Author"
                else:
                    role = "Secondary Author"

                citation = f"{full_name} et al. ({year})"

                authors_data.append({
                    "pmid": pmid,
                    "title": title,
                    "author_order": idx + 1,
                    "author_name": full_name,
                    "role": role,
                    "affiliation": affiliation,
                    "journal": journal,
                    "year": year,
                    "citation": citation
                })
        except Exception as e:
            print("Author parsing error:", e)

    return pd.DataFrame(authors_data)
