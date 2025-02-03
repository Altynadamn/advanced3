---
# ChromaDB and RAG Fusion Chatbot Application

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Installation Instructions](#installation-instructions)
4. [How to Use](#how-to-use)
5. [File Breakdown](#file-breakdown)
6. [Technical Insights](#technical-insights)
7. [Sample Queries](#sample-queries)
8. [License](#license)

---

## Overview

This project builds on the **Assignment 3** chatbot, enhancing its functionality by implementing **Multi Query** and **RAG Fusion** techniques. The application utilizes **ChromaDB** for efficient document storage and retrieval, paired with the **Ollama llama3.2** model for generating precise answers. This setup allows the chatbot to process multiple queries simultaneously and retrieve the most relevant documents, resulting in more accurate and context-rich responses.

The app is designed with an intuitive **Streamlit** interface, allowing users to upload custom documents and interact with the assistant to get tailored answers based on the **Constitution of Kazakhstan** or other uploaded content.

---

## Key Features

- **Multi Query Expansion**: Automatically generates variations of user queries to capture a wider context and improve document retrieval.
- **RAG Fusion**: Combines relevant content from multiple sources to provide richer and more accurate answers.
- **Constitution Querying**: Preloads the full **Constitution of Kazakhstan** for accurate, legally grounded responses.
- **Custom Document Uploads**: Users can upload `.txt` files to enhance the range of topics the assistant can respond to.
- **Fast and Efficient Retrieval**: Leverages **ChromaDB** for vector-based document retrieval.
- **Streamlit Interface**: A clean and simple interface for querying, file uploads, and interacting with the assistant.

---

## Installation Instructions

### Prerequisites

Before starting, ensure the following are installed:

- Python 3.9 or later
- pip
- **Ollama server** (Make sure the Ollama server is running, and adjust the URL if necessary)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd <repository-name>
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the English version of the **Constitution of the Republic of Kazakhstan** and save it as `constitution.txt` in your project directory.

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

5. Open the application in your browser (Streamlit will provide a local URL).

---

## How to Use

1. **Multi Query Expansion for Constitution Queries**:

   - The assistant will automatically generate multiple versions of your query to expand the search space and retrieve more relevant documents.
   - Detailed answers will cite specific articles and sections of the Constitution.

2. **Custom Document Upload**:

   - Upload `.txt` files to extend the assistant's knowledge base. It will incorporate the content from these documents to respond to your queries.
   - The assistant will perform **RAG Fusion** to combine information from both the Constitution and the uploaded documents for a richer response.

3. **Interacting with the Assistant**:

   - Type your query in the provided text box, and the assistant will generate a response using the retrieved documents and the RAG pipeline.

---

## File Breakdown

1. **app.py** ([source](src/app.py)):  
   This is the main application file that implements the RAG Fusion pipeline, query processing, and Streamlit UI components.

2. **constitution.txt**:  
   Contains the full text of the **Constitution of the Republic of Kazakhstan**.

3. **requirements.txt** ([source](requirements.txt)):  
   Lists all the required Python libraries for the project.

4. **style.css** ([source](src/style.css)):  
   Custom styles for the Streamlit interface.

---

## Technical Insights

### Multi Query Expansion

The assistant generates multiple variations of a user’s query, allowing it to retrieve a wider range of relevant documents. This helps capture different phrasings and nuances in the user’s input, leading to a more thorough and precise response.

### RAG Fusion Workflow

1. **Query Expansion**: The system creates multiple variations of a user’s query to broaden document retrieval.
2. **Document Retrieval**: The system queries **ChromaDB** for relevant documents, such as content from the Constitution or uploaded files.
3. **Fusion of Contexts**: The retrieved documents are combined to provide a more comprehensive context for answering the query.
4. **Response Generation**: Using **Ollama llama3.2**, the assistant generates contextually aware responses based on the fused documents.

### Citing Articles and Sections

The system can refer to specific articles and sections of the Constitution in its responses for greater clarity. For example:

> "According to Article 5, Section 2 of the Constitution, ..."

---

## Sample Queries

### Example 1: Constitution Query

**Input**: What are the rights of citizens in Kazakhstan?  
**Response**: According to Article 12, Section 1 of the Constitution, citizens of Kazakhstan are guaranteed the right to freedom, equality, and personal dignity.

### Example 2: Multi Query Expansion

**Input**: What is the official language of Kazakhstan?  
**Generated Queries**:
- What language is officially recognized in Kazakhstan?
- What is the state language of Kazakhstan?
- Which language is used for official purposes in Kazakhstan?  

**Response**: According to Article 7, Section 1 of the Constitution, the official language of Kazakhstan is Kazakh.

### Example 3: RAG Fusion with Custom Documents

**Uploaded Document**:  
`economy.txt` contains the following text:
> "Kazakhstan’s economy is heavily dependent on oil exports."

**Input**: What drives Kazakhstan's economy?  
**Response**: Based on the uploaded document, Kazakhstan’s economy is largely driven by oil exports.

---

## License

This project is released under the **MIT License**. You are free to use, modify, and distribute the code, provided proper attribution is given.

---
