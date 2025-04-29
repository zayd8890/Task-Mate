# tests/conftest.py
import pytest
import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup any global fixtures here
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables and configurations"""
    # Set environment variables for testing
    os.environ["OPENAI_API_KEY"] = "test_api_key"
    os.environ["SEARCH_API_KEY"] = "test_search_api_key"
    
    # Create any necessary test directories
    os.makedirs("test_output", exist_ok=True)
    
    yield
    
    # Cleanup after tests
    if os.path.exists("test_output"):
        import shutil
        shutil.rmtree("test_output")