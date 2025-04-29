# # ai_ml_logic/task_decomposition.py
# from datetime import datetime, timedelta
# from dateutil.parser import parse

# def decompose_task(task_description, deadline=None, task_type=None):
#     """
#     Breaks down a large task into smaller subtasks.
    
#     Args:
#         task_description (str): Description of the task.
#         deadline (str or datetime): Deadline of the task (optional).
#         task_type (str): Type of task (e.g., "work", "personal") (optional).
    
#     Returns:
#         list: List of subtasks with descriptions and deadlines.
#     """
#     # Rule-based decomposition for common tasks
#     if "exam" in task_description.lower():
#         subtasks = [
#             {"description": "Review chapter 1", "deadline": None},
#             {"description": "Review chapter 2", "deadline": None},
#             {"description": "Solve practice problems", "deadline": None},
#             {"description": "Take mock test", "deadline": None},
#         ]
#     elif "report" in task_description.lower():
#         subtasks = [
#             {"description": "Write outline", "deadline": None},
#             {"description": "Write draft", "deadline": None},
#             {"description": "Review and edit", "deadline": None},
#             {"description": "Submit report", "deadline": None},
#         ]
#     else:
#         # Default decomposition for generic tasks
#         subtasks = [
#             {"description": task_description, "deadline": deadline}
#         ]
    
#     # Assign deadlines to subtasks if a deadline is provided
#     if deadline:
#         if isinstance(deadline, str):
#             deadline = parse(deadline)  # Convert string to datetime
        
#         # Distribute subtasks evenly over the available time
#         num_subtasks = len(subtasks)
#         time_per_subtask = (deadline - datetime.now()) / num_subtasks
        
#         for i, subtask in enumerate(subtasks):
#             subtask["deadline"] = deadline - (num_subtasks - i - 1) * time_per_subtask
    
#     return subtasks