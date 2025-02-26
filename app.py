<<<<<<< HEAD
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
=======
import streamlit as st
import logging
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import numpy as np
import chardet
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

# Подключение к базе данных MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["rag_db"]
collection = mongo_db["documents"]

class EmbeddingFunction:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def call(self, input):
        if isinstance(input, str):
            input = [input]
        vectors = self.model.encode(input)
        if len(vectors) == 0:
            raise ValueError("Empty embedding generated.")
        return vectors


embedding = EmbeddingFunction("paraphrase-multilingual-MiniLM-L12-v2")


def add_document_to_mongodb(documents, ids):
    try:
        for doc, doc_id in zip(documents, ids):
            if not doc.strip():
                raise ValueError("Cannot add an empty or whitespace-only document.")

            embedding_vector = embedding.call(doc)

            logging.info(f"Generated embedding for document '{doc}': {embedding_vector}")

            collection.insert_one({
                "_id": doc_id,
                "document": doc,
                "embedding": embedding_vector[0].tolist()
            })
    except Exception as e:
        logging.error(f"Error adding document: {e}")
        raise

def query_documents_from_mongodb(query_text, n_results=1):
    try:
        query_embedding = embedding(query_text)[0]
        docs = collection.find()

        similarities = []
        for doc in docs:
            doc_embedding = np.array(doc["embedding"])
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, doc))

        top_results = sorted(similarities, key=lambda x: x[0], reverse=True)[:n_results]
        return [doc["document"] for _, doc in top_results]
    except Exception as e:
        logging.error(f"Error querying documents: {e}")
        return []

def query_with_ollama(prompt, model_name):
    try:
        logging.info(f"Sending prompt to Ollama with model {model_name}: {prompt}")
        llm = OllamaLLM(model=model_name)
        response = llm.invoke(prompt)
        logging.info(f"Ollama response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error with Ollama query: {e}")
        return f"Error with Ollama API: {e}"

def retrieve_and_answer(query_text, model_name):
    retrieved_docs = query_documents_from_mongodb(query_text)
    context = " ".join(retrieved_docs) if retrieved_docs else "No relevant documents found."

    augmented_prompt = f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"
    return query_with_ollama(augmented_prompt, model_name)

# Функция для извлечения текста с сайта Конституции Республики Казахстан
def get_constitution_text():
    url = "https://www.akorda.kz/en/constitution-of-the-republic-of-kazakhstan-50912"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        constitution_text = ""
        for paragraph in soup.find_all("p"):
            constitution_text += paragraph.get_text() + "\n"
        logging.info(f"Extracted Constitution text: {constitution_text[:500]}...")  # Покажем первые 500 символов
        return constitution_text       
    else:
        logging.error("Error fetching the Constitution text from the website.")
        return "Error fetching the Constitution text from the website."

# === Multiquery and RAG Fusion Functions ===
def generate_alternative_queries(question, model, num_queries=5):
    """
    Generate alternative queries from the original question using Ollama.
    """
    prompt = (
        f"You are an AI language model assistant. Your task is to generate {num_queries} different "
        f"versions of the given user question to retrieve relevant documents from a vector database. "
        f"By generating multiple perspectives on the user question, your goal is to help the user overcome "
        f"some of the limitations of the distance-based similarity search. Provide these alternative questions "
        f"separated by newlines.\nOriginal question: {question}"
    )
    response = query_with_ollama(prompt, model)
    alternative_queries = [q.strip() for q in response.split("\n") if q.strip()]
    return alternative_queries

def reciprocal_rank_fusion(results, k=60):
    """
    Perform Reciprocal Rank Fusion (RRF) on lists of retrieved documents.
    Each element in 'results' is a list of documents (strings) retrieved for an alternative query.
    """
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            fused_scores[doc] += 1 / (rank + k)
    # Sort documents by fused score in descending order
    fused_results = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return fused_results

def multiquery_rag_fusion(query, model, num_alternatives=5, n_results=3, k=60):
    """
    Generate alternative queries, retrieve documents for each, and apply RRF to fuse results.
    Returns a list of tuples (document, fused_score).
    """
    alternative_queries = generate_alternative_queries(query, model, num_alternatives)
    logging.info(f"Alternative queries: {alternative_queries}")
    all_results = []
    for alt_query in alternative_queries:
        docs = query_documents_from_mongodb(alt_query, n_results)
        all_results.append(docs)
    logging.info(f"Retrieved documents for alternative queries: {all_results}")
    fused_results = reciprocal_rank_fusion(all_results, k)
    return fused_results

def final_rag_fusion_answer(query, model, num_alternatives=5, n_results=3, k=60):
    """
    Get final answer using RAG Fusion: fuse retrieved documents and generate an answer with context.
    """
    fused_results = multiquery_rag_fusion(query, model, num_alternatives, n_results, k)
    if fused_results:
        # Use top 3 fused documents as context (adjust as needed)
        top_docs = [doc for doc, score in fused_results[:3]]
        context = " ".join(top_docs)
    else:
        context = "No relevant documents found."
    augmented_prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    answer = query_with_ollama(augmented_prompt, model)
    return answer

# === Streamlit UI ===

st.title("Chat with Ollama")

# Define your model (this is used by both query_with_ollama and the multiquery functions)
model = "llama3.2:1b"

# Update the sidebar options to include the new multiquery/RAG Fusion option
menu_options = [
    "Show Documents in MongoDB", 
    "Add New Document to MongoDB as Vector", 
    "Upload File and Ask Question", 
    "Ask Ollama a Question", 
    "Ask Question About Constitution",
    "Ask Multiquery & RAG Fusion Question"
]
menu = st.sidebar.selectbox("Choose an action", menu_options)

if menu == "Show Documents in MongoDB":
    st.subheader("Stored Documents in MongoDB")
    documents = collection.find()
    if documents:
        for i, doc in enumerate(documents, start=1):
            st.write(f"{i}. {doc['document']}")
    else:
        st.write("No data available!")

elif menu == "Add New Document to MongoDB as Vector":
    st.subheader("Add a New Document to MongoDB")
    new_doc = st.text_area("Enter the new document:")
    uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
    
if st.button("Add Document"):
        if uploaded_file is not None:
            try:
                file_bytes = uploaded_file.read()
                detected_encoding = chardet.detect(file_bytes)['encoding']
                if not detected_encoding:
                    raise ValueError("Failed to detect file encoding.")
                file_content = file_bytes.decode(detected_encoding)

                doc_id = f"doc{collection.count_documents({}) + 1}"
                st.write(f"Adding document from file: {uploaded_file.name}")
                add_document_to_mongodb([file_content], [doc_id])
                st.success(f"Document added successfully with ID {doc_id}")
            except Exception as e:
                st.error(f"Failed to add document: {e}")
        elif new_doc.strip(): 
            try:
                doc_id = f"doc{collection.count_documents({}) + 1}"
                st.write(f"Adding document: {new_doc}")
                add_document_to_mongodb([new_doc], [doc_id])
                st.success(f"Document added successfully with ID {doc_id}")
            except Exception as e:
                st.error(f"Failed to add document: {e}")
        else:
            st.warning("Please enter a non-empty document or upload a file before adding.")

elif menu == "Upload File and Ask Question":
    st.subheader("Upload a file and ask a question about its content")
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.read()
            detected_encoding = chardet.detect(file_bytes)['encoding']
            if not detected_encoding:
                raise ValueError("Failed to detect file encoding.")
            file_content = file_bytes.decode(detected_encoding)

            st.write("File content successfully loaded:")
            st.text_area("File Content", file_content, height=200)

            question = st.text_input("Ask a question about this file's content:")
            if question:
                response = query_with_ollama(f"Context: {file_content}\n\nQuestion: {question}\nAnswer:", model)
                st.write("Response:", response)

        except Exception as e:
            st.error(f"Failed to process the file: {e}")

elif menu == "Ask Ollama a Question":
    query = st.text_input("Ask a question")
    if query:
        response = retrieve_and_answer(query, model)
        st.write("Response:", response)

elif menu == "Ask Question About Constitution":
    question = st.text_input("Ask a question about the Constitution of Kazakhstan")
    if question:
        try:
            # Извлекаем текст с сайта Конституции
            constitution_text = get_constitution_text()
            if constitution_text:
                # Ограничиваем объем текста для передачи в модель (например, первые 2000 символов)
                context = constitution_text[:2000]  # Ограничение на первые 2000 символов
                logging.info(f"Constitution text: {context[:500]}...")  # Отладочный вывод

                # Формируем запрос к Ollama
                augmented_prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
                response = query_with_ollama(augmented_prompt, model)

                # Выводим ответ от Ollama и краткий текст Конституции
                st.write("Constitution Text (Extract):")
                st.text_area("Constitution Text", context, height=200)
                st.write("Response from Ollama:", response)

                # Генерация краткого текста
                summary_prompt = f"Summarize the following content: {context}"
                summary = query_with_ollama(summary_prompt, model)
                st.write("Summary of the Constitution Text:", summary)
            else:
                st.write("Failed to fetch Constitution text.")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            st.write("An error occurred while processing the request.")
            
elif menu == "Ask Multiquery & RAG Fusion Question":
    st.subheader("Ask a question using Multiquery and RAG Fusion")
    query = st.text_input("Enter your question:")
    if query:
        # The final_rag_fusion_answer function will:
        # 1. Generate alternative queries.
        # 2. Retrieve documents for each alternative query.
        # 3. Fuse the results via reciprocal rank fusion.
        # 4. Build an augmented prompt for the final answer.
        response = final_rag_fusion_answer(query, model)
        st.write("Response:", response)
        
        
>>>>>>> cb9e6c2 (MULTI-QUERY & Rag Fusion)
