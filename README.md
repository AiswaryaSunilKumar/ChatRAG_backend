# ChatRAG: PDF Chatbot with FastAPI & Streamlit

## Overview
ChatRAG is an AI-powered chatbot that allows users to upload a PDF (such as a research paper), process it into a vector database, and interactively ask questions about its content. The system uses a FastAPI backend for PDF processing, vector storage, and query answering, and a Streamlit frontend for user interaction.

---

## Architecture

- **Frontend:** Streamlit web app
- **Backend:** FastAPI (Python)
- **Database:** Vector store using PostgreSQL (with pgvector extension)
- **LLM:** Gemini (via LangChain)

### High-Level Flow
1. User uploads a PDF via the Streamlit app.
2. The PDF is sent to the FastAPI backend, which processes and stores its content as vector embeddings.
3. The user can then ask questions about the PDF. The backend retrieves relevant chunks using vector similarity and answers using an LLM.
4. The answer is displayed in the Streamlit chat interface.

---

## FastAPI Backend

### Main Entrypoint: `main.py`
- Initializes FastAPI app.
- Adds CORS middleware for frontend-backend communication.
- Includes two routers:
  - `/vector` (PDF processing & vector store creation)
  - `/query` (Answering user questions)

### Routers

#### 1. `api/router/vectorRouter.py`
- **Endpoint:** `POST /vector/vector`
- **Request:** `{ "table_path": "<PDF file path>" }`
- **Response:** `{ "table_path": "<PDF file path>" }`
- **Functionality:**
    - Receives the PDF file path.
    - Calls `create_vector_store` to:
        - Load the PDF.
        - Split it into chunks.
        - Generate embeddings for each chunk.
        - Store them in a PostgreSQL table.
    - Returns the path as confirmation.

#### 2. `api/router/queryRouter.py`
- **Endpoint:** `POST /query/query`
- **Request:** `{ "query": "<user question>", "table_path": "<PDF file path>" }`
- **Response:** `{ "answer": "<answer from LLM>" }`
- **Functionality:**
    - Receives a user query and PDF path.
    - Calls `research_assistant` to:
        - Retrieve top relevant chunks from the vector store.
        - Compose a prompt for the LLM.
        - Return the generated answer.

---

## Backend Function Details

### `services/vector_store/creation.py`
- **`load_pdf(pdf_path)`**: Loads and parses the PDF into document objects.
- **`chunk_documents(docs)`**: Splits the PDF into overlapping text chunks for embedding.
- **`get_embedding(text, embeddings)`**: Generates a vector embedding for a chunk using the LLM's embedding model.
- **`sanitize_table_name(name)`**: Converts a file name into a safe SQL table name.
- **`create_table_if_not_exists(engine, pdf_path)`**: Creates (or resets) a table for the PDF's embeddings in PostgreSQL.
- **`insert_chunks_with_embeddings(engine, chunks, source_file, embeddings)`**: Inserts each chunk and its embedding into the database.
- **`create_vector_store(PDF_PATH)`**: Orchestrates the above; loads, chunks, embeds, and stores the PDF.

### `services/agent/assistant.py`
- **`research_assistant(query, pdf_path)`**:
    - Calls `search_vector_store` to retrieve the top 5 relevant chunks from the PDF.
    - Composes a prompt for the Gemini LLM, including the user query and retrieved excerpts.
    - Invokes the LLM and returns the answer.

---

## Streamlit Frontend (`streamlit_app.py`)

### Features
- **PDF Upload:**
  - Users can upload a PDF via the sidebar.
  - The file is saved locally and sent to the backend for processing.
- **Vector Store Creation:**
  - On upload, the app calls `/vector/vector` to process and embed the PDF.
  - Success/failure is shown to the user.
- **Chat Interface:**
  - Users can ask questions about the uploaded PDF.
  - Each question triggers a call to `/query/query`, sending the query and PDF path.
  - Answers (or error messages) are displayed in a conversational format.
- **Session State:**
  - Remembers uploaded file, chat history, and vector store status for a smooth user experience.

### Communication with Backend
- Uses `requests.post` to interact with FastAPI endpoints.
- Handles upload, vector store creation, and chat queries via HTTP.

---

## Running the Project

**Prerequisites**
Paste your Google API Key and Supabase Connection String in the `.env` file.

1. **Install dependencies:**
   ```bash
   uv sync
   ```
2. **Start the backend:**
   ```bash
   uv run uvicorn main:app --reload
   ```
3. **Start the frontend:**
   ```bash
   uv run streamlit run streamlit_app.py
   ```

---

## Notes
- Ensure PostgreSQL with the `pgvector` extension is running and accessible.
- Configure connection strings and LLM keys as needed in the `settings` module.
- The LLM used is Gemini (can be replaced/configured in `LLMFactory`).

---

## File Structure
```
ChatRAG/
├── api/
│   └── router/
│       ├── queryRouter.py
│       └── vectorRouter.py
├── services/
│   ├── agent/
│   │   └── assistant.py
│   └── vector_store/
│       └── creation.py
├── streamlit_app.py
├── main.py
├── README.md
└── ...
```

---

## Contact & Contributions
Pull requests and issues are welcome!
