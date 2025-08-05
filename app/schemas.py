"""
API response schemas for the Todo API.

This module defines the structure of API responses, including
success responses, error responses, and paginated lists.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.models.todo import Todo


class TodoResponse(BaseModel):
    """Response schema for single todo operations."""

    success: bool = True
    message: str
    data: Optional[Todo] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Todo created successfully",
                "data": {
                    "id": 1,
                    "title": "Learn FastAPI",
                    "description": "Complete the FastAPI tutorial",
                    "completed": False,
                    "priority": "high",
                    "created_at": "2023-01-01T10:00:00",
                    "updated_at": "2023-01-01T10:00:00",
                },
            }
        }


class TodoListResponse(BaseModel):
    """Response schema for listing todos with pagination."""

    success: bool = True
    message: str
    data: List[Todo]
    pagination: dict

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Todos retrieved successfully",
                "data": [
                    {
                        "id": 1,
                        "title": "Learn FastAPI",
                        "description": "Complete the FastAPI tutorial",
                        "completed": False,
                        "priority": "high",
                        "created_at": "2023-01-01T10:00:00",
                        "updated_at": "2023-01-01T10:00:00",
                    }
                ],
                "pagination": {
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1,
                },
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for error cases."""

    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Todo not found",
                "error_code": "TODO_NOT_FOUND",
                "details": {"todo_id": 999},
            }
        }
