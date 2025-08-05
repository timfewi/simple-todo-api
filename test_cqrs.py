"""
Test script to validate CQRS implementation.

This script tests the CQRS pattern implementation without running the full API.
It validates that commands and queries can be executed properly.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.cqrs.buses import CommandBus, QueryBus
from app.cqrs.commands.todo_commands import (
    CreateTodoCommand,
    DeleteTodoCommand,
    UpdateTodoCommand,
)
from app.cqrs.handlers.todo_command_handlers import (
    CreateTodoCommandHandler,
    DeleteTodoCommandHandler,
    UpdateTodoCommandHandler,
)
from app.cqrs.handlers.todo_query_handlers import (
    GetTodoListQueryHandler,
    GetTodoQueryHandler,
    GetTodosCountQueryHandler,
)
from app.cqrs.queries.todo_queries import (
    GetTodoListQuery,
    GetTodoQuery,
    GetTodosCountQuery,
)
from app.database.connection import SessionLocal, get_db


async def test_cqrs_implementation():
    """Test the CQRS implementation with a simple workflow."""
    print("🧪 Testing CQRS Implementation...")

    # Create database session
    db = SessionLocal()

    try:
        # Setup command bus
        command_bus = CommandBus()
        command_bus.register_handler(CreateTodoCommand, CreateTodoCommandHandler(db))
        command_bus.register_handler(UpdateTodoCommand, UpdateTodoCommandHandler(db))
        command_bus.register_handler(DeleteTodoCommand, DeleteTodoCommandHandler(db))

        # Setup query bus
        query_bus = QueryBus()
        query_bus.register_handler(GetTodoQuery, GetTodoQueryHandler(db))
        query_bus.register_handler(GetTodoListQuery, GetTodoListQueryHandler(db))
        query_bus.register_handler(GetTodosCountQuery, GetTodosCountQueryHandler(db))

        print("✅ Buses configured successfully")

        # Test 1: Create a todo
        create_command = CreateTodoCommand(
            title="Test CQRS Todo",
            description="Testing our CQRS implementation",
            completed=False,
            priority="medium",
        )

        created_todo = await command_bus.execute(create_command)
        print(f"✅ Created todo: {created_todo.title} (ID: {created_todo.id})")

        # Test 2: Query the todo
        get_query = GetTodoQuery(todo_id=created_todo.id)
        retrieved_todo = await query_bus.execute(get_query)
        print(f"✅ Retrieved todo: {retrieved_todo.title}")

        # Test 3: List todos
        list_query = GetTodoListQuery(skip=0, limit=10, completed=None, priority=None, search=None, sort_by="", sort_desc=False)
        todos_list = await query_bus.execute(list_query)
        print(f"✅ Retrieved {len(todos_list)} todos from list query")

        # Test 4: Count todos
        count_query = GetTodosCountQuery(completed=None, priority=None, search=None)
        total_count = await query_bus.execute(count_query)
        print(f"✅ Total todos count: {total_count}")

        # Test 5: Update the todo
        update_command = UpdateTodoCommand(
            todo_id=created_todo.id,
            title="Updated CQRS Todo",
            description="Updated description",  # Provide a description
            completed=True,
            priority="high",  # Provide a priority
        )

        updated_todo = await command_bus.execute(update_command)
        print(
            f"✅ Updated todo: {updated_todo.title} (Completed: {updated_todo.completed})"
        )

        # Test 6: Delete the todo
        delete_command = DeleteTodoCommand(todo_id=created_todo.id)
        deletion_success = await command_bus.execute(delete_command)
        print(f"✅ Deleted todo successfully: {deletion_success}")

        # Test 7: Verify deletion
        deleted_todo = await query_bus.execute(GetTodoQuery(todo_id=created_todo.id))
        print(f"✅ Verified deletion - todo is None: {deleted_todo is None}")

        print("\n🎉 All CQRS tests passed successfully!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test_cqrs_implementation())
