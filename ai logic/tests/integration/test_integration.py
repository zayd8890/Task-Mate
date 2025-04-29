# tests/integration/test_integration.py
import pytest
from ai_ml_logic.task_prioritization import auto_assign_weight, resolve_dependencies
from ai_ml_logic.scheduling import create_schedule

def test_end_to_end():
    tasks = [
        {"id": 1, "description": "Task 1", "deadline": "2023-11-01", "type": "work", "dependencies": []},
        {"id": 2, "description": "Task 2", "deadline": "2023-11-02", "type": "work", "dependencies": [1]},
    ]
    
    # Resolve dependencies
    ordered_tasks = resolve_dependencies(tasks)
    
    # Assign weights
    for task in ordered_tasks:
        task["priority"] = auto_assign_weight(task["description"], task.get("deadline"), task.get("type"))
    
    # Create schedule
    schedule = create_schedule(ordered_tasks, "2023-10-25")
    
    # Check if the schedule is created correctly
    assert len(schedule) == 2
    assert schedule[0]["description"] == "Task 1"
    assert schedule[1]["description"] == "Task 2"