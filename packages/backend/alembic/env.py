from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sqlalchemy

from alembic import context

# 將專案根目錄加入 Python Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# 導入模型以支援自動遷移
from src.database.models import Base
from src.database.db import DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 從環境變數設定資料庫URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 設定metadata用於自動遷移
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode using async engine."""

    # 處理異步引擎的配置
    configuration = config.get_section(config.config_ini_section)
    url = configuration.get("sqlalchemy.url")
    configuration["sqlalchemy.url"] = url.replace("+asyncpg", "")  # 移除async驅動器

    try:
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    except sqlalchemy.exc.OperationalError as e:
        raise RuntimeError("資料庫連接失敗，請檢查 DATABASE_URL 設置") from e

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # 比較時包含外鍵
            include_schemas=True,
            # 比較時包含索引
            include_index=True,
            # 支援 UUID 類型
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
