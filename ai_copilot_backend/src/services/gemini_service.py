import os
from typing import Optional
import google.generativeai as genai
from src.models.schemas import Message


class GeminiService:
    """
    Service class for interacting with Google's Gemini API.
    
    Handles initialization, configuration, and communication with the Gemini
    generative AI model for chat-based interactions.
    """
    
    def __init__(self):
        """
        Initialize the Gemini service with API key from environment.
        
        Raises:
            ValueError: If GEMINI_API_KEY environment variable is not set
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please configure your API key in the .env file."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        # Using gemini-pro for text generation
        self.model = genai.GenerativeModel('gemini-pro')
    
    # PUBLIC_INTERFACE
    def generate_reply(
        self, 
        prompt: str, 
        history: Optional[list[Message]] = None
    ) -> str:
        """
        Generate a reply from the Gemini API based on the prompt and conversation history.
        
        Args:
            prompt: The user's message/prompt to send to the AI
            history: Optional list of previous messages for conversation context
            
        Returns:
            The AI-generated response as a string
            
        Raises:
            Exception: If there's an error communicating with the Gemini API
        """
        try:
            # Build conversation context if history is provided
            if history:
                # Format history for the model
                conversation_parts = []
                for msg in history:
                    role_prefix = "User" if msg.role == "user" else "Assistant"
                    conversation_parts.append(f"{role_prefix}: {msg.content}")
                
                # Combine history with current prompt
                full_prompt = "\n".join(conversation_parts) + f"\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt
            
            # Generate content using the model
            response = self.model.generate_content(full_prompt)
            
            # Extract and return the text response
            if response and response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            # Log the error (in production, use proper logging)
            error_message = str(e)
            print(f"Error generating reply from Gemini API: {error_message}")
            
            # Return a user-friendly error message
            if "API key" in error_message:
                raise Exception(
                    "Invalid or missing API key. Please check your GEMINI_API_KEY configuration."
                )
            else:
                raise Exception(
                    f"Error communicating with Gemini API: {error_message}"
                )
