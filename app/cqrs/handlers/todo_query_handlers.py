"""
Query handlers for Todo operations.

Each query handler encapsulates the data retrieval logic for
a specific query. Handlers are responsible for database access,
filtering, and data transformation.
"""

from typing import List, Optional

from sqlalchemy import case
from sqlalchemy.orm import Session

from app.cqrs.base import QueryHandler
from app.cqrs.queries.todo_queries import (
    GetTodoListQuery,
    GetTodoQuery,
    GetTodosCountQuery,
)
from app.database.connection import TodoDB
from app.models.todo import Todo


class GetTodoQueryHandler(QueryHandler[GetTodoQuery, Optional[Todo]]):
    """
    Handler for retrieving a single todo by ID.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, query: GetTodoQuery) -> Optional[Todo]:
        """
        Handle single todo retrieval query.

        Args:
            query: Get todo query

        Returns:
            Todo or None: Todo entity if found
        """
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == query.todo_id).first()

        if not db_todo:
            return None

        return Todo.model_validate(db_todo)


class GetTodoListQueryHandler(QueryHandler[GetTodoListQuery, List[Todo]]):
    """
    Handler for retrieving a list of todos with filtering and pagination.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, query: GetTodoListQuery) -> List[Todo]:
        """
        Handle todo list retrieval query.

        Args:
            query: Get todo list query

        Returns:
            List[Todo]: List of todo entities
        """
        # Start with base query
        db_query = self.db.query(TodoDB)

        # Apply status filter
        if query.completed is not None:
            db_query = db_query.filter(TodoDB.completed == query.completed)

        # Apply priority filter
        if query.priority is not None:
            db_query = db_query.filter(TodoDB.priority == query.priority)

        # Apply search filter
        if query.search:
            search_term = f"%{query.search}%"
            db_query = db_query.filter(
                (TodoDB.title.ilike(search_term))
                | (TodoDB.description.ilike(search_term))
            )

        # Apply ordering
        if query.sort_by == "title":
            if query.sort_desc:
                db_query = db_query.order_by(TodoDB.title.desc())
            else:
                db_query = db_query.order_by(TodoDB.title.asc())
        elif query.sort_by == "priority":
            # Custom priority ordering: high > medium > low
            priority_case = case(
                (TodoDB.priority == "high", 3),
                (TodoDB.priority == "medium", 2),
                (TodoDB.priority == "low", 1),
                else_=0,
            )
            if query.sort_desc:
                db_query = db_query.order_by(priority_case.desc())
            else:
                db_query = db_query.order_by(priority_case.asc())
        elif query.sort_by == "created_at":
            if query.sort_desc:
                db_query = db_query.order_by(TodoDB.created_at.desc())
            else:
                db_query = db_query.order_by(TodoDB.created_at.asc())
        else:  # Default: updated_at
            if query.sort_desc:
                db_query = db_query.order_by(TodoDB.updated_at.desc())
            else:
                db_query = db_query.order_by(TodoDB.updated_at.asc())

        # Apply pagination
        db_query = db_query.offset(query.skip).limit(query.limit)

        # Execute query
        db_todos = db_query.all()

        # Convert to domain models
        return [Todo.model_validate(db_todo) for db_todo in db_todos]


class GetTodosCountQueryHandler(QueryHandler[GetTodosCountQuery, int]):
    """
    Handler for counting todos with optional filtering.
    """

    def __init__(self, db: Session):
        self.db = db

    async def handle(self, query: GetTodosCountQuery) -> int:
        """
        Handle todo count query.

        Args:
            query: Get todos count query

        Returns:
            int: Number of todos matching criteria
        """
        # Start with base query
        db_query = self.db.query(TodoDB)

        # Apply status filter
        if query.completed is not None:
            db_query = db_query.filter(TodoDB.completed == query.completed)

        # Apply priority filter
        if query.priority is not None:
            db_query = db_query.filter(TodoDB.priority == query.priority)

        # Apply search filter
        if query.search:
            search_term = f"%{query.search}%"
            db_query = db_query.filter(
                (TodoDB.title.ilike(search_term))
                | (TodoDB.description.ilike(search_term))
            )

        # Return count
        return db_query.count()
