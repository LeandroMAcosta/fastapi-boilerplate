# FastAPI Application

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

This repository contains a FastAPI application with database integration, Docker support, authentication, and user management.

## Project Structure

The project follows a modular architecture:

- `src/`: Main application code
  - `core/`: Core components (config, database, server setup)
  - `modules/`: Feature modules (auth, user)
- `alembic/`: Database migration tools
- `tests/`: Test suite
- Docker configuration for containerization

### Core Components (per module)

- **models.py**: SQLAlchemy ORM models mapping to database tables
- **repository.py**: Database query operations implementing the Repository pattern
- **schemas.py**: Pydantic models for request/response validation and serialization
- **service.py**: Business logic layer that orchestrates repositories and implements domain rules
- **routes.py**: API endpoints that connect HTTP requests to services

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional, for containerized deployment, recommended for frontend developers)

## Setup Instructions

### Local Development Setup

1. **Clone the repository**

<!-- Change url if this boilerplate was forked or copied -->
```bash
git clone https://github.com/LeandroMAcosta/fastapi_boilerplate
cd fastapi_boilerplate
```

2. **Create and activate a virtual environment**

Clarification: The following steps are optional but recommended for local development. You can also use the Docker setup directly.
If you are frontend developer, you can skip this step and use the docker setup. [Docker Setup](#docker-setup)

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env.local` file in the project root with necessary configuration (database connection, secret keys, etc.).
You can copy from env.example
```bash
cp env.example .env.local
```

5. **Run database migrations**

```bash
alembic upgrade head
```

6. **Start the application**

```bash
python -m src.main
```

The API will be available at http://localhost:8000

### Docker Setup

1. **Build and start the containers**

```bash
docker-compose up --build
```

This will start the API and database services as defined in the `docker-compose.yml`.

2. **Run migrations in the container**

```bash
docker-compose exec app alembic upgrade head
```

## API Documentation

When the application is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- ReDoc alternative documentation: http://localhost:8000/redoc

## Database Migrations

This project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Revert migrations
alembic downgrade -1
```

## Testing

Run the test suite with:

```bash
pytest
```

## Project Development

The project uses several tools to ensure code quality:

- **Black**: For consistent code formatting (line length: 120)
- **isort**: For standardized import ordering
- **mypy**: For static type checking
- **pre-commit**: For automated code quality checks

### Pre-commit Setup

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the git hooks:
```bash
pre-commit install
```

3. (Optional) Run against all files:
```bash
pre-commit run --all-files
```