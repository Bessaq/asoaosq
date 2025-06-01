# Project Brief: Astrologia API

## Core Requirements and Goals

The primary goal of this project is to develop a robust and accurate Astrologia API using Python, FastAPI, and the Kerykeion library. The API should provide endpoints for calculating:

1.  **Natal Charts:** Calculate detailed birth charts including planetary positions, house cusps, Ascendant, Midheaven, and aspects.
2.  **Current Transits:** Calculate planetary positions for a specific date, time, and location.
3.  **Transits to Natal Chart:** Calculate transit planetary positions and the aspects they form with natal planets and points.
4.  **(Optional) Natal Chart SVG:** Generate an SVG representation of a natal chart.

The API should be designed with modularity, statelessness, clarity, consistency, scalability, and maintainability in mind.

## Project Scope

The initial scope includes the core functionalities listed above. Future considerations, such as Progressions, Directions, Synastry, Solar/Lunar Returns, textual interpretations, support for different Ayanamsas, and ephemeris lookups, are outside the initial scope.

## Key Technologies

- Python 3.9+
- FastAPI
- Kerykeion (with pyswisseph)
- Standard Python libraries (`datetime`, `pytz`)
- Uvicorn or Gunicorn

## Data Format

All requests and responses will use JSON format.

## Authentication

Initial authentication will be based on API Keys sent in the `X-API-KEY` header.

## Error Handling

Standard HTTP status codes will be used, with JSON bodies providing clear error messages.

## Versioning

The API will be versioned, starting with `/api/v1/`.
