# main.py
from ai_ml_logic.task_prioritization import auto_assign_weight

# Example tasks
tasks = [
    {"description": "Prepare for math exam", "deadline": "2023-11-10", "type": "work"},
    {"description": "Go for a run", "deadline": "2023-10-25", "type": "health"},
    {"description": "Buy groceries", "deadline": "2023-10-26", "type": "personal"},
]

# User-defined weights
user_weights = {
    "work": 0.9,
    "health": 0.8,
    "personal": 0.4,
}

# Assign weights to tasks
for task in tasks:
    weight = auto_assign_weight(
        task["description"],
        task.get("deadline"),
        task.get("type"),
        user_weights
    )
    print(f"Task: {task['description']}, Priority: {weight:.2f}")