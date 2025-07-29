"""Database models package.

This package contains all the database models for the application.
Models are organized by domain and are imported here for convenient access.
"""

from .sport_center import SportCenter
from .real_time_flow import RealTimeFlow
from .historical_stats import HistoricalStats

from sqlalchemy.ext.declarative import declarative_base

# Create the base class for declarative models
Base = declarative_base()

# Import all models here for convenient access and to ensure they are registered with SQLAlchemy
__all__ = [
    "Base",
    "SportCenter",
    "RealTimeFlow",
    "HistoricalStats",
]
