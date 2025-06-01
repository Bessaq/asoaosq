# System Patterns: Astrologia API

## System Architecture

The API follows a layered architecture:

- **API Layer:** Handles HTTP requests, input validation, and response formatting. Built with FastAPI.
- **Astrological Logic Layer:** Contains the core astrological calculation logic, primarily using the Kerykeion library. This layer abstracts the complexity of Kerykeion and Swiss Ephemeris from the API layer.
- **Utilities/Configuration Layer:** Provides auxiliary functions, date/time handling, and configuration management.

## Key Technical Decisions

- **Framework:** FastAPI was chosen over Flask for its performance and automatic documentation generation (OpenAPI).
- **Astrology Library:** Kerykeion was selected for its comprehensive features and reliance on the accurate Swiss Ephemeris.
- **Stateless Design:** Each API request is independent and contains all necessary data, simplifying scaling and management.
- **JSON Data Format:** Standardized JSON for all data exchange.

## Design Patterns in Use

- **Layered Architecture:** Separating concerns into distinct layers (API, Logic, Utilities).
- **RESTful API:** Designing endpoints and interactions based on REST principles.
- **Input Validation:** Implementing validation at the API layer to ensure data integrity before processing.

## Component Relationships

- The API Layer receives requests and calls functions in the Astrological Logic Layer.
- The Astrological Logic Layer uses the Kerykeion library to perform calculations.
- The Utilities Layer provides supporting functions used by other layers.
- The API Layer formats the results from the Astrological Logic Layer into JSON responses.

## Critical Implementation Paths

- **Natal Chart Calculation:** Receiving birth data -> Validating data -> Calling Kerykeion to create `AstrologicalSubject` -> Extracting planet, house, and aspect data -> Formatting JSON response.
- **Current Transits Calculation:** Receiving date/time/location -> Validating data -> Calling Kerykeion to create `AstrologicalSubject` -> Extracting planet data -> Formatting JSON response.
- **Transits to Natal Calculation:** Receiving natal and transit data -> Validating both datasets -> Creating two `AstrologicalSubject` objects -> Calculating aspects between the two subjects (potentially using Kerykeion's synastry or aspect calculation functions) -> Formatting JSON response.
- **Error Handling:** Detecting invalid input or calculation errors -> Returning appropriate HTTP status codes and JSON error messages.
