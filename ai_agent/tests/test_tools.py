# tests/test_tools.py
import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the tool modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tools modules
from tools import calculator, file_operations

class TestCalculator:
    """Test suite for the calculator tool"""
    
    def test_calculate_basic_operations(self):
        """Test basic arithmetic operations"""
        assert calculator.calculate("2 + 2") == "4"
        assert calculator.calculate("10 - 5") == "5"
        assert calculator.calculate("3 * 4") == "12"
        assert calculator.calculate("20 / 5") == "4.0"
    
    def test_calculate_complex_expressions(self):
        """Test more complex mathematical expressions"""
        assert calculator.calculate("(2 + 3) * 4") == "20"
        assert calculator.calculate("10 / 2 + 5") == "10.0"
    
    def test_calculate_math_functions(self):
        """Test math module functions"""
        assert calculator.calculate("pow(2, 3)") == "8"
        assert calculator.calculate("round(3.14159, 2)") == "3.14"
    
    def test_calculate_input_validation(self):
        """Test input validation for security"""
        # This should be rejected as it contains invalid characters
        result = calculator.calculate("__import__('os').system('echo hacked')")
        assert "Error" in result
        assert "Invalid characters" in result


class TestFileOperations:
    """Test suite for the file operations tools"""
    
    @pytest.fixture
    def temp_file(self, tmp_path):
        """Create a temporary file for testing"""
        file_path = tmp_path / "test_file.txt"
        with open(file_path, "w") as f:
            f.write("Test content")
        return file_path
    
    def test_read_file(self, temp_file):
        """Test reading a file"""
        # Use the absolute path because of the security checks
        result = file_operations.read_file(str(temp_file))
        assert result == "Test content"
    
    def test_write_file(self, tmp_path):
        """Test writing to a file"""
        file_path = tmp_path / "write_test.txt"
        content = "New content"
        
        result = file_operations.write_file(str(file_path), content)
        assert "Successfully wrote to file" in result
        
        # Verify the file was written correctly
        with open(file_path, "r") as f:
            assert f.read() == content
    
    def test_directory_traversal_prevention(self, tmp_path):
        """Test prevention of directory traversal attacks"""
        # Try to access a file outside the working directory
        result = file_operations.read_file("../../../etc/passwd")
        assert "Error" in result
        assert "Access to files outside" in result