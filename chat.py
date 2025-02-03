import os
import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  

# Configuration
llm_model = "llama3.2"
base_url = "http://localhost:11434" 
chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))

class ChromaDBEmbeddingFunction:
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return self.langchain_embeddings.embed_documents(input)

embedding = ChromaDBEmbeddingFunction(
    OllamaEmbeddings(model=llm_model, base_url=base_url)
)

collection_name = "rag_collection_demo"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "RAG collection for documents"},
    embedding_function=embedding
)

def add_documents_to_collection(documents, ids):
    collection.add(documents=documents, ids=ids)

def query_chromadb(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"]

def query_ollama(prompt):
    llm = OllamaLLM(model=llm_model, base_url=base_url)
    return llm.invoke(prompt)

def rag_pipeline(query_text):
    retrieved_docs = query_chromadb(query_text)
    context = " ".join(doc for docs in retrieved_docs for doc in docs) if retrieved_docs else ""

    prompt = f"{context} {query_text}" if context else query_text
    return query_ollama(prompt)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def read_pdf(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def main():
    st.title("Interactive RAG Chatbot")

    model = st.sidebar.selectbox("Choose a model", ["llama3.2"])

    st.sidebar.header("Upload Documents")
    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "txt":
                content = uploaded_file.read().decode("utf-8")
            elif file_extension == "pdf":
                content = read_pdf(uploaded_file)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_text(content)

            chunk_ids = [f"{uploaded_file.name}_chunk_{i}" for i in range(len(chunks))]
            add_documents_to_collection(chunks, chunk_ids)

        st.sidebar.success(f"Uploaded and processed {len(uploaded_files)} file(s).")
    
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
