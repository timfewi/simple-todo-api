"""
CQRS buses implementation for routing commands and queries to their handlers.

This module provides concrete implementations of CommandBus and QueryBus
that handle the routing of commands and queries to their appropriate handlers.
"""

from typing import Any, Dict, Type, TypeVar

from app.cqrs.base import Command
from app.cqrs.base import CommandBus as CommandBusInterface
from app.cqrs.base import CommandHandler, Query
from app.cqrs.base import QueryBus as QueryBusInterface
from app.cqrs.base import QueryHandler

TCommand = TypeVar("TCommand", bound=Command)
TQuery = TypeVar("TQuery", bound=Query)
TResult = TypeVar("TResult")

class CommandBus(CommandBusInterface):
    """
    Command bus implementation for routing commands to their handlers.

    This class maintains a registry of command types and their corresponding
    handlers, enabling dynamic routing and execution of commands.
    """

    def __init__(self):
        """Initialize the command bus with an empty handler registry."""
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register_handler(
        self, command_type: Type[TCommand], handler: CommandHandler[TCommand, Any]
    ) -> None:
        """
        Register a command handler for a specific command type.

        Args:
            command_type: The command class type
            handler: The handler instance for this command type
        """
        self._handlers[command_type] = handler

    async def execute(self, command: TCommand) -> Any:
        """
        Execute a command by routing it to the appropriate handler.

        Args:
            command: The command instance to execute

        Returns:
            Any: The result returned by the command handler

        Raises:
            ValueError: If no handler is registered for the command type
        """
        command_type = type(command)
        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for command type: {command_type}")

        handler = self._handlers[command_type]
        return await handler.handle(command)

    async def send(self, command: Command) -> Any:
        """
        Send a command to its handler (alias for execute method).

        Args:
            command: The command instance to send

        Returns:
            Any: The result returned by the command handler
        """
        return await self.execute(command)


class QueryBus(QueryBusInterface):
    """
    Query bus implementation for routing queries to their handlers.

    This class maintains a registry of query types and their corresponding
    handlers, enabling dynamic routing and execution of queries.
    """

    def __init__(self):
        """Initialize the query bus with an empty handler registry."""
        self._handlers: Dict[Type[Query], QueryHandler] = {}

    def register_handler(
        self, query_type: Type[TQuery], handler: QueryHandler[TQuery, Any]
    ) -> None:
        """
        Register a query handler for a specific query type.

        Args:
            query_type: The query class type
            handler: The handler instance for this query type
        """
        self._handlers[query_type] = handler

    async def execute(self, query: TQuery) -> Any:
        """
        Execute a query by routing it to the appropriate handler.

        Args:
            query: The query instance to execute

        Returns:
            Any: The result returned by the query handler

        Raises:
            ValueError: If no handler is registered for the query type
        """
        query_type = type(query)
        if query_type not in self._handlers:
            raise ValueError(f"No handler registered for query type: {query_type}")

        handler = self._handlers[query_type]
        return await handler.handle(query)

    async def send(self, query: Query) -> Any:
        """
        Send a query to its handler (alias for execute method).

        Args:
            query: The query instance to send

        Returns:
            Any: The result returned by the query handler
        """
        return await self.execute(query)
