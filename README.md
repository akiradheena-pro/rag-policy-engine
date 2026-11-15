# HR Policy RAG Assistant

A document-grounded question-answering assistant for HR policies. The project lets users ask questions about policy documents and receive answers based on retrieved content.

This is an academic project and portfolio demonstration. It is not an official HR system and its answers should be checked against the source policy before being used for decisions.

## What it does

- Ingests policy documents and prepares them for retrieval.
- Uses a vector store to retrieve relevant policy content for a question.
- Generates a response using a language model through the project’s configured provider.
- Provides a Streamlit interface for asking questions.
- Includes evaluation code and saved evaluation results.

## Architecture

```text
Policy documents
      ↓
Ingestion and chunking
      ↓
ChromaDB vector index
      ↓
User question → retrieval → language model → answer
      ↓
Streamlit interface
```

The repository also includes a Dockerfile and deployment configuration. See the project files for the current run and deployment setup.

## Technology

- Python
- LangChain
- ChromaDB
- Groq API
- Streamlit
- Docker

## Repository layout

```text
app/                    Application code
data/                   Policy document data
chroma_db/              Local vector-store data
ingest.py               Document ingestion
evaluate.py             Evaluation script
evaluation_results.json Saved evaluation output
streamlit_app.py        Streamlit user interface
main.py                 Application entry point
Dockerfile              Container configuration
requirements.txt        Python dependencies
```

## Run locally

1. Clone the repository and enter the project directory.

   ```bash
   git clone https://github.com/akiradheena-pro/rag-policy-engine.git
   cd rag-policy-engine
   ```

2. Create and activate a virtual environment, then install dependencies.

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Configure the model provider credentials using environment variables. Do not commit API keys or other secrets.

4. Build or refresh the vector index using the ingestion script:

   ```bash
   python ingest.py
   ```

5. Start the interface:

   ```bash
   streamlit run streamlit_app.py
   ```

Check the application configuration and scripts for the exact environment-variable names and any additional setup required by the current version.

## Evaluation

The repository includes `evaluate.py` and `evaluation_results.json`. Consult the evaluation output for the dataset, metrics, and results produced by this project. Evaluation scores depend on the dataset and test procedure; they should not be interpreted as a guarantee that every answer is correct or complete.

## Security and limitations

- Keep provider API keys in local environment variables or a secret manager; never commit real credentials.
- Treat generated responses as assistance, not authoritative HR or legal advice.
- Verify important answers against the cited source policy.
- The project is a portfolio/academic demonstration and has not been presented here as a supported production HR service.

## Author

Akira Dheena — [GitHub profile](https://github.com/akiradheena-pro)
