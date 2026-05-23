import os
import pandas as pd

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ==========================================
# Load Data
# ==========================================

papers_df = pd.read_excel(
    "data/processed/pubmed_papers.xlsx"
)

authors_df = pd.read_excel(
    "data/processed/pubmed_authors.xlsx"
)

# ==========================================
# Initialize Biomedical Embedding Model
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="NeuML/pubmedbert-base-embeddings"
)

# ==========================================
# Build Paper Embeddings
# ==========================================

def build_paper_embeddings():

    print("🔎 Building paper embeddings...")

    # Embedding text
    texts = (
        papers_df["title"].fillna("") + " " +
        papers_df["abstract"].fillna("")
    ).tolist()

    # Metadata
    metadata = [
        {
            "pmid": row.get("pmid", ""),
            "title": row.get("title", ""),
            "journal": row.get("journal", ""),
            "year": row.get("year", ""),
            "doi": row.get("doi", ""),
            "citation_count": row.get("citation_count", 0)
        }
        for _, row in papers_df.iterrows()
    ]

    # Create FAISS vector store
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadata
    )

    # Save locally
    vector_store.save_local(
        "data/vector_store/papers_index"
    )

    print("✅ Paper embeddings saved.")


# ==========================================
# Build Author Embeddings
# ==========================================

def build_author_embeddings():

    print("👩‍🔬 Building author embeddings...")

    # Better semantic representation of expertise
    texts = (
        authors_df["author_name"].fillna("") + " " +
        authors_df["affiliation"].fillna("") + " " +
        authors_df["title"].fillna("")
    ).tolist()

    # Metadata
    metadata = [
        {
            "pmid": row.get("pmid", ""),
            "author_name": row.get("author_name", ""),
            "author_order": row.get("author_order", ""),
            "role": row.get("role", ""),
            "affiliation": row.get("affiliation", ""),
            "journal": row.get("journal", ""),
            "year": row.get("year", ""),
            "citation": row.get("citation", 0)
        }
        for _, row in authors_df.iterrows()
    ]

    # Create FAISS vector store
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadata
    )

    # Save locally
    vector_store.save_local(
        "data/vector_store/authors_index"
    )

    print("✅ Author embeddings saved.")


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    os.makedirs(
        "data/vector_store",
        exist_ok=True
    )

    build_paper_embeddings()
    build_author_embeddings()

    print("🎉 Embedding build complete.")