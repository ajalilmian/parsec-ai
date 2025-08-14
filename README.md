# Parsec AI

**Parsec AI** is an intelligent document query system to chat with your PDFs. It's built with a **FastAPI** backend, **Streamlit** frontend and a **Retrieval-Augmented Generation (RAG)** pipeline.

## About The Project

Parse documents at light speed. Parsec AI allows you to have a conversation with your files. Simply upload a PDF, such as a marketing brief, a research paper or a legal document, and ask questions in natural language to get instant, context-aware answers.

This project demonstrates a modern, full-stack approach to building AI applications. It features a decoupled architecture with a robust backend handling the core AI logic and a user-friendly frontend for the chat interface.

## Key Features

- **PDF Upload:** Easily upload and process PDF documents.
- **Conversational Q&A:** Ask follow-up questions in a natural, chat-like manner.
- **Context-Aware Answers:** The AI generates responses based only on the content of the uploaded document, preventing hallucination.
- **Real-time Interaction:** A responsive interface for a smooth user experience.

## How It Works

The core of Parsec AI is a **Retrieval-Augmented Generation (RAG)** pipeline built with LangChain.

1. **Ingestion:** The uploaded PDF is loaded and split into smaller, manageable chunks.
2. **Embedding:** Each chunk is converted into a numerical representation (embedding) using OpenAI's models.
3. **Storage:** These embeddings are stored in a ChromaDB vector store for efficient searching.
4. **Retrieval:** When you ask a question, the system finds the most relevant chunks from the vector store.
5. **Generation:** The relevant chunks and your original question are sent to an OpenAI language model, which generates a coherent, context-aware answer.

## Tech Stack

- **Backend:** Python, FastAPI, LangChain, OpenAI, ChromaDB, PyPDF
- **Frontend:** Streamlit, Requests
- **Architecture:** Decoupled REST API (Backend) + Web UI (Frontend)

## Setup and Installation

Follow these steps to get a local copy up and running.

### Prerequisites

- Python 3.9+
- Git

### Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/ajalilmian/parsec-ai.git
   cd parsec-ai

   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   ```

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt

   ```

4. **Set up your environment variables**

   Create a `.env` file inside the `backend/` directory and add your OpenAI API key:

   ```text
   OPENAI_API_KEY="sk-YourSecretKeyHere"

   ```

## Usage

You'll need to run the backend and frontend in two separate terminals.

1. **Run the Backend Server** (from the root directory)

   ```bash
   cd backend
   uvicorn main:app --reload

   ```

   The API will be available at `http://127.0.0.1:8000`.

2. **Run the Frontend Application** (from the root directory, in a new terminal)

   ```bash
   cd frontend
   streamlit run app.py

   ```

   Open your browser and go to `http://localhost:8501`.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
