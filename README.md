# Interactive AI Assistant for the Constitution of Kazakhstan

## Project Overview
LlamaChat is an interactive Retrieval-Augmented Generation (RAG) chatbot designed to provide contextual answers based on uploaded documents, particularly focusing on the **Constitution of Kazakhstan**. This AI-powered assistant leverages advanced language models to process legal texts, making it an invaluable tool for understanding constitutional law, answering detailed questions, and assisting with legal research. Users can upload .txt files containing the Constitution of Kazakhstan or similar legal documents, and the chatbot will provide answers based on the content. 

Built using Streamlit for the frontend, Ollama for model embeddings, and ChromaDB for data storage, LlamaChat offers a seamless and intuitive interface for real-time, document-based question answering.

## Key Features
- **Document Upload**: Easily upload the **Constitution of Kazakhstan** (or other legal documents) for in-depth interaction.
- **Contextual Question Answering**: Ask questions about the Constitution and receive precise, context-aware answers directly from the document.
- **Real-time Interaction**: Get instant, AI-generated responses, with relevant sections of the Constitution referenced in real-time.
- **Persistent Data Storage**: Document embeddings are stored in ChromaDB, ensuring fast and scalable retrieval for future queries without needing to reprocess the text.
- **Customizable Interface**: Users can select models and adjust settings to optimize the experience, depending on the complexity of the questions or the focus of the document.

## Technologies Used
- **Streamlit**: For building the user-friendly web interface.
- **Ollama**: For creating high-quality embeddings and generating model responses.
- **ChromaDB**: To store document embeddings persistently and facilitate efficient document retrieval.
- **Python**: Main programming language for backend logic.
- **SentenceTransformers**: For document embedding and vector-based similarity search.

## Installation

### Prerequisites
Ensure you have the following installed:
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
1. **Upload the Constitution of Kazakhstan**: Upload the full text of the **Constitution of Kazakhstan** (or other legal documents). The chatbot will process the content and store it for querying.
2. **Ask Questions**: Type any questions related to the Constitution or legal provisions. For example:
   - *"What are the key principles of the Republic of Kazakhstan?"*
   - *"What does Article 2 of the Constitution state about sovereignty?"*
   - *"How does the Constitution define the responsibilities of the President?"*
   - *"What is the legal basis for Kazakhstan's independence?"*
3. **Retrieve Contextual Information**: The chatbot will reference the uploaded Constitution to provide specific and accurate answers based on the relevant sections or articles.
4. **Persistent Storage**: All document embeddings are stored in ChromaDB, allowing future queries to be answered quickly without reprocessing the document every time.

## Focus on the Constitution of Kazakhstan
LlamaChat is particularly tailored for exploring and understanding the **Constitution of Kazakhstan**. The chatbot can:
- Analyze and interpret articles, clauses, and provisions of the Constitution.
- Provide detailed responses about the legal and historical context of specific articles.
- Assist legal professionals, students, and educators in answering questions related to constitutional law in Kazakhstan.
- Offer insights into Kazakhstan’s governance, legal structure, and key principles such as sovereignty, independence, and the rule of law.

This makes LlamaChat an essential tool for anyone needing detailed, real-time legal information from the **Constitution of Kazakhstan**.

## Configuration
You can customize the following settings:
- **Model**: Choose from available AI models, such as Llama 3.2, to optimize the chatbot’s ability to process and answer constitutional queries.
- **Storage**: Adjust the database path if necessary (SQLite by default via ChromaDB).

## Contribution
We welcome contributions to enhance this project! To contribute:
1. **Fork the Repository**: Create a copy of the repository to work on your changes.
2. **Create a Feature Branch**: Use a descriptive branch name for your changes.
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit Your Changes**: Provide clear, concise commit messages.
   ```bash
   git commit -m "Added feature to analyze constitutional law"
   ```
4. **Push Changes**:
   ```bash
   git push origin feature/your-feature
   ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Special thanks to the following tools that made this project possible:
- **Streamlit** for the easy-to-use web interface.
- **ChromaDB** for persistent and scalable data storage.
- **Ollama** for providing powerful AI embeddings and language model support.
- **SentenceTransformers** for efficient document embedding and similarity searching.

---

