"""
Gemini API Client

Handles communication with Google's Gemini API for natural language processing.
Includes fallback mock responses when API key is not configured.
"""

import logging
from typing import List, Dict, Any, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    
    This client wraps the google-generativeai SDK and provides
    a simplified interface for generating chat responses. It includes
    a fallback mechanism for testing without an API key.
    """
    
    def __init__(self):
        """
        Initialize the Gemini client.
        
        Attempts to configure the google-generativeai SDK with the API key
        from settings. If the key is missing or invalid, falls back to
        mock mode for testing.
        """
        self.model = None
        self.mock_mode = False
        
        try:
            import google.generativeai as genai
            
            if settings.GOOGLE_GEMINI_API_KEY and settings.GOOGLE_GEMINI_API_KEY != "your_api_key_here":
                genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
                self.model = genai.GenerativeModel(settings.MODEL_NAME)
                logger.info(f"Gemini client initialized with model: {settings.MODEL_NAME}")
            else:
                logger.warning("GOOGLE_GEMINI_API_KEY not configured. Running in MOCK MODE.")
                self.mock_mode = True
                
        except ImportError:
            logger.error("google-generativeai package not installed. Running in MOCK MODE.")
            self.mock_mode = True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}. Running in MOCK MODE.")
            self.mock_mode = True
    
    # PUBLIC_INTERFACE
    async def generate_response(
        self,
        prompt: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate a response to the user's prompt.
        
        Args:
            prompt: The user's message/question
            history: Optional conversation history for context
        
        Returns:
            str: The AI-generated response in markdown format
        
        Note:
            If running in mock mode (no API key), returns a predefined
            response indicating the service is in test mode.
        """
        if self.mock_mode:
            return self._generate_mock_response(prompt)
        
        try:
            # Start a chat session with history if available
            chat = self.model.start_chat(history=self._format_history_for_gemini(history))
            
            # Generate response
            response = chat.send_message(prompt)
            
            # Extract text from response
            response_text = response.text
            
            logger.debug(f"Generated response length: {len(response_text)} chars")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response from Gemini: {str(e)}", exc_info=True)
            # Fallback to mock response on error
            return self._generate_mock_response(prompt, error=True)
    
    def _format_history_for_gemini(
        self,
        history: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, str]]:
        """
        Format conversation history for Gemini API.
        
        Converts internal message format to Gemini's expected format.
        
        Args:
            history: List of message dictionaries
        
        Returns:
            List of formatted messages for Gemini
        """
        if not history:
            return []
        
        formatted = []
        for msg in history[:-1]:  # Exclude the last message (current prompt)
            role = "user" if msg.get("role") == "user" else "model"
            formatted.append({
                "role": role,
                "parts": [msg.get("content", "")]
            })
        
        return formatted
    
    def _generate_mock_response(self, prompt: str, error: bool = False) -> str:
        """
        Generate a mock response for testing without API key.
        
        Args:
            prompt: The user's prompt (used to customize mock response)
            error: Whether this is an error fallback
        
        Returns:
            str: A mock response in markdown format
        """
        if error:
            return """# ⚠️ Service Error

I apologize, but I encountered an error while processing your request. This could be due to:

- API connectivity issues
- Rate limiting
- Service unavailability

Please try again in a moment. If the issue persists, contact support.

---
*Error fallback mode active*
"""
        
        return f"""# 🤖 Mock Response Mode

**Your message:** {prompt[:100]}...

I'm currently running in **mock mode** because the Gemini API key is not configured.

## To enable full AI functionality:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file:
   ```
   GOOGLE_GEMINI_API_KEY=your_actual_key_here
   ```
3. Restart the server

## Available capabilities when properly configured:

- ✍️ **Writing assistance** - drafting, editing, and proofreading
- 📝 **Summarization** - condensing long texts
- 💡 **Brainstorming** - generating ideas and solutions
- 💻 **Coding help** - writing, debugging, and explaining code
- 📚 **Research** - finding information and explanations

---
*This is a test response. Configure your API key to unlock full AI capabilities.*
"""


# Global singleton instance
gemini_client = GeminiClient()
