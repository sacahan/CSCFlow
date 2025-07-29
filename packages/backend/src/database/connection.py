"""Database connection configuration.

This module provides database connection configuration and utility functions.
"""

import os
from typing import Optional

DATABASE_URL: Optional[str] = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/cscflow"
)
