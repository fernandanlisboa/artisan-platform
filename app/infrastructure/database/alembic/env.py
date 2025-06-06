# app/infrastructure/database/alembic/env.py

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from dotenv import load_dotenv # Import to load .env
import os # Import to access environment variables

from app import db 
# import app.infrastructure.persistence.models_db # Garante que os modelos ORM sejam carregados

# --- ADICIONE ESTES IMPORTS EXPLÍCITOS PARA CADA UM DOS SEUS MODELOS DB ---
from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel
from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
from app.infrastructure.persistence.models_db.artisan_db_model import ArtisanDBModel
from app.infrastructure.persistence.models_db.buyer_db_model import BuyerDBModel
from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
from app.infrastructure.persistence.models_db.review_db_model import ReviewDBModel
from app.infrastructure.persistence.models_db.order_db_model import OrderDBModel
from app.infrastructure.persistence.models_db.order_item_db_model import OrderItemDBModel
from app.infrastructure.persistence.models_db.message_db_model import MessageDBModel

load_dotenv() 

# --- PRINT WAS HERE IN THE GLOBAL CONTEXT, REMOVE OR MOVE IT INSIDE FUNCTIONS ---
# The print you had here at the top is not necessary if it's inside the functions


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata


def run_migrations_offline() -> None:
    url = os.getenv("DATABASE_URL")
    # Este print serve para o modo offline
    print(f"DEBUG OFFLINE: DATABASE_URL que Alembic está lendo (OFFLINE): {url}") # Opcional
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,             
        compare_server_default=True,   
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_database_url = os.getenv("DATABASE_URL")

    # --- NOVO LOCAL DO PRINT DE DEBUG PARA O MODO ONLINE (CRÍTICO) ---
    print(f"\n--- DEBUG ALEMBIC ONLINE START ---")
    print(f"DATABASE_URL que Alembic está lendo (ONLINE): {alembic_database_url}")
    if alembic_database_url:
        try:
            user = alembic_database_url.split('://')[1].split(':')[0]
            host = alembic_database_url.split('@')[1].split(':')[0] if '@' in alembic_database_url else 'N/A'
            print(f"Usuário na URL (ONLINE): {user}")
            print(f"Host na URL (ONLINE): {host}")
        except IndexError:
            print("Formato de DATABASE_URL inválido para análise.")
    print(f"--- DEBUG ALEMBIC ONLINE END ---\n")
    # --- FIM DO NOVO LOCAL DO PRINT ---


    config_section = config.get_section(config.config_ini_section, {})
    config_section['sqlalchemy.url'] = alembic_database_url


    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            compare_type=True,             # Bom ter
            compare_server_default=True,   # <--- VERIFIQUE/ADICIONE ESTA LINHA
            render_as_batch=True,  # Necessário para MySQL
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()