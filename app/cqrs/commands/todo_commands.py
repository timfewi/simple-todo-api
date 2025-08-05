"""
Todo-related commands for CQRS implementation.

Commands represent operations that change the state of todos.
They contain all the data needed to perform the operation.
"""

from typing import Optional

from pydantic import BaseModel, Field

from app.cqrs.base import Command


class CreateTodoCommand(Command):
    """
    Command to create a new todo.

    This command encapsulates all the data needed to create a todo,
    including validation rules and business constraints.
    """

    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(
        None, max_length=1000, description="Todo description"
    )
    completed: bool = Field(False, description="Whether the todo is completed")
    priority: str = Field(
        "medium", pattern="^(low|medium|high)$", description="Priority level"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "title": "Learn CQRS pattern",
                "description": "Implement CQRS in FastAPI Todo application",
                "completed": False,
                "priority": "high",
            }
        }


class UpdateTodoCommand(Command):
    """
    Command to update an existing todo.

    Contains the todo ID and the fields to update.
    Only provided fields will be updated.
    """

    todo_id: int = Field(..., gt=0, description="ID of the todo to update")
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="New title"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="New description"
    )
    completed: Optional[bool] = Field(None, description="Completion status")
    priority: Optional[str] = Field(
        None, pattern="^(low|medium|high)$", description="New priority"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "todo_id": 1,
                "title": "Updated title",
                "priority": "high",
                "completed": True,
            }
        }


class DeleteTodoCommand(Command):
    """
    Command to delete a todo.

    Simple command that only requires the todo ID.
    """

    todo_id: int = Field(..., gt=0, description="ID of the todo to delete")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"todo_id": 1}}
