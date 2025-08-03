from logging.config import fileConfig
import os
import importlib
import pkgutil

from sqlalchemy import engine_from_config, pool, MetaData
from alembic import context

# Load logging config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🚀 Add backend to sys.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Import engine + dynamic loader
from backend.utils.db import engine
from backend.utils.config import get_client_name
from backend.utils.model_loader import get_all_models

# ✅ Dynamically load models from client
client_name = get_client_name()
models = get_all_models(client_name)

# ✅ Collect metadata
metadata = MetaData()
for model in models:
    metadata._add_table(model.__tablename__, model.metadata.schema, model.__table__)

target_metadata = metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
