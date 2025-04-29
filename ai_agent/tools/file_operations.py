# tools/file_operations.py - File handling utilities
import os
import json

def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Contents of the file as a string
    """
    try:
        # Security check - prevent directory traversal
        abs_path = os.path.abspath(file_path)
        base_dir = os.path.abspath(os.getcwd())
        
        if not abs_path.startswith(base_dir):
            return "Error: Access to files outside the working directory is not allowed"
        
        if not os.path.exists(abs_path):
            return f"Error: File '{file_path}' not found"
        
        with open(abs_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success message or error message
    """
    try:
        # Security check - prevent directory traversal
        abs_path = os.path.abspath(file_path)
        base_dir = os.path.abspath(os.getcwd())
        
        if not abs_path.startswith(base_dir):
            return "Error: Access to files outside the working directory is not allowed"
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        with open(abs_path, 'w') as file:
            file.write(content)
            
        return f"Successfully wrote to file: {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"