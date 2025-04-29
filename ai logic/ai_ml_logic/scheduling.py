# ai_ml_logic/scheduling.py
from datetime import datetime, timedelta

def create_schedule(tasks, start_date, hours_per_day=8, recurring_tasks=None):
    """
    Creates a schedule for tasks, including recurring tasks.

    Args:
        tasks (list): List of tasks to schedule. Each task is a dict with "description",
                      "deadline", and "type".
        start_date (str or datetime): Start date for the schedule. If provided as a string,
                                      it will be parsed into a datetime object.
        hours_per_day (int): Number of working hours per day (default: 8).
        recurring_tasks (list): List of recurring tasks (optional). Each recurring task is a
                                dict with "description", "type", and "frequency".

    Returns:
        list: Scheduled tasks with "start_time" and "end_time" added.

    Example:
        >>> tasks = [
        ...     {"description": "Task 1", "deadline": "2023-11-01", "type": "work"},
        ...     {"description": "Task 2", "deadline": "2023-11-02", "type": "work"},
        ... ]
        >>> create_schedule(tasks, "2023-10-25")
        [{"description": "Task 1", "deadline": "2023-11-01", "type": "work",
          "start_time": datetime(2023, 10, 25, 9, 0), "end_time": datetime(2023, 10, 25, 11, 0)},
         {"description": "Task 2", "deadline": "2023-11-02", "type": "work",
          "start_time": datetime(2023, 10, 25, 11, 0), "end_time": datetime(2023, 10, 25, 13, 0)}]
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    schedule = []
    current_time = start_date
    
    # Schedule non-recurring tasks
    for task in tasks:
        task["start_time"] = current_time
        task["end_time"] = current_time + timedelta(hours=2)  # Assume 2 hours per task
        schedule.append(task)
        current_time = task["end_time"]
        
        # Move to the next day if working hours are exceeded
        if current_time.hour >= 17:  # Assuming workday ends at 5 PM
            current_time = current_time.replace(hour=9, minute=0) + timedelta(days=1)
    
    # Schedule recurring tasks
    if recurring_tasks:
        for task in recurring_tasks:
            task["start_time"] = current_time
            task["end_time"] = current_time + timedelta(hours=2)
            schedule.append(task)
            current_time = task["end_time"]
            
            if current_time.hour >= 17:
                current_time = current_time.replace(hour=9, minute=0) + timedelta(days=1)
    
    return schedule