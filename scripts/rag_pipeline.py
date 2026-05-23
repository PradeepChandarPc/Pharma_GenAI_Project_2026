from src.rag.rag_pipeline import load_indexes, build_retrievers, load_llm, build_rag_chain

def main():
    # 1. Load indexes
    model, papers_index, authors_index = load_indexes()

    # 2. Build retrievers
    papers_retriever, authors_retriever = build_retrievers(papers_index, authors_index)

    # 3. Load local LLM (Ollama)
    llm = load_llm()

    # 4. Build RAG chains
    papers_qa = build_rag_chain(llm, papers_retriever)
    authors_qa = build_rag_chain(llm, authors_retriever)

    # 5. Run sample queries
    print("📄 Papers QA:")
    print(papers_qa.run("What are the latest therapies for Type 2 diabetes?"))

    print("\n👩‍🔬 Authors QA:")
    print(authors_qa.run("Which authors are publishing on immunotherapy?"))

if __name__ == "__main__":
    main()
