# tests/test_scheduling.py
import pytest
from datetime import datetime, timedelta
from ai_ml_logic.scheduling import create_schedule

def test_create_schedule():
    tasks = [
        {"description": "Task 1", "deadline": "2023-11-01", "type": "work"},
        {"description": "Task 2", "deadline": "2023-11-02", "type": "work"},
    ]
    start_date = "2023-10-25"
    schedule = create_schedule(tasks, start_date)
    
    # Check if tasks are scheduled correctly
    assert len(schedule) == 2
    assert schedule[0]["start_time"].strftime("%Y-%m-%d") == "2023-10-25"
    assert schedule[1]["start_time"].strftime("%Y-%m-%d") == "2023-10-25"

def test_create_schedule_recurring_tasks():
    tasks = [
        {"description": "Task 1", "deadline": "2023-11-01", "type": "work"},
    ]
    recurring_tasks = [
        {"description": "Daily standup", "type": "work", "frequency": "daily"},
    ]
    start_date = "2023-10-25"
    schedule = create_schedule(tasks, start_date, recurring_tasks=recurring_tasks)
    
    # Check if recurring tasks are included
    assert len(schedule) == 2
    assert schedule[1]["description"] == "Daily standup"