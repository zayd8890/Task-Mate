# tests/integration/test_circular_dependencies.py
import pytest
from ai_ml_logic.task_prioritization import resolve_dependencies

def test_circular_dependencies():
    tasks = [
        {"id": 1, "description": "Task 1", "dependencies": [2]},
        {"id": 2, "description": "Task 2", "dependencies": [1]},
    ]
    
    # Check if circular dependencies are detected
    with pytest.raises(ValueError, match="Circular dependencies detected!"):
        resolve_dependencies(tasks)