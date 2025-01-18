import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz
from io import BytesIO
import tempfile

# Constants
LLM_MODEL = "llama3.2"
BASE_URL = "http://localhost:11434"

chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))

class ChromaDBEmbeddingFunction:
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        elif not isinstance(input, list):
            raise ValueError("Input to the embedding function must be a string or a list of strings.")
        return self.langchain_embeddings.embed_documents(input)

embedding = ChromaDBEmbeddingFunction(
    langchain_embeddings=OllamaEmbeddings(model=LLM_MODEL, base_url=BASE_URL)
)

collection_name = "rag_collection_demo"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "RAG collection for documents"},
    embedding_function=embedding
)

def add_documents_to_collection(documents, ids):
    if not documents or not ids:
        raise ValueError("Documents or IDs are empty, cannot add to collection")
    collection.add(documents=documents, ids=ids)

def read_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name

    try:
        doc = fitz.open(tmp_file_path)
        text = ""
        for page in doc:
            text += page.get_text()
    finally:
        doc.close()
        os.remove(tmp_file_path)
    return text

def read_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="content")
    return content.get_text() if content else ""

def process_and_add_documents(content, file_name_prefix=""):
    if not content:
        print(f"Warning: Content from {file_name_prefix} is empty. Skipping processing.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(content)

    if not chunks:
        print(f"No chunks found in the content of {file_name_prefix}")
    else:
        print(f"Splitting content into {len(chunks)} chunks for {file_name_prefix}.")

    chunk_ids = [f"{file_name_prefix}_chunk_{i}" for i in range(len(chunks))]

    if not chunks or not chunk_ids:
        print(f"Warning: No valid chunks or chunk IDs for {file_name_prefix}. Skipping add to collection.")
        return

    add_documents_to_collection(chunks, chunk_ids)

def rag_pipeline(query_text):
    retrieved_docs = query_chromadb(query_text)
    context = " ".join(doc for docs in retrieved_docs for doc in docs) if retrieved_docs else ""
    prompt = f"{context} {query_text}" if context else query_text
    return query_ollama(prompt)

def query_chromadb(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"]

def query_ollama(prompt):
    llm = OllamaLLM(model=LLM_MODEL, base_url=BASE_URL)
    return llm.invoke(prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("Interactive AI Assistant for the Constitution of Kazakhstan")

    model = st.sidebar.selectbox("Choose a model", [LLM_MODEL])

    st.sidebar.header("Upload Documents or Provide URL")
    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True
    )
    url = st.sidebar.text_input("Enter URL to HTML version of Constitution")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "txt":
                content = uploaded_file.read().decode("utf-8")
            elif file_extension == "pdf":
                content = read_pdf(uploaded_file)

            process_and_add_documents(content, file_name_prefix=uploaded_file.name)

        st.sidebar.success(f"Uploaded and processed {len(uploaded_files)} file(s).")

    if url:
        content = read_html(url)
        process_and_add_documents(content, file_name_prefix="html_version")

    prompt = st.chat_input("Ask your question:")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.container():
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Assistant is typing..."):
                    response_message = rag_pipeline(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response_message})
                    st.write(response_message)

if __name__ == "__main__":
    main()
