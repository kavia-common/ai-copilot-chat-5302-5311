import os
from typing import List, Dict
import google.generativeai as genai


class GeminiClient:
    """
    PUBLIC_INTERFACE
    Service class for interacting with Google's Gemini AI API.
    Handles chat message processing and response generation.
    """
    
    def __init__(self):
        """Initialize the Gemini client with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    # PUBLIC_INTERFACE
    def respond(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response from Gemini based on conversation history.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
                     Roles can be 'user', 'assistant', or 'system'.
        
        Returns:
            str: The generated response from Gemini.
        
        Raises:
            Exception: If the API call fails or returns an error.
        """
        try:
            # Convert message history to Gemini format
            # Gemini uses 'user' and 'model' roles
            conversation_parts = []
            
            # Add system prompt if present
            system_prompt = None
            for msg in messages:
                if msg.get("role") == "system":
                    system_prompt = msg.get("content", "")
                elif msg.get("role") == "user":
                    conversation_parts.append({
                        "role": "user",
                        "parts": [msg.get("content", "")]
                    })
                elif msg.get("role") == "assistant":
                    conversation_parts.append({
                        "role": "model",
                        "parts": [msg.get("content", "")]
                    })
            
            # Build the prompt
            if system_prompt:
                # Prepend system prompt to first user message if exists
                if conversation_parts and conversation_parts[0]["role"] == "user":
                    conversation_parts[0]["parts"][0] = f"{system_prompt}\n\n{conversation_parts[0]['parts'][0]}"
                else:
                    conversation_parts.insert(0, {
                        "role": "user",
                        "parts": [system_prompt]
                    })
            
            # Start chat with history
            chat = self.model.start_chat(history=conversation_parts[:-1] if len(conversation_parts) > 1 else [])
            
            # Send the last message
            last_message = conversation_parts[-1]["parts"][0] if conversation_parts else "Hello"
            response = chat.send_message(last_message)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
