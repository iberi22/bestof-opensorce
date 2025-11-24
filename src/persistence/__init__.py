"""
Persistence module for storing processed repositories and video metadata.
"""

from .firebase_store import FirebaseStore

__all__ = ['FirebaseStore']
