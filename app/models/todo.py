"""Pydantic models for the Todo API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Base Todo model with common fields shared across operations."""

    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(
        None, max_length=1000, description="Todo description"
    )
    completed: bool = Field(False, description="Whether the todo is completed")
    priority: str = Field(
        "medium", pattern="^(low|medium|high)$", description="Priority level"
    )


class TodoCreate(TodoBase):
    """Model for creating a new todo item."""

    pass


class TodoUpdate(BaseModel):
    """Model for updating an existing todo item."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class Todo(TodoBase):
    """Complete Todo model including database fields."""

    id: int = Field(..., description="Unique todo identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial and build a Todo API",
                "completed": False,
                "priority": "high",
                "created_at": "2023-01-01T10:00:00",
                "updated_at": "2023-01-01T10:00:00",
            }
        }
