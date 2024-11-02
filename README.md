# FastAPI Starter

A comprehensive template to kickstart your FastAPI project with best practices, including Redis caching, background task processing with Celery, and SQLAlchemy ORM. This starter project is well-structured for scalability and modularity.

## Features

- **FastAPI** for quick and efficient API creation.
- **Celery** for asynchronous task management.
- **Redis** for caching and as a message broker.
- **SQLAlchemy** ORM for database interaction.
- **Alembic** for database migrations.
- **Docker** support for containerized development.
- **Pre-commit Hooks** for code quality checks.
- **Integrated Testing** using Pytest.

## Project Structure
```
.
├── .vscode/                     # VSCode workspace settings for this project
├── migrations/                  # Database migrations using Alembic
├── src/
│   ├── core/                    # Core functionality and shared utilities
│   │   ├── cache/               # Caching configurations and utilities
│   │   ├── db/                  # Database setup and connection management
│   │   ├── decorators/          # Custom decorators for function enhancements
│   │   ├── di/                  # Dependency injection configurations
│   │   ├── error/               # Error handling and custom exceptions
│   │   ├── helpers/             # Utility functions for common tasks
│   │   ├── middleware/          # Middleware for logging, error handling, etc.
│   │   ├── models/              # Shared data models (Pydantic, SQLAlchemy)
│   │   ├── permissions/         # Access control and permissions logic
│   │   ├── rate_limiter/        # Rate limiting configurations and logic
│   │   ├── repository/          # Repositories for database operations
│   │   ├── schemas/             # Pydantic schemas for data validation
│   │   ├── security/            # Security utilities (JWT, password hashing)
│   │   ├── send_request/        # HTTP request handling and third-party API integration
│   │   ├── service/             # Core business services and reusable services
│   │   ├── config.py            # Application configuration settings
│   │   └── dependencies/        # Dependency injections (e.g., auth, DB sessions)
│   ├── modules/                 # Modular application components
│   │   ├── auth/                # Auth module with routes, services etc.
│   │   ├── users/               # User module with routes, services, models, etc.
│   │   │   ├── controllers/     # User-related route controllers
│   │   │   ├── models.py        # User model definition
│   │   │   ├── services/        # User-specific business logic
│   │   │   ├── repository.py    # User data repository
│   │   │   ├── router.py        # User API route definitions
│   │   │   └── schemas.py       # User data validation schemas
│   ├── scripts/                 # Scripts for project automation and setup
│   ├── seeders/                 # Database seeders for populating initial data
│   ├── templates/               # HTML templates (if needed)
│   ├── worker/                  # Celery worker configuration and tasks
│   ├── routers.py               # Application-wide router aggregation
│   ├── main.py                  # FastAPI application entry point
│   └── tests/                   # Unit and integration test cases
├── .env.example                 # Environment variable template
├── docker-compose.yml           # Docker Compose configuration for services
├── pyproject.toml               # Poetry configuration for dependencies
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

- **Python 3.12+**
- **Docker** (recommended)
- **Redis** for caching and Celery broker
- **PostgreSQL** database (or any other supported by SQLAlchemy)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MahmudulHassan5809/fastapi-starter.git
   cd fastapi-starter
   ```

2. **Install dependencies**:

   ```bash
   poetry install
   ```

3. **Set up environment variables**:

   Copy `.env.example` to `.env` and modify it according to your setup.

4. **Run database migrations**:

   ```bash
   alembic upgrade head
   ```

5. **Start the application**:

   ```bash
   poetry run uvicorn src.main:app --reload
   ```

### Running with Docker

For a fully containerized setup, use Docker Compose:

```bash
docker-compose up --build
```

## Application Configuration

The application uses a `.env` file to configure settings like database URL, Redis URL, and API keys. The `src/core/config.py` file loads these configurations into the application.

## Modules

### Core Module

Located in `src/core/`, this module includes configuration, dependency injection, and more:

- **cache/**: Manages caching mechanisms for the application, including setups for Redis and in-memory caching to improve response times and reduce load on the database.
- **db/**: Sets up and manages the database connection, including session handling and ORM configurations.
- **decorators/**: Contains custom decorators to enhance functions, such as caching results, timing executions, or enforcing permissions.
- **di/**: Configures dependency injection, enabling modular and testable components by managing and injecting dependencies where needed.
- **error/**: Centralizes error handling with custom exceptions and error responses, simplifying error management across the application.
- **helpers/**: Utility functions used throughout the application for common tasks, like date formatting, logging helpers, or response shaping.
- **middleware/**: Custom middleware to manage logging, error handling, and request/response modification globally in the application.
- **models/**: Contains shared data models, including Pydantic schemas and SQLAlchemy models, providing a consistent data structure.
- **permissions/**: Defines access control and permission logic, enabling role-based or rule-based access checks.
- **rate_limiter/**: Manages request rate limiting for APIs, implementing limits to prevent abuse or excessive usage.
- **repository/**: Repositories for managing database interactions, with common CRUD operations abstracted for reusability.
- **schemas/**: Pydantic schemas for data validation, serialization, and deserialization, ensuring data integrity.
- **security/**: Manages security utilities, including JWT handling, password hashing, and other authentication mechanisms.
- **send_request/**: Functions to send HTTP requests, integrate with third-party APIs, and handle response parsing.
- **service/**: Core business services that provide reusable, encapsulated business logic for various modules.
- **config.py**: Centralized configuration file that loads and manages environment variables and application settings.
- **dependencies/**: Sets up dependency injections for various routes, including authentication, database sessions, and caching. 

### Users Module

Located in `src/modules/users/`, the Users module handles all user-related functionality.

- **controllers/**: Handles user-related routes and controls the flow between the API and business logic.
- **models.py**: Defines the `User` model using SQLAlchemy, specifying the structure and fields of the user entity.
- **services/**: Implements core business logic specific to users, such as registration, authentication, and profile updates.
- **repository.py**: Manages data operations for the user entity, encapsulating database interactions.
- **router.py**: Sets up and defines API routes for user operations.
- **schemas.py**: Contains Pydantic schemas for request and response validation in user-related operations.

## Database Migrations

Database schema changes are managed with Alembic:

```bash
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

## Caching with Redis

Redis is used to cache responses and improve response times. The caching logic is integrated into FastAPI through the dependency injection framework.

## Background Tasks with Celery

Celery is set up for asynchronous task management. To run the Celery worker, execute:

```bash
celery -A src.worker worker --loglevel=info
```

### Celery Configuration

The Celery broker is configured to use Redis, and this can be modified in the `.env` file. Task functions are registered in the `tasks` module.

## Testing

The project includes a robust test suite for unit and integration testing.

1. **Run all tests**:

   ```bash
   bash src/scripts/create_test_db.py
   python src/seeders/main.py
   pytest -s
   ```

2. **Pre-commit hooks**:

   This project uses pre-commit hooks for code quality. Run them on all files with:

   ```bash
   poetry run pre-commit run --all-files
   ```

### Test Structure

- **Unit Tests**: Test individual functions and classes.
- **Integration Tests**: Test API endpoints and database interactions.

## CI/CD Integration

The project is ready for CI/CD pipelines with GitHub Actions for automated testing, linting, and deployment. The GitHub Actions configuration can be extended to add custom workflows.

## Contributing

1. **Fork** the repository.
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -m 'Add your feature'`
4. **Push to the branch**: `git push origin feature/your-feature`
5. **Open a pull request**.

## License

This project is licensed under the MIT License.
