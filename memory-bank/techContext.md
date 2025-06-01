# Technical Context: Astrologia API

## Technologies Used

- **Language:** Python 3.9+
- **Web Framework:** FastAPI
- **Astrology Library:** Kerykeion (utilizes pyswisseph)
- **Date/Time Handling:** Python's built-in `datetime` and `pytz` for timezones.
- **ASGI Server:** Uvicorn (recommended for FastAPI)
- **Text Processing:** pdftotext (from poppler-utils)
- **Vector Embeddings (Attempted):** SentenceTransformers
- **Vector Index (Attempted):** FAISS
- **API Key Authentication:** FastAPI's `APIKeyHeader` and `Security`
## Development Setup

1.  Clone the project repository.
2.  Create a Python virtual environment (`python -m venv venv`).
3.  Activate the virtual environment (`source venv/bin/activate` or `venv\Scripts\activate` on Windows).
4.  Install dependencies using pip (`pip install -r requirements.txt`).
5.  Run the FastAPI application using Uvicorn (`uvicorn main:app --host 0.0.0.0 --port 8000`).

## Technical Constraints

- Reliance on Kerykeion for core calculations. Any limitations or behaviors of Kerykeion will affect the API.
- Precision of calculations for historical dates may vary slightly compared to other software due to differences in ephemeris handling or algorithms.
- The optional SVG generation depends on Kerykeion's capabilities in this area.
- The RAG implementation is currently limited by available RAM and may require alternative approaches.

## Dependencies

- `fastapi`
- `uvicorn`
- `kerykeion`
- `pyswisseph`
- `pytz`
- `python-dotenv`
- `requests` (for example usage in documentation)
- `langchain`
- `faiss-cpu`
- `sentence-transformers`
- `pdftotext` (requires poppler-utils to be installed on the system)

## Tool Usage Patterns

- Standard Python development tools (linters, formatters) should be used to maintain code quality.
- API testing can be done using tools like `curl`, Postman, or Python's `requests` library.
- The built-in OpenAPI documentation provided by FastAPI at `/docs` or `/redoc` will be crucial for understanding and using the API endpoints.
- The `pdftotext` command-line tool is used for extracting text from PDF files.
- Langchain and SentenceTransformers are used for creating vector embeddings and searching for similar text.
- FastAPI's `APIKeyHeader` and `Security` are used for implementing API key authentication.
- Taskmaster AI is used for project management and task generation.
