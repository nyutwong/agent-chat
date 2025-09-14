from langchain.chat_models import init_chat_model
from base_agent_chat import BaseAgentChat

class LangchainAgent(BaseAgentChat):
    def __init__(self, model, model_provider):
        """
        Langchain Agent
        
        Args:
            model (str): Model to use
            model_provider (str): Provider for the model (e.g., "ollama")
        """
        super().__init__(model)
        self.model = model
        self.model_provider = model_provider
        self.client = init_chat_model(model, model_provider=model_provider)
        
    def chat(self, message, system_prompt):
        """
        Send message to Langchain and get response
        
        Args:
            message (str): Message to send
            system_prompt (str): System prompt
            
        Returns:
            str: Response from Langchain
        """
        # Add user message to conversation history
        self._add_user_message(message)
        
        # Get messages for API call
        messages = self._prepare_messages(system_prompt)
        
        try:
            # Call Langchain
            response = self.client.invoke(messages)
            
            # Extract response
            assistant_message = str(response.content)
            
            # Add response to conversation history
            self._add_assistant_message(assistant_message)
            
            # แสดง token usage
            usage = response.usage_metadata
            print(f"\n📊 Token Usage:")
            print(f"   Input tokens: {usage['input_tokens']}")
            print(f"   Output tokens: {usage['output_tokens']}")
            print(f"   Total tokens: {usage['total_tokens']}")
            print("-" * 50)

            return assistant_message

            
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None