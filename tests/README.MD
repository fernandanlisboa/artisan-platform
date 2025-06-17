# Artisan Platform - Tests README

## Overview

This document provides an overview of the testing strategy and structure for the Artisan Platform project. Testing is a critical part of ensuring the reliability and quality of the application.

## Types of Tests

*   **Unit Tests:** Focus on testing individual components (functions, classes) in isolation, using mocks to simulate dependencies.
*   **Integration Tests:** Verify the interaction between different parts of the system, such as services and repositories.
*   **API Tests:** Test the full API stack, from the routes to the database, ensuring that the application behaves as expected from an external perspective.

## Test Structure

The `tests/` directory is organized as follows:

*   `unit/`: Contains unit tests.
*   `integration/`: Contains integration tests.
*   `api/`: Contains API tests.
*   `mocks/`: Contains mock objects and factories.
*   `conftest.py`: Contains pytest fixtures and configuration.

## Running Tests

1.  **Unit Tests:**

    ```bash
    pytest tests/unit
    ```
2.  **Integration Tests:**

    ```bash
    pytest tests/integration
    ```
3.  **API Tests:**

    ```bash
    pytest tests/api
    ```

## Key Fixtures

*   `app`: Configures the Flask application for testing.
*   `db`: Provides a database session for testing.
*   `client`: Provides a Flask test client for making API requests.
*   `repositories`: Initializes real repositories (for integration tests).
*   `service`: Creates services with real or mock repositories.
*   `valid_user_data`, `valid_address_data`, `valid_artisan_data`, `valid_product_data`: Provide valid data for creating test entities.
*   `clean_database`: Cleans the database before and after each test.

## Helpers

Helper functions are used to create test entities and set up common test scenarios. These functions are located in `tests/integration/helpers.py`.

## Mocks

Mocks are used in unit tests to isolate the code being tested and simulate the behavior of dependencies. The `tests/mocks/` directory contains mock objects and factories.

## Test Coverage

To generate a test coverage report:

```bash
pytest --cov=app --cov-report term-missing