"""
API routes for Todo operations.

This module defines all the HTTP endpoints for the Todo API,
including CRUD operations with proper error handling and response formatting.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database.connection import get_db
from app.models.todo import Todo, TodoCreate, TodoUpdate
from app.schemas import ErrorResponse, TodoListResponse, TodoResponse

# Create API router
router = APIRouter()


@router.get("/todos", response_model=TodoListResponse)
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of todos to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of todos to return"
    ),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(
        None, regex="^(low|medium|high)$", description="Filter by priority"
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of todos with optional filtering and pagination.

    Args:
        skip: Number of todos to skip (pagination)
        limit: Maximum number of todos to return
        completed: Filter by completion status (optional)
        priority: Filter by priority level (optional)
        db: Database session

    Returns:
        TodoListResponse: List of todos with pagination information
    """
    # Get todos and total count
    todos = crud.get_todos(
        db, skip=skip, limit=limit, completed=completed, priority=priority
    )
    total_count = crud.get_todos_count(db, completed=completed, priority=priority)

    # Calculate pagination info
    total_pages = (total_count + limit - 1) // limit
    current_page = (skip // limit) + 1

    return TodoListResponse(
        message="Todos retrieved successfully",
        data=[Todo.model_validate(todo) for todo in todos],
        pagination={
            "total": total_count,
            "page": current_page,
            "page_size": limit,
            "total_pages": total_pages,
        },
    )


@router.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item.

    Args:
        todo: Todo data for creation
        db: Database session

    Returns:
        TodoResponse: Created todo item
    """
    db_todo = crud.create_todo(db=db, todo=todo)

    return TodoResponse(
        message="Todo created successfully", data=Todo.model_validate(db_todo)
    )


@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=200)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific todo item by ID.

    Args:
        todo_id: ID of the todo to retrieve
        db: Database session

    Returns:
        TodoResponse: Todo item

    Raises:
        HTTPException: If todo not found
    """
    db_todo = crud.get_todo(db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                message="Todo not found",
                error_code="TODO_NOT_FOUND",
                details={"todo_id": todo_id},
            ).dict(),
        )

    return TodoResponse(
        message="Todo retrieved successfully", data=Todo.model_validate(db_todo)
    )


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing todo item.

    Args:
        todo_id: ID of the todo to update
        todo_update: Updated todo data
        db: Database session

    Returns:
        TodoResponse: Updated todo item

    Raises:
        HTTPException: If todo not found
    """
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo_update)

    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                message="Todo not found",
                error_code="TODO_NOT_FOUND",
                details={"todo_id": todo_id},
            ).model_dump(),
        )

    return TodoResponse(
        message="Todo updated successfully", data=Todo.from_orm(db_todo)
    )


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a todo item.

    Args:
        todo_id: ID of the todo to delete
        db: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If todo not found
    """
    success = crud.delete_todo(db, todo_id=todo_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                message="Todo not found",
                error_code="TODO_NOT_FOUND",
                details={"todo_id": todo_id},
            ).model_dump(),
        )

    return {"success": True, "message": "Todo deleted successfully"}
