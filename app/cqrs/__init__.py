"""
CQRS (Command Query Responsibility Segregation) implementation for Todo API.

This package contains the CQRS implementation including commands, queries,
handlers, and buses for the Todo application.
"""

# Import base interfaces
from .base import Command
from .base import CommandBus as CommandBusInterface
from .base import CommandHandler, Query
from .base import QueryBus as QueryBusInterface
from .base import QueryHandler

# Import concrete implementations
from .buses import CommandBus, QueryBus
from .dependencies import get_command_bus, get_query_bus

__all__ = [
    # Base interfaces
    "Command",
    "Query",
    "CommandHandler",
    "QueryHandler",
    "CommandBusInterface",
    "QueryBusInterface",
    # Implementations
    "CommandBus",
    "QueryBus",
    # Dependencies
    "get_command_bus",
    "get_query_bus",
]
