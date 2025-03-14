# FastAPI Application

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

The `pyproject.toml` file contains configuration for Black code formatting.