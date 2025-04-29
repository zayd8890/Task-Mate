# tests/test_task_prioritization.py
import pytest
from datetime import datetime, timedelta
from ai_ml_logic.task_prioritization import auto_assign_weight

def test_auto_assign_weight_with_deadline():
    # Test task with a deadline
    task_description = "Prepare for math exam"
    deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    weight = auto_assign_weight(task_description, deadline, "work")
    assert 0 <= weight <= 1

def test_auto_assign_weight_without_deadline():
    # Test task without a deadline
    task_description = "Read a book"
    weight = auto_assign_weight(task_description, task_type="personal")
    assert weight == 0.5  # Default weight for tasks without deadlines

def test_auto_assign_weight_urgent_task():
    # Test task with urgent keywords
    task_description = "Finish urgent report ASAP"
    weight = auto_assign_weight(task_description, task_type="work")
    assert weight > 0.8  # Higher priority for urgent tasks

def test_auto_assign_weight_custom_weights():
    # Test task with custom weights
    task_description = "Go for a run"
    custom_weights = {"health": 0.9}
    weight = auto_assign_weight(task_description, task_type="health", user_weights=custom_weights)
    assert weight == 0.9  # Custom weight for health tasks