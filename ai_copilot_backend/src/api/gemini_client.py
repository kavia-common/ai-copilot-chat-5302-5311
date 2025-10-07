import os
from typing import List, Tuple, Dict, Any
import httpx
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str
    id: str = None


class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    
    This client handles communication with the Gemini Generative Language API,
    including request formatting, error handling, and response parsing.
    """
    
    def __init__(self):
        """
        Initialize the Gemini client.
        
        Reads configuration from environment variables:
        - GOOGLE_GEMINI_API_KEY: API key for authentication
        - GEMINI_MODEL: Model to use (default: gemini-1.5-flash)
        """
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        if not self.api_key:
            print("WARNING: GOOGLE_GEMINI_API_KEY not set. API calls will fail.")
            print("Please set GOOGLE_GEMINI_API_KEY in your .env file.")
    
    def _format_messages_for_gemini(self, messages: List[ChatMessage]) -> List[Dict[str, Any]]:
        """
        Format messages for Gemini API format.
        
        Args:
            messages: List of ChatMessage objects
            
        Returns:
            List of formatted message dictionaries
        """
        formatted = []
        for msg in messages:
            # Map roles: user -> user, assistant -> model
            role = "model" if msg.role == "assistant" else "user"
            # Skip system messages for now (can be prepended as context if needed)
            if msg.role != "system":
                formatted.append({
                    "role": role,
                    "parts": [{"text": msg.content}]
                })
        return formatted
    
    async def generate(self, messages: List[ChatMessage]) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a response using the Gemini API.
        
        Args:
            messages: List of ChatMessage objects representing the conversation
            
        Returns:
            Tuple of (response_text, model_info) where model_info contains
            model name and usage statistics
            
        Raises:
            Exception: If API key is not configured or API call fails
        """
        # Check for API key
        if not self.api_key:
            raise Exception(
                "Gemini API key not configured. "
                "Please set GOOGLE_GEMINI_API_KEY environment variable. "
                "You can obtain an API key from https://makersuite.google.com/app/apikey"
            )
        
        try:
            # Format messages for Gemini
            formatted_messages = self._format_messages_for_gemini(messages)
            
            # Prepare request
            url = f"{self.base_url}/models/{self.model}:generateContent"
            params = {"key": self.api_key}
            
            payload = {
                "contents": formatted_messages,
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            # Make API call
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    params=params,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                # Check for errors
                if response.status_code != 200:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("error", {}).get("message", error_detail)
                    except:
                        pass
                    raise Exception(f"Gemini API error ({response.status_code}): {error_detail}")
                
                # Parse response
                result = response.json()
                
                # Extract text from response
                candidates = result.get("candidates", [])
                if not candidates:
                    raise Exception("No response generated from Gemini API")
                
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if not parts:
                    raise Exception("Empty response from Gemini API")
                
                response_text = parts[0].get("text", "")
                
                # Extract usage metadata
                usage_metadata = result.get("usageMetadata", {})
                model_info = {
                    "model": self.model,
                    "usage": {
                        "promptTokens": usage_metadata.get("promptTokenCount", 0),
                        "completionTokens": usage_metadata.get("candidatesTokenCount", 0),
                        "totalTokens": usage_metadata.get("totalTokenCount", 0)
                    }
                }
                
                return response_text, model_info
                
        except httpx.TimeoutException:
            raise Exception("Request to Gemini API timed out. Please try again.")
        except httpx.RequestError as e:
            raise Exception(f"Network error calling Gemini API: {str(e)}")
        except Exception as e:
            # Re-raise with context
            raise Exception(f"Error generating response: {str(e)}")
