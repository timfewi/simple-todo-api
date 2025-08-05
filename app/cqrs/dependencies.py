"""
CQRS dependency injection setup for FastAPI.

This module provides dependency injection functions for creating
and configuring CQRS buses and handlers with database sessions.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.cqrs.buses import CommandBus, QueryBus
from app.cqrs.commands.todo_commands import (
    CreateTodoCommand,
    DeleteTodoCommand,
    UpdateTodoCommand,
)
from app.cqrs.handlers.todo_command_handlers import (
    CreateTodoCommandHandler,
    DeleteTodoCommandHandler,
    UpdateTodoCommandHandler,
)
from app.cqrs.handlers.todo_query_handlers import (
    GetTodoListQueryHandler,
    GetTodoQueryHandler,
    GetTodosCountQueryHandler,
)
from app.cqrs.queries.todo_queries import (
    GetTodoListQuery,
    GetTodoQuery,
    GetTodosCountQuery,
)
from app.database.connection import get_db


def get_command_bus(db: Annotated[Session, Depends(get_db)]) -> CommandBus:
    """
    Create and configure the command bus with all command handlers.

    Args:
        db: Database session dependency

    Returns:
        CommandBus: Configured command bus with registered handlers
    """
    command_bus = CommandBus()

    # Register command handlers
    command_bus.register_handler(CreateTodoCommand, CreateTodoCommandHandler(db))
    command_bus.register_handler(UpdateTodoCommand, UpdateTodoCommandHandler(db))
    command_bus.register_handler(DeleteTodoCommand, DeleteTodoCommandHandler(db))

    return command_bus


def get_query_bus(db: Annotated[Session, Depends(get_db)]) -> QueryBus:
    """
    Create and configure the query bus with all query handlers.

    Args:
        db: Database session dependency

    Returns:
        QueryBus: Configured query bus with registered handlers
    """
    query_bus = QueryBus()

    # Register query handlers
    query_bus.register_handler(GetTodoQuery, GetTodoQueryHandler(db))
    query_bus.register_handler(GetTodoListQuery, GetTodoListQueryHandler(db))
    query_bus.register_handler(GetTodosCountQuery, GetTodosCountQueryHandler(db))

    return query_bus
