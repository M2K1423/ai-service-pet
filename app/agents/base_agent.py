"""Base agent class"""


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    def process(self, input_data):
        """Process input data"""
        raise NotImplementedError("Subclasses must implement process method")
