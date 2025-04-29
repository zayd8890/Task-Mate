# tests/test_visualization.py
import pytest
from ai_ml_logic.visualization import visualize_dependencies

def test_visualize_dependencies():
    tasks = [
        {"id": 1, "description": "Task 1", "dependencies": []},
        {"id": 2, "description": "Task 2", "dependencies": [1]},
    ]
    
    # Ensure the function runs without errors
    try:
        visualize_dependencies(tasks)
    except Exception as e:
        pytest.fail(f"Visualization failed with error: {e}")