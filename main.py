import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz
import tempfile

# Constants
LLM_MODEL = "llama3.2"
BASE_URL = "http://localhost:11434"

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))

# ChromaDB embedding function
class ChromaDBEmbeddingFunction:
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        elif not isinstance(input, list):
            raise ValueError("Input to the embedding function must be a string or a list of strings.")
        return self.langchain_embeddings.embed_documents(input)

# Initialize Ollama embeddings
embedding = ChromaDBEmbeddingFunction(
    langchain_embeddings=OllamaEmbeddings(model=LLM_MODEL, base_url=BASE_URL)
)

# Create or get ChromaDB collection
collection_name = "rag_collection_demo"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "RAG collection for documents"},
    embedding_function=embedding
)

# Function to add documents to ChromaDB collection
def add_documents_to_collection(documents, ids):
    if not documents or not ids:
        raise ValueError("Documents or IDs are empty, cannot add to collection")
    collection.add(documents=documents, ids=ids)

# Function to read PDF files
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

# Function to read HTML content from URL
def read_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="content")
    return content.get_text() if content else ""

# Function to process and add documents to ChromaDB collection
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

# Function to perform RAG pipeline for query processing
def rag_pipeline(query_text):
    retrieved_docs = query_chromadb(query_text)
    context = " ".join(doc for docs in retrieved_docs for doc in docs) if retrieved_docs else ""
    prompt = f"{context} {query_text}" if context else query_text
    return query_ollama(prompt)

# Function to query ChromaDB for documents
def query_chromadb(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"]

# Function to query Ollama for response generation
def query_ollama(prompt):
    llm = OllamaLLM(model=LLM_MODEL, base_url=BASE_URL)
    return llm.invoke(prompt)

# Initialize Streamlit app
if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("Interactive AI Assistant")

    model = st.sidebar.selectbox("Choose a model", [LLM_MODEL])

    st.sidebar.header("Upload Documents or Provide URL")
    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True
    )
    url = st.sidebar.text_input("Enter URL to HTML version of document")

    # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "txt":
                content = uploaded_file.read().decode("utf-8")
            elif file_extension == "pdf":
                content = read_pdf(uploaded_file)

            process_and_add_documents(content, file_name_prefix=uploaded_file.name)

        st.sidebar.success(f"Uploaded and processed {len(uploaded_files)} file(s).")

    # Process URL input
    if url:
        content = read_html(url)
        process_and_add_documents(content, file_name_prefix="html_version")

    # Handle user input queries
    prompt = st.chat_input("Ask your question(s):")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.container():
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Assistant is typing..."):
                    # Multi-query support: process each question separately
                    prompts = prompt.split(";")  # Assuming questions are separated by ";"
                    response_messages = []
                    for q in prompts:
                        q = q.strip()  # Clean up any extra spaces
                        if q:
                            response_message = rag_pipeline(q)
                            response_messages.append(response_message)
                            st.session_state.messages.append({"role": "assistant", "content": response_message})

                    st.write(response_messages)

if __name__ == "__main__":
    main()
