# tests/test_dependencies.py
import pytest
from ai_ml_logic.task_prioritization import resolve_dependencies

def test_resolve_dependencies():
    tasks = [
        {"id": 1, "description": "Task 1", "dependencies": []},
        {"id": 2, "description": "Task 2", "dependencies": [1]},
    ]
    ordered_tasks = resolve_dependencies(tasks)
    
    # Check if tasks are ordered correctly
    assert ordered_tasks[0]["id"] == 1
    assert ordered_tasks[1]["id"] == 2

def test_circular_dependencies():
    tasks = [
        {"id": 1, "description": "Task 1", "dependencies": [2]},
        {"id": 2, "description": "Task 2", "dependencies": [1]},
    ]
    
    # Check if circular dependencies are detected
    with pytest.raises(ValueError, match="Circular dependencies detected!"):
        resolve_dependencies(tasks)