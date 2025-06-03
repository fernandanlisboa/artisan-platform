# artisan-platform


## Database Migrations (Alembic)

This backend project utilizes **Alembic** for managing database schema migrations. Alembic is a lightweight database migration tool for SQLAlchemy, designed to handle changes to your database schema in a versioned, controlled, and automated manner. It perfectly aligns with our project's commitment to Free and Open Source Software (FOSS) and integrated DevSecOps practices.

### Why Alembic?

* **Version Control for Database Schema:** Just like your code, your database schema evolves. Alembic allows us to track every change (adding tables, columns, modifying types) in versioned scripts.
* **Consistency Across Environments:** Ensures that your database schema is consistent across all environments (local development, testing, staging, production) by applying changes in a predictable order.
* **CI/CD Integration:** Migrations can be automatically applied as part of our Continuous Integration/Continuous Deployment (CI/CD) pipeline (e.g., via GitHub Actions) to ensure the database is always up-to-date with the latest code changes.
* **Collaboration:** Facilitates collaborative development, allowing multiple developers to contribute schema changes without conflicts.

### Setup and Configuration

1.  **Installation:**
    Alembic is a Python package and can be installed via `pip` within your virtual environment:
    ```bash
    pip install Alembic
    # Ensure it's added to your requirements.txt:
    # pip freeze > requirements.txt
    ```

2.  **Initialization:**
    If not already initialized, set up the Alembic environment in your project's infrastructure layer. This creates the necessary configuration files and migration script directory:
    ```bash
    # Run from the project root (where run.py is located)
    alembic init app/infrastructure/database/alembic
    ```
    This command will create the `alembic.ini` file and the `alembic/` folder (containing `env.py`, `script.py.mako`, and the `versions/` directory) inside `app/infrastructure/database/`.

3.  **Configuration (`env.py`):**
    The `app/infrastructure/database/alembic/env.py` file is configured to:
    * Load your database connection URL from the `DATABASE_URL` environment variable (defined in your `.env` file for local development, and as a GitHub Secret for CI/CD).
    * Import your SQLAlchemy models (e.g., `app.infrastructure.persistence.models_db.user_db_model`) by leveraging the `db.metadata` object from your Flask application's `app/__init__.py`. This allows Alembic to `autogenerate` migrations based on changes to your Python models.

### Key Alembic Commands

Ensure your MySQL server is running and your virtual environment is active before running these commands. All commands should be executed from the **root directory of your project**.

* **Generate a New Migration Script:**
    After making changes to your SQLAlchemy models (e.g., adding a new table, column, or modifying an existing one), Alembic can automatically detect these changes and generate a migration script.
    ```bash
    alembic revision --autogenerate -m "Add new feature_name table"
    ```
    Review the generated `.py` file in `app/infrastructure/database/alembic/versions/` to ensure it correctly reflects your intended schema changes.

* **Apply Pending Migrations to the Database:**
    This command runs all migration scripts that have not yet been applied to your database.
    ```bash
    alembic upgrade head
    ```
    This is the command that will be executed in your CI/CD pipeline.

* **Check Current Database Version:**
    ```bash
    alembic current
    ```

* **View Migration History:**
    ```bash
    alembic history
    ```

### Integration with CI/CD (GitHub Actions)

Alembic migrations are an integral part of our CI/CD pipeline. In the GitHub Actions workflow, after dependencies are installed and tests are run, the `alembic upgrade head` command will be executed to ensure the database schema is up-to-date before or during deployment. This ensures a consistent database state across all environments.

```yaml
# Example step in your .github/workflows/main.yml
- name: Run Database Migrations
  run: |
    alembic upgrade head
  working-directory: app/infrastructure/database/alembic # Ensure Alembic runs from its config location
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }} # Use your DB connection string from GitHub Secrets