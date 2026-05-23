import streamlit as st
from src.rag.rag import load_indexes, build_retrievers, load_llm, build_rag_chain

# App title
st.title("Pharma GenAI Assistant")

# Load indexes, retrievers, and LLM once
@st.cache_resource
def init_pipeline():
    model, papers_index, authors_index = load_indexes()
    papers_retriever, authors_retriever = build_retrievers(papers_index, authors_index)
    llm = load_llm()
    papers_qa = build_rag_chain(llm, papers_retriever)
    authors_qa = build_rag_chain(llm, authors_retriever)
    return papers_qa, authors_qa

papers_qa, authors_qa = init_pipeline()

# User input
query = st.text_input("Enter your biomedical question:")

# Dropdown to choose retriever
retriever_choice = st.selectbox("Choose source:", ["Papers", "Authors"])

# Run query
if query:
    if retriever_choice == "Papers":
        answer = papers_qa.run(query)
    else:
        answer = authors_qa.run(query)

    st.subheader("Answer")
    st.write(answer)
