# Active Context: Astrologia API

## Current Work Focus

The current focus is on establishing the foundational structure of the Astrologia API based on the provided documentation and diagrams. This involves setting up the FastAPI application, defining the core data models, and implementing the initial endpoint logic for Natal Charts, Current Transits, and Transits to Natal, integrating with the Kerykeion library.

## Recent Changes

No code changes have been made yet. The recent activity has been focused on reviewing the existing documentation and planning the implementation steps.

## Next Steps

1.  Create the necessary directory structure for the FastAPI application (e.g., `app/`).
2.  Define the Pydantic models for request and response data based on the API specifications.
3.  Implement the main FastAPI application instance.
4.  Create API routers for each endpoint (`natal_chart`, `current_transits`, `transits_to_natal`, and optionally `natal_chart_svg`).
5.  Implement the logic within each router to:
    *   Receive and validate input data using Pydantic models.
    *   Call the Kerykeion library to perform astrological calculations.
    *   Format the results into the defined JSON response structure.
    *   Handle potential errors from input validation or Kerykeion.
6.  Implement API key authentication.
7.  Add basic unit tests for the core calculation logic.

## Active Decisions and Considerations

- Confirming the exact methods within Kerykeion for calculating aspects between transit and natal charts. The documentation suggests using `AstrologicalSubject` and potentially adapting `Synastry` logic or using general aspect calculation functions.
- Determining the best way to handle timezones and historical dates with Kerykeion to ensure accuracy.
- Deciding whether to implement the optional SVG generation endpoint in the initial phase or defer it.

## Important Patterns and Preferences

- Adhering to the layered architecture and RESTful design principles.
- Prioritizing clear and readable code.
- Using type hints for better code maintainability.

## Learnings and Project Insights

- The provided documentation (`arquitetura_api_astrologia.md`, `documentacao.md`, `fluxo_dados_integracao.md`) and the Mermaid diagram offer a solid foundation for the API structure and data flow.
- Kerykeion appears to be a suitable library for the core astrological calculations.
- Careful handling of date, time, location, and timezones is crucial for accurate astrological results.
