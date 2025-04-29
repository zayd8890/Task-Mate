# tests/conftest.py
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def sample_tasks():
    """
    Provides a sample list of tasks for testing.

    Returns:
        list: Sample tasks with "id", "description", "deadline", "type", and "dependencies".

    Example:
        >>> tasks = sample_tasks()
        >>> tasks
        [{"id": 1, "description": "Task 1", "deadline": "2023-11-01", "type": "work", "dependencies": []},
         {"id": 2, "description": "Task 2", "deadline": "2023-11-02", "type": "work", "dependencies": [1]}]
    """
    return [
        {"id": 1, "description": "Task 1", "deadline": "2023-11-01", "type": "work", "dependencies": []},
        {"id": 2, "description": "Task 2", "deadline": "2023-11-02", "type": "work", "dependencies": [1]},
    ]