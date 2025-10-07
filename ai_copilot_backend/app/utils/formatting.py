"""
Formatting Utilities

Helper functions for formatting text, markdown, and response data.
"""

import re
from typing import Any


# PUBLIC_INTERFACE
def format_markdown_response(text: str) -> str:
    """
    Format and clean markdown text for consistent rendering.
    
    Ensures proper spacing around code blocks, headers, and lists
    for optimal display in markdown renderers.
    
    Args:
        text: Raw text response (may contain markdown)
    
    Returns:
        str: Cleaned and formatted markdown text
    """
    if not text:
        return ""
    
    # Ensure code blocks have proper spacing
    text = re.sub(r'```(\w+)?\n', r'\n```\1\n', text)
    text = re.sub(r'\n```\n', r'\n```\n\n', text)
    
    # Ensure headers have proper spacing
    text = re.sub(r'(^|\n)(#{1,6})\s*([^\n]+)', r'\1\n\2 \3\n', text)
    
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', r'\n\n', text)
    
    # Trim leading/trailing whitespace
    text = text.strip()
    
    return text


# PUBLIC_INTERFACE
def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with an optional suffix.
    
    Args:
        text: The text to truncate
        max_length: Maximum length before truncation
        suffix: String to append if truncated
    
    Returns:
        str: Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


# PUBLIC_INTERFACE
def sanitize_session_id(session_id: str) -> str:
    """
    Sanitize a session ID to prevent injection attacks.
    
    Removes any non-alphanumeric characters except hyphens.
    
    Args:
        session_id: The session ID to sanitize
    
    Returns:
        str: Sanitized session ID
    """
    return re.sub(r'[^a-zA-Z0-9\-]', '', session_id)
