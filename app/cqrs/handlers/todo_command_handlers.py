"""
Command handlers for Todo operations.

Each command handler encapsulates the business logic for processing
a specific command. Handlers are responsible for validation,
business rules, and coordinating with the database.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.cqrs.base import CommandHandler
from app.cqrs.commands.todo_commands import (
    CreateTodoCommand,
    DeleteTodoCommand,
    UpdateTodoCommand,
)
from app.database.connection import TodoDB
from app.models.todo import Todo


class CreateTodoCommandHandler(CommandHandler[CreateTodoCommand, Todo]):
    """
    Handler for creating new todos.

    Encapsulates business logic for todo creation including
    validation and automatic priority setting.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, command: CreateTodoCommand) -> Todo:
        """
        Handle todo creation command.

        Args:
            command: Create todo command

        Returns:
            Todo: Created todo entity

        Raises:
            ValueError: If business rules are violated
        """
        # Business rule: Check for duplicate titles
        existing_todo = (
            self.db.query(TodoDB)
            .filter(TodoDB.title.ilike(f"%{command.title}%"))
            .first()
        )

        if existing_todo:
            raise ValueError(
                f"A todo with similar title already exists: '{existing_todo.title}'"
            )

        # Business rule: Auto-escalate priority for urgent keywords
        priority = command.priority
        urgent_keywords = [
            "urgent",
            "asap",
            "emergency",
            "critical",
            "hotfix",
            "immediate",
        ]

        if any(keyword in command.title.lower() for keyword in urgent_keywords):
            priority = "high"

        # Create the database entity
        db_todo = TodoDB(
            title=command.title,
            description=command.description,
            completed=command.completed,
            priority=priority,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)

        # Convert to domain model
        return Todo.model_validate(db_todo)


class UpdateTodoCommandHandler(CommandHandler[UpdateTodoCommand, Optional[Todo]]):
    """
    Handler for updating existing todos.

    Encapsulates business logic for todo updates including
    validation and business rule enforcement.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, command: UpdateTodoCommand) -> Optional[Todo]:
        """
        Handle todo update command.

        Args:
            command: Update todo command

        Returns:
            Todo or None: Updated todo entity if found

        Raises:
            ValueError: If business rules are violated
        """
        # Find the todo
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == command.todo_id).first()

        if not db_todo:
            return None

        # Business rule: Can't modify completed todos older than 24 hours
        if (
            db_todo.completed is True
            and db_todo.updated_at is not None
            and (datetime.now(timezone.utc) - db_todo.updated_at).total_seconds()
            > 86400
        ):  # 24 hours
            raise ValueError("Cannot modify completed todos older than 24 hours")

        # Apply updates only for provided fields
        if command.title is not None:
            # Business rule: Check for duplicate titles (excluding current todo)
            existing_todo = (
                self.db.query(TodoDB)
                .filter(TodoDB.title.ilike(f"%{command.title}%"))
                .filter(TodoDB.id != command.todo_id)
                .first()
            )

            if existing_todo:
                raise ValueError(
                    f"A todo with similar title already exists: '{existing_todo.title}'"
                )

            db_todo.title = command.title  # type: ignore

        if command.description is not None:
            # Ensure description is properly truncated if too long
            if len(command.description) > 1000:
                raise ValueError("Description cannot exceed 1000 characters")
            db_todo.description = command.description  # type: ignore

        if command.priority is not None:
            db_todo.priority = command.priority  # type: ignore

        if command.completed is not None:
            db_todo.completed = command.completed  # type: ignore

        # Always update the timestamp
        db_todo.updated_at = datetime.now(timezone.utc)  # type: ignore

        self.db.commit()
        self.db.refresh(db_todo)

        return Todo.model_validate(db_todo)


class DeleteTodoCommandHandler(CommandHandler[DeleteTodoCommand, bool]):
    """
    Handler for deleting todos.

    Encapsulates business logic for todo deletion.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, command: DeleteTodoCommand) -> bool:
        """
        Handle todo deletion command.

        Args:
            command: Delete todo command

        Returns:
            bool: True if deleted successfully, False if not found
        """
        # Find the todo
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == command.todo_id).first()

        if not db_todo:
            return False

        # Perform the deletion
        self.db.delete(db_todo)
        self.db.commit()

        return True
