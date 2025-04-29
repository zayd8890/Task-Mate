# tests/test_integration.py
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent
from tools import calculator, task_manager

class TestIntegration:
    """Test suite for integration between agent and tools"""
    
    @pytest.fixture
    def agent(self):
        """Create a real agent with actual tools for integration testing"""
        return Agent(
            tools={
                "calculator": calculator.calculate,
                "decompose_task": task_manager.decompose_task
            }
        )
    
    @patch("task_management.ai_ml_logic.task_decomposition.decompose_task")
    @patch("openai.ChatCompletion.create")
    def test_agent_with_task_manager(self, mock_openai, mock_decompose, agent):
        """Test the integration between agent and task manager"""
        # Configure the mock response from OpenAI
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "I'll help decompose this task.\n```tool decompose_task\n{\"task_description\": \"Build a website\", \"complexity_level\": 2}\n```"
                    }
                }
            ]
        }
        
        # Configure the mock response from task_decomposition
        mock_decompose.return_value = [
            {"id": 1, "description": "Design wireframes"},
            {"id": 2, "description": "Create HTML structure"},
            {"id": 3, "description": "Style with CSS"},
            {"id": 4, "description": "Add JavaScript functionality"}
        ]
        
        # Process a message that should trigger the task manager
        result = agent.process("Decompose the task of building a website")
        
        # Verify the task_decomposition function was called with the correct arguments
        mock_decompose.assert_called_once_with("Build a website", 2)
        
        # Verify the response includes results from task decomposition
        assert "Design wireframes" in result
        assert "Create HTML structure" in result
        assert "Style with CSS" in result
        assert "Add JavaScript functionality" in result
