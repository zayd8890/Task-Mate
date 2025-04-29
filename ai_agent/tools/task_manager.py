# tools/task_manager.py - Task management integration for SmolaGent

import sys
import os
import yaml
from typing import Dict, List, Any, Optional, Union
from task_management.ai_ml_logic import scheduling, task_decomposition, task_prioritization, visualization
from task_management.utils import *
from task_management.scripts import scripts

class TaskManagerTool:
    """Tool for managing tasks with scheduling, decomposition, and prioritization"""
    
    def __init__(self):
        """Initialize the task management tool"""
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML files"""
        config = {}
        
        # Load settings
        settings_path = os.path.join("task_management", "config", "settings.yaml")
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                config.update(yaml.safe_load(f) or {})
        
        # Load API keys (if needed)
        api_keys_path = os.path.join("task_management", "config", "api_keys.yaml")
        if os.path.exists(api_keys_path):
            with open(api_keys_path, 'r') as f:
                config["api_keys"] = yaml.safe_load(f) or {}
        
        return config

    def decompose_task(self, task_description: str, complexity_level: int = 1) -> List[Dict[str, str]]:
        """
        Decompose a complex task into smaller, manageable subtasks.
        
        Args:
            task_description: Description of the main task
            complexity_level: Level of detail for decomposition (1-3)
            
        Returns:
            List of subtasks with descriptions
        """
        try:
            # Call your existing task_decomposition module
            return task_decomposition.decompose_task(task_description, complexity_level)
        except Exception as e:
            return [{"error": f"Failed to decompose task: {str(e)}"}]

    def prioritize_tasks(self, tasks: List[Dict[str, Any]], criteria: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """
        Prioritize a list of tasks based on specified criteria.
        
        Args:
            tasks: List of task dictionaries
            criteria: Dictionary of criteria weights (optional)
            
        Returns:
            Prioritized list of tasks
        """
        try:
            # Default criteria if none provided
            if criteria is None:
                criteria = {
                    "urgency": 0.3,
                    "importance": 0.4,
                    "effort": 0.2,
                    "dependencies": 0.1
                }
            
            # Call your existing task_prioritization module
            return task_prioritization.prioritize_tasks(tasks, criteria)
        except Exception as e:
            return [{"error": f"Failed to prioritize tasks: {str(e)}"}]

    def schedule_tasks(self, tasks: List[Dict[str, Any]], time_frame: str = "today") -> Dict[str, Any]:
        """
        Generate a schedule for tasks within the specified time frame.
        
        Args:
            tasks: List of task dictionaries
            time_frame: Time frame for scheduling ("today", "week", "month")
            
        Returns:
            Scheduled tasks with time slots
        """
        try:
            # Call your existing scheduling module
            return scheduling.create_schedule(tasks, time_frame)
        except Exception as e:
            return {"error": f"Failed to schedule tasks: {str(e)}"}

    def visualize_tasks(self, data: Dict[str, Any], viz_type: str = "gantt") -> str:
        """
        Generate a visualization of tasks.
        
        Args:
            data: Task data to visualize
            viz_type: Type of visualization ("gantt", "kanban", "timeline")
            
        Returns:
            Path to the generated visualization or base64 image data
        """
        try:
            # Call your existing visualization module
            return visualization.create_visualization(data, viz_type)
        except Exception as e:
            return f"Error generating visualization: {str(e)}"

    def run_script(self, script_name: str, params: Dict[str, Any] = None) -> Any:
        """
        Run a predefined script from the task management system.
        
        Args:
            script_name: Name of the script to run
            params: Parameters to pass to the script
            
        Returns:
            Script execution result
        """
        try:
            # Call your existing scripts module
            if not params:
                params = {}
            
            script_func = getattr(scripts, script_name, None)
            if not script_func:
                return f"Error: Script '{script_name}' not found"
            
            return script_func(**params)
        except Exception as e:
            return f"Error running script: {str(e)}"


# Functions to expose to the agent
def decompose_task(task_description: str, complexity_level: int = 1) -> List[Dict[str, str]]:
    """
    Decompose a complex task into smaller, manageable subtasks.
    
    Args:
        task_description: Description of the main task
        complexity_level: Level of detail for decomposition (1-3)
        
    Returns:
        List of subtasks with descriptions
    """
    tool = TaskManagerTool()
    return tool.decompose_task(task_description, complexity_level)

def prioritize_tasks(tasks: List[Dict[str, Any]], criteria: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
    """
    Prioritize a list of tasks based on specified criteria.
    
    Args:
        tasks: List of task dictionaries
        criteria: Dictionary of criteria weights (optional)
        
    Returns:
        Prioritized list of tasks
    """
    tool = TaskManagerTool()
    return tool.prioritize_tasks(tasks, criteria)

def schedule_tasks(tasks: List[Dict[str, Any]], time_frame: str = "today") -> Dict[str, Any]:
    """
    Generate a schedule for tasks within the specified time frame.
    
    Args:
        tasks: List of task dictionaries
        time_frame: Time frame for scheduling ("today", "week", "month")
        
    Returns:
        Scheduled tasks with time slots
    """
    tool = TaskManagerTool()
    return tool.schedule_tasks(tasks, time_frame)

def visualize_tasks(data: Dict[str, Any], viz_type: str = "gantt") -> str:
    """
    Generate a visualization of tasks.
    
    Args:
        data: Task data to visualize
        viz_type: Type of visualization ("gantt", "kanban", "timeline")
        
    Returns:
        Path to the generated visualization or base64 image data
    """
    tool = TaskManagerTool()
    return tool.visualize_tasks(data, viz_type)

def run_task_script(script_name: str, params: Dict[str, Any] = None) -> Any:
    """
    Run a predefined script from the task management system.
    
    Args:
        script_name: Name of the script to run
        params: Parameters to pass to the script
        
    Returns:
        Script execution result
    """
    tool = TaskManagerTool()
    return tool.run_script(script_name, params)