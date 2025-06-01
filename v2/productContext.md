# Product Context: Astrologia API

## Purpose and Problem Solved

This API aims to provide accurate and reliable astrological calculations programmatically. It solves the problem of needing a robust backend for applications that require astrological data, such as:

- Astrological charting software
- Websites providing daily horoscopes or transit information
- Research tools for astrological patterns
- Educational platforms teaching astrology

By offering a standardized API, developers can integrate complex astrological calculations into their applications without needing to implement the intricate logic themselves or manage the underlying ephemeris data.

## How it Should Work

The API should function as a stateless service, receiving requests with all necessary input data (birth details, transit dates, locations) and returning structured JSON responses containing the calculated astrological information. The interaction should be straightforward, following standard RESTful API principles.

## User Experience Goals

- **Ease of Integration:** Developers should find it easy to integrate the API into their applications using standard HTTP libraries.
- **Predictable Responses:** The JSON response structure should be consistent and well-documented, making it easy to parse and utilize the data.
- **Reliability and Accuracy:** The core astrological calculations, powered by Kerykeion and Swiss Ephemeris, should be highly accurate and reliable.
- **Clear Error Handling:** When errors occur (e.g., invalid input), the API should return informative error messages to help developers diagnose issues.
