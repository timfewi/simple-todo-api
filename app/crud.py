"""
CRUD operations for Todo items.

This module contains database operations for creating, reading, updating,
and deleting Todo items using SQLAlchemy ORM.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.connection import TodoDB
from app.models.todo import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate) -> TodoDB:
    """
    Create a new todo item in the database.

    Args:
        db: Database session
        todo: Todo data for creation

    Returns:
        TodoDB: Created todo item
    """
    db_todo = TodoDB(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        priority=todo.priority,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def get_todo(db: Session, todo_id: int) -> Optional[TodoDB]:
    """
    Retrieve a single todo item by ID.

    Args:
        db: Database session
        todo_id: ID of the todo to retrieve

    Returns:
        TodoDB or None: Todo item if found, None otherwise
    """
    return db.query(TodoDB).filter(TodoDB.id == todo_id).first()


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
) -> List[TodoDB]:
    """
    Retrieve multiple todo items with optional filtering and pagination.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        completed: Filter by completion status (optional)
        priority: Filter by priority level (optional)

    Returns:
        List[TodoDB]: List of todo items
    """
    query = db.query(TodoDB)

    # Apply filters if provided
    if completed is not None:
        query = query.filter(TodoDB.completed == completed)

    if priority is not None:
        query = query.filter(TodoDB.priority == priority)

    # Order by creation date (newest first) and apply pagination
    return query.order_by(TodoDB.created_at.desc()).offset(skip).limit(limit).all()


def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoDB]:
    """
    Update an existing todo item.

    Args:
        db: Database session
        todo_id: ID of the todo to update
        todo_update: Updated todo data

    Returns:
        TodoDB or None: Updated todo item if found, None otherwise
    """
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not db_todo:
        return None

    # Update only provided fields
    update_data = todo_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_todo, field, value)

    # The updated_at timestamp will be automatically updated by SQLAlchemy
    # due to the onupdate parameter in the model definition

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """
    Delete a todo item from the database.

    Args:
        db: Database session
        todo_id: ID of the todo to delete

    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not db_todo:
        return False

    db.delete(db_todo)
    db.commit()

    return True


def get_todos_count(
    db: Session, completed: Optional[bool] = None, priority: Optional[str] = None
) -> int:
    """
    Get the total count of todos matching the given filters.

    Args:
        db: Database session
        completed: Filter by completion status (optional)
        priority: Filter by priority level (optional)

    Returns:
        int: Total count of matching todos
    """
    query = db.query(TodoDB)

    if completed is not None:
        query = query.filter(TodoDB.completed == completed)

    if priority is not None:
        query = query.filter(TodoDB.priority == priority)

    return query.count()
