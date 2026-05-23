from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA





def load_indexes():
    model = SentenceTransformer("NeuML/pubmedbert-base-embeddings")
    papers_index = FAISS.load_local("data/vector_store/papers_index", model.encode,allow_dangerous_deserialization=True)
    authors_index = FAISS.load_local("data/vector_store/authors_index", model.encode,allow_dangerous_deserialization=True)
    return model, papers_index, authors_index

def build_retrievers(papers_index, authors_index):
    papers_retriever = papers_index.as_retriever(search_type="similarity", search_kwargs={"k":3})
    authors_retriever = authors_index.as_retriever(search_type="similarity", search_kwargs={"k":3})
    return papers_retriever, authors_retriever

def load_llm():
    # Local Ollama model
    return Ollama(model="llama3.2")   # or "mistral", "gemma", etc.

def build_rag_chain(llm, retriever):
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")


