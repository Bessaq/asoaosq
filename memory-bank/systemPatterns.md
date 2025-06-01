# System Patterns: Astrologia API

## System Architecture

The API follows a layered architecture:

- **API Layer:** Handles HTTP requests, input validation, and response formatting. Built with FastAPI.
- **Astrological Logic Layer:** Contains the core astrological calculation logic, primarily using the Kerykeion library. This layer abstracts the complexity of Kerykeion and Swiss Ephemeris from the API layer.
- **Utilities/Configuration Layer:** Provides auxiliary functions, date/time handling, and configuration management.
- **RAG Layer (Planned):** This layer will handle the retrieval of relevant information from the astrological books and generate interpretations. Due to resource limitations, this layer is currently not fully implemented and will be based on a simpler text search approach initially.

## Key Technical Decisions

- **Framework:** FastAPI was chosen over Flask for its performance and automatic documentation generation (OpenAPI).
- **Astrology Library:** Kerykeion was selected for its comprehensive features and reliance on the accurate Swiss Ephemeris.
- **Stateless Design:** Each API request is independent and contains all necessary data, simplifying scaling and management.
- **JSON Data Format:** Standardized JSON for all data exchange.
- **API Key Authentication:** Implemented for basic security.

## Design Patterns in Use

- **Layered Architecture:** Separating concerns into distinct layers (API, Logic, Utilities, RAG).
- **RESTful API:** Designing endpoints and interactions based on REST principles.
- **Input Validation:** Implementing validation at the API layer to ensure data integrity before processing.

## Component Relationships

- The API Layer receives requests and calls functions in the Astrological Logic Layer.
- The Astrological Logic Layer uses the Kerykeion library to perform calculations.
- The Utilities Layer provides supporting functions used by other layers.
- The API Layer formats the results from the Astrological Logic Layer into JSON responses.
- (Future) The API Layer will call the RAG Layer to generate interpretations based on the input data and the retrieved information from the astrological books.

## Critical Implementation Paths

- **Natal Chart Calculation:** Receiving birth data -> Validating data -> Calling Kerykeion to create `AstrologicalSubject` -> Extracting planet, house, and aspect data -> Formatting JSON response.
- **Current Transits Calculation:** Receiving date/time/location -> Validating data -> Calling Kerykeion to create `AstrologicalSubject` -> Extracting planet data -> Formatting JSON response.
- **Transits to Natal Calculation:** Receiving natal and transit data -> Validating both datasets -> Creating two `AstrologicalSubject` objects -> Calculating aspects between the two subjects (potentially using Kerykeion's synastry or aspect calculation functions) -> Formatting JSON response.
- **SVG Chart Generation:** Receiving chart data -> Creating `AstrologicalSubject` -> Using `KerykeionChartSVG` to generate the SVG -> Returning the SVG as a response.
- **Error Handling:** Detecting invalid input or calculation errors -> Returning appropriate HTTP status codes and JSON error messages.
- **(Future) Interpretation Generation:** Receiving a request for interpretation -> Using the RAG layer to retrieve relevant information from the astrological books -> Using a language model to generate a textual interpretation -> Returning the interpretation in the JSON response.
