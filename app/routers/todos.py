"""
API routes for Todo operations using CQRS pattern.

This module defines all the HTTP endpoints for the Todo API,
using Command Query Responsibility Segregation (CQRS) for better separation
of concerns and improved maintainability.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.cqrs.buses import CommandBus, QueryBus
from app.cqrs.commands.todo_commands import (
    CreateTodoCommand,
    DeleteTodoCommand,
    UpdateTodoCommand,
)
from app.cqrs.dependencies import get_command_bus, get_query_bus
from app.cqrs.queries.todo_queries import (
    GetTodoListQuery,
    GetTodoQuery,
    GetTodosCountQuery,
)
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
        None, pattern="^(low|medium|high)$", description="Filter by priority"
    ),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: str = Query("updated_at", description="Sort by field"),
    sort_desc: bool = Query(True, description="Sort descending"),
    query_bus: QueryBus = Depends(get_query_bus),
):
    """
    Retrieve a list of todos with optional filtering and pagination.

    Args:
        skip: Number of todos to skip (pagination)
        limit: Maximum number of todos to return
        completed: Filter by completion status (optional)
        priority: Filter by priority level (optional)
        search: Search term for title and description (optional)
        sort_by: Field to sort by
        sort_desc: Sort in descending order
        query_bus: Query bus dependency

    Returns:
        TodoListResponse: List of todos with pagination information
    """
    # Create list query
    list_query = GetTodoListQuery(
        skip=skip,
        limit=limit,
        completed=completed,
        priority=priority,
        search=search,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )

    # Create count query
    count_query = GetTodosCountQuery(
        completed=completed,
        priority=priority,
        search=search,
    )

    # Execute queries
    todos = await query_bus.execute(list_query)
    total_count = await query_bus.execute(count_query)

    # Calculate pagination info
    total_pages = (total_count + limit - 1) // limit
    current_page = (skip // limit) + 1

    return TodoListResponse(
        message="Todos retrieved successfully",
        data=todos,
        pagination={
            "total": total_count,
            "page": current_page,
            "page_size": limit,
            "total_pages": total_pages,
        },
    )


@router.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate, command_bus: CommandBus = Depends(get_command_bus)
):
    """
    Create a new todo item.

    Args:
        todo: Todo data for creation
        command_bus: Command bus dependency

    Returns:
        TodoResponse: Created todo item

    Raises:
        HTTPException: If business rules are violated
    """
    # Create command
    command = CreateTodoCommand(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        priority=todo.priority,
    )

    try:
        # Execute command
        created_todo = await command_bus.execute(command)

        return TodoResponse(message="Todo created successfully", data=created_todo)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                message=str(e),
                error_code="BUSINESS_RULE_VIOLATION",
                details={"validation_error": str(e)},
            ).model_dump(),
        )


@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=200)
async def get_todo(todo_id: int, query_bus: QueryBus = Depends(get_query_bus)):
    """
    Retrieve a specific todo item by ID.

    Args:
        todo_id: ID of the todo to retrieve
        query_bus: Query bus dependency

    Returns:
        TodoResponse: Todo item

    Raises:
        HTTPException: If todo not found
    """
    # Create query
    query = GetTodoQuery(todo_id=todo_id)

    # Execute query
    todo = await query_bus.execute(query)

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                message="Todo not found",
                error_code="TODO_NOT_FOUND",
                details={"todo_id": todo_id},
            ).model_dump(),
        )

    return TodoResponse(message="Todo retrieved successfully", data=todo)


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    command_bus: CommandBus = Depends(get_command_bus),
):
    """
    Update an existing todo item.

    Args:
        todo_id: ID of the todo to update
        todo_update: Updated todo data
        command_bus: Command bus dependency

    Returns:
        TodoResponse: Updated todo item

    Raises:
        HTTPException: If todo not found or business rules violated
    """
    # Create command
    command = UpdateTodoCommand(
        todo_id=todo_id,
        title=todo_update.title,
        description=todo_update.description,
        completed=todo_update.completed,
        priority=todo_update.priority,
    )

    try:
        # Execute command
        updated_todo = await command_bus.execute(command)

        if updated_todo is None:
            raise HTTPException(
                status_code=404,
                detail=ErrorResponse(
                    message="Todo not found",
                    error_code="TODO_NOT_FOUND",
                    details={"todo_id": todo_id},
                ).model_dump(),
            )

        return TodoResponse(message="Todo updated successfully", data=updated_todo)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                message=str(e),
                error_code="BUSINESS_RULE_VIOLATION",
                details={"validation_error": str(e)},
            ).model_dump(),
        )


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, command_bus: CommandBus = Depends(get_command_bus)):
    """
    Delete a todo item.

    Args:
        todo_id: ID of the todo to delete
        command_bus: Command bus dependency

    Returns:
        dict: Success message

    Raises:
        HTTPException: If todo not found
    """
    # Create command
    command = DeleteTodoCommand(todo_id=todo_id)

    # Execute command
    success = await command_bus.execute(command)

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
