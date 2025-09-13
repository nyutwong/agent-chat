import requests
import os
from providers.base import BaseAgent

class OllamaAgent(BaseAgent):
    def __init__(self, model, host, port):
        """
        Ollama Agent
        
        Args:
            model (str): Model to use
            host (str): Ollama host address
            port (int): Ollama port number
        """
        super().__init__(model)
        self.api_url = f"http://{host}:{port}/api/chat"
        
    def chat(self, message, system_prompt):
        """
        Send message to Ollama and get response
        
        Args:
            message (str): Message to send
            system_prompt (str): System prompt
            
        Returns:
            str: Response from Ollama
        """
        # Add user message to conversation history
        self._add_user_message(message)
        
        # Get messages for API call
        messages = self._prepare_messages(system_prompt)
        
        try:
            # Call Ollama API
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": float(os.getenv("TEMPERATURE", 0.7))
                    }
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response
            assistant_message = result["message"]["content"]
            
            # Show token usage if available
            if "prompt_eval_count" in result and "eval_count" in result:
                print(f"\n📊 Token Usage:")
                print(f"   Input tokens: {result.get('prompt_eval_count', 'N/A')}")
                print(f"   Output tokens: {result.get('eval_count', 'N/A')}")
                print(f"   Total tokens: {result.get('prompt_eval_count', 0) + result.get('eval_count', 0)}")
                print("-" * 50)
            
            # Add response to conversation history
            self._add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None