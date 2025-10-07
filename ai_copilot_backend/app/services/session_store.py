"""
Session Store

In-memory session management for storing conversation histories.
Note: Sessions are not persisted and will be lost on server restart.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from threading import Lock

logger = logging.getLogger(__name__)


class SessionStore:
    """
    In-memory storage for chat sessions.
    
    This class manages chat sessions, storing conversation history
    for each session. Data is stored in memory only and is not persisted.
    
    Thread-safe operations using locks to prevent race conditions.
    """
    
    def __init__(self):
        """Initialize the session store with an empty dictionary and lock."""
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        logger.info("Session store initialized")
    
    # PUBLIC_INTERFACE
    def create_session(self) -> str:
        """
        Create a new chat session.
        
        Generates a unique session ID and initializes an empty message list.
        
        Returns:
            str: The newly created session ID
        """
        session_id = str(uuid.uuid4())
        
        with self._lock:
            self._sessions[session_id] = {
                "messages": [],
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
        
        logger.info(f"Created session: {session_id}")
        return session_id
    
    # PUBLIC_INTERFACE
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by ID.
        
        Args:
            session_id: The unique session identifier
        
        Returns:
            dict: Session data including messages and metadata, or None if not found
        """
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                # Update last activity timestamp
                session["last_activity"] = datetime.now().isoformat()
            return session
    
    # PUBLIC_INTERFACE
    def append_message(self, session_id: str, message: Dict[str, Any]) -> bool:
        """
        Add a message to a session's conversation history.
        
        Args:
            session_id: The session to append to
            message: Message dictionary with 'role' and 'content' keys
        
        Returns:
            bool: True if message was added, False if session not found
        """
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                logger.warning(f"Attempted to append to non-existent session: {session_id}")
                return False
            
            session["messages"].append(message)
            session["last_activity"] = datetime.now().isoformat()
            
            logger.debug(f"Appended message to session {session_id}. Total messages: {len(session['messages'])}")
            return True
    
    # PUBLIC_INTERFACE
    def reset_session(self, session_id: str) -> bool:
        """
        Clear all messages from a session while keeping it active.
        
        Args:
            session_id: The session to reset
        
        Returns:
            bool: True if session was reset, False if session not found
        """
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                logger.warning(f"Attempted to reset non-existent session: {session_id}")
                return False
            
            session["messages"] = []
            session["last_activity"] = datetime.now().isoformat()
            
            logger.info(f"Reset session: {session_id}")
            return True
    
    # PUBLIC_INTERFACE
    def delete_session(self, session_id: str) -> bool:
        """
        Permanently delete a session.
        
        Args:
            session_id: The session to delete
        
        Returns:
            bool: True if session was deleted, False if not found
        """
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                logger.info(f"Deleted session: {session_id}")
                return True
            
            logger.warning(f"Attempted to delete non-existent session: {session_id}")
            return False
    
    # PUBLIC_INTERFACE
    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all active sessions.
        
        Returns:
            dict: Dictionary of all sessions with their data
        
        Note:
            Use with caution in production as this can return large amounts of data.
        """
        with self._lock:
            return dict(self._sessions)
    
    # PUBLIC_INTERFACE
    def session_count(self) -> int:
        """
        Get the total number of active sessions.
        
        Returns:
            int: Number of active sessions
        """
        with self._lock:
            return len(self._sessions)


# Global singleton instance
session_store = SessionStore()
