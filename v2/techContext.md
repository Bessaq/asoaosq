# Technical Context: Astrologia API

## Technologies Used

- **Language:** Python 3.9+
- **Web Framework:** FastAPI
- **Astrology Library:** Kerykeion (utilizes pyswisseph)
- **Date/Time Handling:** Python's built-in `datetime` and `pytz` for timezones.
- **ASGI Server:** Uvicorn (recommended for FastAPI)

## Development Setup

1.  Clone the project repository.
2.  Create a Python virtual environment (`python -m venv venv`).
3.  Activate the virtual environment (`source venv/bin/activate` or `venv\Scripts\activate` on Windows).
4.  Install dependencies using pip (`pip install -r requirements.txt`).
5.  Run the FastAPI application using Uvicorn (`uvicorn app.main:app --host 0.0.0.0 --port 8000`).

## Technical Constraints

- Reliance on Kerykeion for core calculations. Any limitations or behaviors of Kerykeion will affect the API.
- Precision of calculations for historical dates may vary slightly compared to other software due to differences in ephemeris handling or algorithms.
- The optional SVG generation depends on Kerykeion's capabilities in this area.

## Dependencies

- `fastapi`
- `uvicorn`
- `kerykeion`
- `pyswisseph`
- `pytz`
- `requests` (for example usage in documentation)

## Tool Usage Patterns

- Standard Python development tools (linters, formatters) should be used to maintain code quality.
- API testing can be done using tools like `curl`, Postman, or Python's `requests` library.
- The built-in OpenAPI documentation provided by FastAPI at `/docs` or `/redoc` will be crucial for understanding and using the API endpoints.
