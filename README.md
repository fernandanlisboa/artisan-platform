# 🏺 Artisan Platform API - Robust Backend Architecture

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" />
  <img src="https://img.shields.io/badge/OWASP%20ZAP-000000?style=flat-square&logo=owasp&logoColor=white" />
</p>

## 📌 Overview

The Artisan Platform API is a robust, production-ready backend built to demonstrate advanced software engineering practices. While its technical focus is on providing a highly scalable, secure, and test-driven architecture, its domain goal is to create a seamless digital ecosystem for independent creators.

This repository serves as a showcase of applying **Clean Architecture principles, automated CI/CD pipelines, and rigorous security testing**, which are foundational skills for modern Backend and DevOps engineering.

## 🎯 Business Context & Problem Statement

**The Problem:** Independent artisans often struggle to establish a digital footprint. They face high commission fees on generic e-commerce platforms and lack tailored tools to manage unique, handcrafted inventories and direct customer relationships.

**The Solution:** The Artisan Platform provides a specialized, low-friction digital environment. It empowers creators by facilitating direct transactions, offering dedicated management tools, and streamlining order fulfillment, ultimately bridging the gap between local craftsmanship and the broader digital market.

## 🏗️ System Architecture

The project strictly follows a **Layered Architecture** to ensure separation of concerns, maintainability, and testability:

* **Presentation Layer:** Handles HTTP requests/responses routing and payload validation using DTOs (Pydantic).
* **Application Layer:** Orchestrates business use cases and logic via decoupled services.
* **Domain Layer:** Represents core business entities and strict domain rules.
* **Infrastructure Layer:** Manages data persistence, utilizing the **Repository Pattern** to abstract database interactions and ORM specificities.

## 🛠️ Tech Stack

* **Core:** Python 3.12
* **Web/API Framework:** FastAPI
* **Database & ORM:** MySQL (Production), SQLite (Testing), SQLAlchemy
* **Data Validation:** Pydantic
* **Migrations:** Alembic
* **DevSecOps:** GitHub Actions (CI/CD), OWASP ZAP (Dynamic Application Security Testing)
* **Testing:** Pytest

## 🧪 Testing Strategy (TDD)

Quality assurance is a first-class citizen in this project. Developed under a Test-Driven Development (TDD) mindset, the application ensures high reliability through:
* **Unit Tests:** Isolating and testing individual business rules and domain logic.
* **Integration Tests:** Validating the interaction between the Application layer and the Infrastructure (Database/Repositories).
* **API/E2E Tests:** Ensuring endpoint contracts and request/response lifecycles work as expected.

Run the test suite using:
```bash
pytest -v --cov=app
```

## 🚀 DevSecOps & CI/CD Pipeline

Automated workflows are configured via **GitHub Actions** (`.github/workflows`) to enforce continuous integration:
1.  **Code Integration:** Triggers `pytest` and linting on every Pull Request.
2.  **Security Scanning:** Integrates **OWASP ZAP** to identify vulnerabilities (e.g., SQL Injection, XSS) before merging. Details in the [Security Testing Documentation](docs/security_testing.md).
3.  **Continuous Deployment:** Automated staging/production deployments upon merging to specific branches.

## ⚙️ Local Setup & Execution

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/fernandanlisboa/artisan-platform
    cd artisan-platform
    ```
2.  **Environment Setup:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Database & Migrations:**
    Create a `.env` file based on `.env.example` and apply Alembic migrations. See details in [Alembic README](app/infrastructure/database/alembic/README).
    ```bash
    alembic upgrade head
    ```
4.  **Run the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 🤝 Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Follow the project's coding conventions.
4.  Submit a pull request.

## 👥 Contributors

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
