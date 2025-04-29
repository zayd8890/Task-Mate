# task_prioritization.py
from datetime import datetime
from dateutil.parser import parse
from collections import defaultdict, deque

# Default weights for task types
DEFAULT_WEIGHTS = {
    "work": 0.8,
    "personal": 0.5,
    "health": 0.7,
    "other": 0.6,
}

def auto_assign_weight(task_description, deadline=None, task_type=None, user_weights=None):
    """
    Auto-assigns a weight (priority) to a task based on its deadline, type, and user preferences.

    Args:
        task_description (str): Description of the task.
        deadline (str or datetime): Deadline of the task (optional). If provided as a string,
                                   it will be parsed into a datetime object.
        task_type (str): Type of task (e.g., "work", "personal") (optional). If not provided,
                         the default weight for "other" tasks will be used.
        user_weights (dict): Custom weights for task types (optional). If not provided,
                             default weights will be used.

    Returns:
        float: Priority weight (0 to 1, where 1 is highest priority).

    Example:
        >>> auto_assign_weight("Prepare for exam", "2023-11-10", "work")
        0.8
    """

    # Use user-defined weights if provided, otherwise use defaults
    weights = user_weights if user_weights else {"work": 0.8, "personal": 0.5, "other": 0.6}
    
    # Ensure the weights dictionary has a default key ("other")
    if "other" not in weights:
        weights["other"] = 0.6
    
    # Base weight based on task type
    base_weight = weights.get(task_type, weights["other"])
    
    # Adjust weight based on deadline
    if deadline:
        if isinstance(deadline, str):
            deadline = parse(deadline)  # Convert string to datetime
        days_until_deadline = (deadline - datetime.now()).days
        if days_until_deadline < 0:
            deadline_factor = 1.0  # Task is overdue
        else:
            deadline_factor = 1 / (days_until_deadline + 1)  # +1 to avoid division by zero
    else:
        deadline_factor = 1.0  # No deadline, use base weight directly
    
    # Adjust weight based on task description (simple NLP)
    urgent_keywords = ["urgent", "asap", "important", "deadline"]
    if any(keyword in task_description.lower() for keyword in urgent_keywords):
        description_factor = 1.5  # Increase priority for urgent tasks
    else:
        description_factor = 1.0
    
    # Final weight calculation
    weight = base_weight * deadline_factor * description_factor
    
    # Normalize weight to a range of 0 to 1
    weight = max(0, min(1, weight))
    
    return weight
def resolve_dependencies(tasks):
    """
    Resolves task dependencies and returns tasks in the correct order using topological sorting.
    Detects and raises an error if circular dependencies are found.

    Args:
        tasks (list): List of tasks, where each task is a dict with "id" and "dependencies".

    Returns:
        list: Tasks in the correct order.

    Raises:
        ValueError: If circular dependencies are detected.

    Example:
        >>> tasks = [
        ...     {"id": 1, "description": "Task 1", "dependencies": []},
        ...     {"id": 2, "description": "Task 2", "dependencies": [1]},
        ... ]
        >>> resolve_dependencies(tasks)
        [{"id": 1, "description": "Task 1", "dependencies": []},
         {"id": 2, "description": "Task 2", "dependencies": [1]}]
    """

    # Build a graph and in-degree count
    graph = defaultdict(list)
    in_degree = {task["id"]: 0 for task in tasks}
    
    for task in tasks:
        for dependency in task["dependencies"]:
            graph[dependency].append(task["id"])
            in_degree[task["id"]] += 1
    
    # Topological sort using Kahn's algorithm
    queue = deque([task["id"] for task in tasks if in_degree[task["id"]] == 0])
    ordered_tasks = []
    
    while queue:
        task_id = queue.popleft()
        ordered_tasks.append(task_id)
        
        for dependent in graph[task_id]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    # Check for circular dependencies
    if len(ordered_tasks) != len(tasks):
        raise ValueError("Circular dependencies detected!")
    
    # Map task IDs back to task details
    task_map = {task["id"]: task for task in tasks}
    return [task_map[task_id] for task_id in ordered_tasks]