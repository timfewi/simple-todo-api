"""
Todo-related queries for CQRS implementation.

Queries represent operations that read data without changing state.
They contain filtering, sorting, and pagination parameters.
"""

from typing import Optional

from pydantic import BaseModel, Field

from app.cqrs.base import Query


class GetTodoQuery(Query):
    """
    Query to get a single todo by ID.

    Simple query that retrieves one todo item.
    """

    todo_id: int = Field(..., gt=0, description="ID of the todo to retrieve")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"todo_id": 1}}


class GetTodoListQuery(Query):
    """
    Query to get a list of todos with filtering and pagination.

    This query encapsulates all the parameters needed for listing todos,
    including filters, sorting, and pagination.
    """

    # Pagination
    skip: int = Field(0, ge=0, description="Number of todos to skip")
    limit: int = Field(
        10, ge=1, le=100, description="Maximum number of todos to return"
    )

    # Filters
    completed: Optional[bool] = Field(None, description="Filter by completion status")
    priority: Optional[str] = Field(
        None, pattern="^(low|medium|high)$", description="Filter by priority"
    )
    search: Optional[str] = Field(None, description="Search in title and description")

    # Sorting
    sort_by: str = Field("updated_at", description="Sort by field")
    sort_desc: bool = Field(True, description="Sort descending")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "skip": 0,
                "limit": 10,
                "completed": False,
                "priority": "high",
                "search": "important task",
                "sort_by": "updated_at",
                "sort_desc": True,
            }
        }


class GetTodosCountQuery(Query):
    """
    Query to get count of todos with filtering.

    Used for pagination calculations.
    """

    completed: Optional[bool] = Field(None, description="Filter by completion status")
    priority: Optional[str] = Field(
        None, pattern="^(low|medium|high)$", description="Filter by priority"
    )
    search: Optional[str] = Field(None, description="Search in title and description")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "completed": False,
                "priority": "high",
                "search": "important task",
            }
        }
