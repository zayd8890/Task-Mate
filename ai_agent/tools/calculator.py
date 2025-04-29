# tools/calculator.py - Mathematical calculations
import math
import re

def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression as a string
        
    Returns:
        The result of the calculation
    """
    # Sanitize input to prevent code injection
    if not re.match(r'^[\d\+\-\*\/\(\)\.\s]*$', expression):
        return "Error: Invalid characters in expression"
    
    try:
        # Use a safer eval with limited scope
        allowed_names = {
            "abs": abs,
            "float": float,
            "int": int,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "sum": sum
        }
        
        # Add common math functions
        for name in dir(math):
            if not name.startswith('_'):
                allowed_names[name] = getattr(math, name)
        
        # Calculate result
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error calculating result: {str(e)}"