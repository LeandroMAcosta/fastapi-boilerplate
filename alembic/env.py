import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context

# Import all models explicitly to populate Base.metadata
from core.db.models import Base
from modules.user.models import User  # Ensure this is imported!

# Load the appropriate .env file based on an ENV variable
env_name = os.getenv("ENVIRONMENT", "local")  # Default to "local"
dotenv_path = f".env.{env_name}"
load_dotenv(dotenv_path)

POSTGRES_URL = os.getenv("POSTGRES_URL")

if not POSTGRES_URL:
    raise ValueError("❌ DATABASE URL is not set. Check your environment variables.")

config = context.config
config.set_main_option("sqlalchemy.url", POSTGRES_URL)

# ✅ Ensure `Base.metadata` is assigned correctly
target_metadata = Base.metadata  # 👈 Fix this, remove the list


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,  # ✅ Fix here, remove list
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
