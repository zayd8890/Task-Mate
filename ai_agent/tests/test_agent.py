# tests/test_agent.py
import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the agent modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent

class TestAgent:
    """Test suite for the Agent class"""
    
    @pytest.fixture
    def mock_tools(self):
        """Create mock tools for testing"""
        return {
            "mock_tool": MagicMock(return_value="Mock tool result"),
            "calculator": MagicMock(return_value="42")
        }
    
    @pytest.fixture
    def agent(self, mock_tools):
        """Create an agent instance with mock tools"""
        return Agent(tools=mock_tools)
    
    @patch("openai.ChatCompletion.create")
    def test_process_basic_response(self, mock_openai, agent):
        """Test processing a basic response without tool calls"""
        # Configure mock OpenAI response
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response."
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        # Process a test message
        result = agent.process("Hello")
        
        # Verify the response
        assert result == "This is a test response."
        assert len(agent.conversation_history) == 2  # User input + assistant response
        assert agent.conversation_history[0]["role"] == "user"
        assert agent.conversation_history[1]["role"] == "assistant"
    
    @patch("openai.ChatCompletion.create")
    def test_process_with_tool_call(self, mock_openai, agent):
        """Test processing a response with a tool call"""
        # Configure mock OpenAI response with tool call
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "Let me calculate that for you.\n```tool calculator\n{\"expression\": \"2+2\"}\n```"
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        # Process a test message
        result = agent.process("What is 2+2?")
        
        # Verify the tool was called
        agent.tools["calculator"].assert_called_once_with(expression="2+2")
        
        # Verify the tool result was incorporated
        assert "42" in result
    
    def test_create_system_message(self, agent):
        """Test the creation of the system message"""
        system_message = agent._create_system_message()
        
        # Check that it's a dictionary with the correct role
        assert isinstance(system_message, dict)
        assert system_message["role"] == "system"
        
        # Check that it contains descriptions of our tools
        assert "Available tools" in system_message["content"]
        assert "mock_tool" in system_message["content"]
        assert "calculator" in system_message["content"]
    
    @patch("openai.ChatCompletion.create", side_effect=Exception("Test error"))
    def test_process_error_handling(self, mock_openai, agent):
        """Test error handling in the process method"""
        # Process a message that will cause an error
        result = agent.process("This will cause an error")
        
        # Verify error handling
        assert "Error processing request" in result
        assert "Test error" in result









