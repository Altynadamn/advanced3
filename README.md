# Interactive AI Assistant for the Constitution of Kazakhstan

## Project Overview
LlamaChat is an interactive Retrieval-Augmented Generation (RAG) chatbot that leverages advanced language models to provide contextual responses based on uploaded documents. The app allows users to upload documents, such as .txt files, and query the chatbot for information within the documents. Built using Streamlit for the frontend, Ollama for model embeddings, and ChromaDB for data storage, LlamaChat offers a simple yet powerful interface for real-time question answering.

## Features
- **Document Upload**: Upload multiple .txt files, one at a time or in bulk, for the chatbot to process and reference.
- **Contextual Question Answering**: Ask questions related to the uploaded documents, and the chatbot generates answers based on the content.
- **Real-time Interaction**: Instant responses from the AI model as you interact with the chatbot.
- **Persistent Data Storage**: Embeddings of documents are stored in ChromaDB for efficient, scalable retrieval.
- **Customizable Interface**: Users can adjust the model and chat settings to enhance their experience.

## Technologies Used
- **Streamlit**: For creating an interactive frontend interface.
- **Ollama**: For embedding and generating model responses.
- **ChromaDB**: For persistent storage of document embeddings and fast retrieval.
- **Python**: Main programming language for backend logic.
- **SentenceTransformers**: For document embedding and vector-based similarity search.

## Installation

### Prerequisites
Before you begin, ensure that you have the following installed:
- Python 3.7+
- pip (Python package manager)

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Altynadamn/OllamaChat.git
   cd LlamaChat
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```
6. Open your browser and go to the URL shown in the terminal, usually `http://localhost:8501`.

## Usage
1. **Upload Documents**: Use the file upload option to upload .txt files containing content that you want to query the chatbot about. For example, you can upload the Constitution of Kazakhstan or any other legal or informational document.
2. **Choose a Model**: Select from the available AI models (e.g., Llama 3.2) to customize your experience.
3. **Ask Questions**: Type your queries in the chat input field. The chatbot will analyze your uploaded documents and provide relevant answers. For instance:
   - *"What are the key principles of the Republic of Kazakhstan?"*
   - *"What does Article 2 of the Constitution state about sovereignty?"*
4. **Retrieve Contextual Information**: The chatbot references the uploaded documents to ensure accurate and relevant responses.
5. **Persistent Storage**: Document embeddings are saved in ChromaDB, allowing efficient retrieval for subsequent queries without needing to reprocess the documents.

### About the Constitution of Kazakhstan
LlamaChat is particularly suited for analyzing complex documents like the Constitution of Kazakhstan. Users can upload the full text of the Constitution and:
- Explore articles and clauses in detail.
- Gain insights into legal and historical contexts.
- Ask questions about specific sections, such as:
  - "What are the responsibilities of the President?"
  - "How does the Constitution define the sovereignty of Kazakhstan?"

This makes LlamaChat an invaluable tool for legal professionals, educators, and students.

## Configuration
You can customize the following settings:
- **Model**: Choose the model you want to interact with (e.g., Llama 3.2).
- **Storage**: Adjust the database path if needed (SQLite is used by default via ChromaDB).

## Contribution
We welcome contributions to improve this project! If you want to make enhancements or fix bugs, please follow these guidelines:

1. **Fork the Repository**: Create a copy of the repository to work on your changes.
2. **Create a Feature Branch**: Use a descriptive name for the branch you're working on.
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit Your Changes**: Write clear commit messages.
   ```bash
   git commit -m "Added new feature"
   ```
4. **Push the Changes**:
   ```bash
   git push origin feature/your-feature
   ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Special thanks to the following tools that made this project possible:
- **Streamlit** for creating the user-friendly web interface.
- **ChromaDB** for scalable, persistent data storage.
- **Ollama** for providing high-quality embeddings and language model support.

