# tests/test_task_manager.py
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the task manager module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the task manager module
from tools import task_manager

class TestTaskManager:
    """Test suite for the task manager tool"""
    
    @pytest.fixture
    def mock_task_decomposition(self):
        """Mock the task_decomposition module"""
        with patch("task_management.ai_ml_logic.task_decomposition") as mock:
            mock.decompose_task.return_value = [
                {"id": 1, "description": "Subtask 1"},
                {"id": 2, "description": "Subtask 2"}
            ]
            yield mock
    
    @pytest.fixture
    def mock_task_prioritization(self):
        """Mock the task_prioritization module"""
        with patch("task_management.ai_ml_logic.task_prioritization") as mock:
            mock.prioritize_tasks.return_value = [
                {"id": 2, "description": "Subtask 2", "priority": "high"},
                {"id": 1, "description": "Subtask 1", "priority": "medium"}
            ]
            yield mock
    
    @pytest.fixture
    def mock_scheduling(self):
        """Mock the scheduling module"""
        with patch("task_management.ai_ml_logic.scheduling") as mock:
            mock.create_schedule.return_value = {
                "schedule": [
                    {"task_id": 2, "start_time": "09:00", "end_time": "10:00"},
                    {"task_id": 1, "start_time": "10:30", "end_time": "12:00"}
                ]
            }
            yield mock
    
    @pytest.fixture
    def mock_visualization(self):
        """Mock the visualization module"""
        with patch("task_management.ai_ml_logic.visualization") as mock:
            mock.create_visualization.return_value = "/path/to/visualization.png"
            yield mock
    
    @pytest.fixture
    def mock_scripts(self):
        """Mock the scripts module"""
        with patch("task_management.scripts.scripts") as mock:
            mock.generate_report.return_value = {"status": "success", "report_path": "/path/to/report.pdf"}
            yield mock
    
    @pytest.fixture
    def mock_yaml(self):
        """Mock the yaml module for config loading"""
        with patch("yaml.safe_load") as mock:
            mock.return_value = {"setting1": "value1", "setting2": "value2"}
            yield mock
    
    def test_decompose_task(self, mock_task_decomposition):
        """Test task decomposition"""
        result = task_manager.decompose_task("Create a marketing campaign", 2)
        
        # Verify the correct function was called with correct args
        mock_task_decomposition.decompose_task.assert_called_once_with("Create a marketing campaign", 2)
        
        # Verify the result
        assert len(result) == 2
        assert result[0]["description"] == "Subtask 1"
        assert result[1]["description"] == "Subtask 2"
    
    def test_prioritize_tasks(self, mock_task_prioritization):
        """Test task prioritization"""
        tasks = [
            {"id": 1, "description": "Subtask 1"},
            {"id": 2, "description": "Subtask 2"}
        ]
        criteria = {"urgency": 0.5, "importance": 0.5}
        
        result = task_manager.prioritize_tasks(tasks, criteria)
        
        # Verify the correct function was called with correct args
        mock_task_prioritization.prioritize_tasks.assert_called_once_with(tasks, criteria)
        
        # Verify the result
        assert len(result) == 2
        assert result[0]["priority"] == "high"
        assert result[1]["priority"] == "medium"
    
    def test_schedule_tasks(self, mock_scheduling):
        """Test task scheduling"""
        tasks = [
            {"id": 1, "description": "Subtask 1"},
            {"id": 2, "description": "Subtask 2"}
        ]
        
        result = task_manager.schedule_tasks(tasks, "today")
        
        # Verify the correct function was called with correct args
        mock_scheduling.create_schedule.assert_called_once_with(tasks, "today")
        
        # Verify the result
        assert "schedule" in result
        assert len(result["schedule"]) == 2
    
    def test_visualize_tasks(self, mock_visualization):
        """Test task visualization"""
        data = {"tasks": [{"id": 1, "description": "Task 1"}]}
        
        result = task_manager.visualize_tasks(data, "gantt")
        
        # Verify the correct function was called with correct args
        mock_visualization.create_visualization.assert_called_once_with(data, "gantt")
        
        # Verify the result
        assert result == "/path/to/visualization.png"
    
    def test_run_task_script(self, mock_scripts):
        """Test running a task script"""
        params = {"project": "Alpha"}
        
        result = task_manager.run_task_script("generate_report", params)
        
        # Verify the script was called with the correct parameters
        mock_scripts.generate_report.assert_called_once_with(project="Alpha")
        
        # Verify the result
        assert result["status"] == "success"
        assert result["report_path"] == "/path/to/report.pdf"
    
    def test_error_handling(self, mock_task_decomposition):
        """Test error handling in task manager"""
        # Make the mock raise an exception
        mock_task_decomposition.decompose_task.side_effect = Exception("Test error")
        
        result = task_manager.decompose_task("Create a marketing campaign")
        
        # Verify error handling
        assert len(result) == 1
        assert "error" in result[0]
        assert "Test error" in result[0]["error"]
