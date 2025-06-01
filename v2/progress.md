# Progress: Astrologia API

## What Works

- Initial project documentation has been reviewed and processed.
- The core architecture and data flow are understood based on the provided diagrams and documents.
- The key technologies and dependencies have been identified.
- The core memory bank structure has been established.

## What's Left to Build

- The actual Python code for the FastAPI application.
- Pydantic models for request and response validation.
- API routers and endpoint logic for:
    - Natal Chart calculation
    - Current Transits calculation
    - Transits to Natal Chart calculation
    - (Optional) Natal Chart SVG generation
- Integration with the Kerykeion library for all astrological calculations.
- API key authentication middleware or dependency.
- Error handling implementation.
- Unit tests.
- Comprehensive documentation within the code (docstrings) and potentially updating the external `documentacao.md` file as implementation progresses.

## Current Status

The project is in the initial planning and setup phase. The architecture and implementation approach have been defined based on the provided materials. The memory bank has been created to store project context.

## Known Issues

- Potential complexities in handling historical dates and timezones accurately with Kerykeion.
- Need to confirm the specific Kerykeion methods for calculating transit-to-natal aspects.

## Evolution of Project Decisions

- The decision to use FastAPI over Flask is based on the provided architecture document's preference for performance and auto-documentation.
- The reliance on Kerykeion is a core decision based on its capabilities and use of Swiss Ephemeris.
