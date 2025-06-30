# Artisan Platform - Project README

## Overview

The Artisan Platform is a web application designed to connect artisans with customers, providing a space to showcase and sell handcrafted products. It aims to empower artisans by providing tools for managing their online presence and facilitating transactions.

## Architecture

The project follows a layered architecture:

*   **Presentation Layer:** Handles HTTP requests and responses, including controllers and DTOs.
*   **Application Layer:** Contains the business logic of the application, implemented through services.
*   **Domain Layer:** Represents the core business objects and rules, using models/entities.
*   **Infrastructure Layer:** Manages data persistence and external system interactions, using repositories and database models.

Key design patterns include the Repository pattern for data access abstraction and Data Transfer Objects (DTOs) for data transfer between layers.

## Technologies

*   **Programming Language:** Python
*   **Web Framework:** Flask
*   **API Framework:** Flask-RESTx
*   **Database:** MySQL, PostgreSQL, SQLite (for testing)
*   **ORM:** SQLAlchemy
*   **Data Validation:** Pydantic
*   **Database Migrations:** Alembic
*   **CI/CD:** GitHub Actions
*   **Security Testing:** OWASP ZAP

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd artisan-platform
    ```
2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**

    *   On Windows:

        ```bash
        venv\Scripts\activate
        ```
    *   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```
4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure environment variables:**

    *   Create a `.env` file based on `.env.example`.
    *   Set the necessary environment variables, such as `FLASK_SECRET_KEY` and `DATABASE_URL`.

## Database Migrations

This backend project utilizes **Alembic** for managing database schema migrations. See more details in the [Alembic README](app/infrastructure/database/alembic/README).

## Continuous Integration and Continuous Deployment (CI/CD)

This project uses **GitHub Actions** for automated CI/CD. The configuration files are located in the `.github/workflows` directory. These workflows automate the following:

*   Running tests on each pull request.
*   Deploying the application to staging/production environments upon merging to specific branches.

## Security Testing

This project incorporates security testing using **OWASP ZAP (Zed Attack Proxy)**. This tool helps identify vulnerabilities in the application. Details on how to run and interpret the security scans can be found in the [Security Testing Documentation](docs/security_testing.md) (example path, create if needed).

## Execution

1.  **Run the application:**

    ```bash
    flask run
    ```
2.  **Run tests:**

    ```bash
    pytest
    ```

## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Follow the project's coding conventions.
4.  Submit a pull request.

## Contributors

<div align="center">
  <a href="https://github.com/fernandanlisboa/" style="margin: 0 10px;">
    <img src="https://avatars.githubusercontent.com/u/50326541?v=4" alt="Fernanda Lisboa" style="border-radius: 50%; width: 40px; height: 40px; vertical-align: middle;">
    Fernanda Lisboa
  </a>
  <a href="https://github.com/Gustavo-Cruzz/" style="margin: 0 10px;">
    <img src="https://avatars.githubusercontent.com/u/82175584?v=4" alt="Gustavo Cruz" style="border-radius: 50%; width: 40px; height: 40px; vertical-align: middle;">
    Gustavo Cruz
  </a>
  <a href="https://github.com/Yas-bonfim/" style="margin: 0 10px;">
    <img src="https://avatars.githubusercontent.com/u/81273398?v=4" alt="Yasmin Bonfim" style="border-radius: 50%; width: 40px; height: 40px; vertical-align: middle;">
    Yasmin Bonfim
  </a>
</div>
