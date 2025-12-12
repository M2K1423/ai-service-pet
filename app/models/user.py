"""User model"""
from dataclasses import dataclass


@dataclass
class User:
    """User model class"""
    
    id: int
    username: str
    email: str
    
    def __str__(self):
        return f"User({self.username}, {self.email})"
