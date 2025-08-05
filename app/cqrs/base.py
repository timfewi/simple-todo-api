"""
Base interfaces for CQRS pattern implementation.

This module defines the core contracts for commands, queries, and handlers
following the CQRS (Command Query Responsibility Segregation) pattern.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

# Type variables for generic handlers
TCommand = TypeVar("TCommand")
TQuery = TypeVar("TQuery")
TResult = TypeVar("TResult")


class Command(BaseModel, ABC):
    """
    Base class for all commands.

    Commands represent operations that change the state of the system.
    They should be imperative (e.g., CreateTodo, UpdateTodo, DeleteTodo).
    """

    pass


class Query(BaseModel, ABC):
    """
    Base class for all queries.

    Queries represent operations that read data without changing state.
    They should be descriptive (e.g., GetTodo, GetTodoList, SearchTodos).
    """

    pass


class CommandHandler(ABC, Generic[TCommand, TResult]):
    """
    Base interface for command handlers.

    Command handlers encapsulate the business logic for processing commands.
    Each command should have exactly one handler.
    """

    @abstractmethod
    async def handle(self, command: TCommand) -> TResult:
        """
        Handle the command and return the result.

        Args:
            command: The command to handle

        Returns:
            The result of handling the command
        """
        pass


class QueryHandler(ABC, Generic[TQuery, TResult]):
    """
    Base interface for query handlers.

    Query handlers encapsulate the logic for processing queries.
    Each query should have exactly one handler.
    """

    @abstractmethod
    async def handle(self, query: TQuery) -> TResult:
        """
        Handle the query and return the result.

        Args:
            query: The query to handle

        Returns:
            The result of handling the query
        """
        pass


class CommandBus(ABC):
    """Interface for command bus that routes commands to handlers."""

    @abstractmethod
    async def send(self, command: Command) -> Any:
        """Send a command to its handler."""
        pass


class QueryBus(ABC):
    """Interface for query bus that routes queries to handlers."""

    @abstractmethod
    async def send(self, query: Query) -> Any:
        """Send a query to its handler."""
        pass
