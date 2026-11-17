"""Basic arithmetic calculator operations."""


def calculator(operation: str, num1: float, num2: float) -> float:
    """Apply an arithmetic operation to two numbers."""
    if operation == "add":
        return num1 + num2
    if operation == "subtract":
        return num1 - num2
    if operation == "multiply":
        return num1 * num2
    if operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    raise ValueError(f"Unsupported operation: {operation}")