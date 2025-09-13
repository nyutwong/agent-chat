from abc import ABC, abstractmethod

class BaseAgentChat(ABC):
    def __init__(self, model):
        """
        Base Agent class that defines common functionality for all agents
        
        Args:
            model (str): Model to use
        """
        self.model = model
        self.conversation_history = []
    
    @abstractmethod
    def chat(self, message, system_prompt):
        """
        Send message to the model and get response
        
        Args:
            message (str): Message to send
            system_prompt (str): System prompt
            
        Returns:
            str: Response from the model
        """
        pass
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🗑️ Conversation history cleared")
    
    def get_history(self):
        """Show conversation history"""
        return self.conversation_history
    
    def _add_user_message(self, message):
        """Add user message to conversation history"""
        self.conversation_history.append({"role": "user", "content": message})
    
    def _add_assistant_message(self, message):
        """Add assistant message to conversation history"""
        self.conversation_history.append({"role": "assistant", "content": message})
    
    def _prepare_messages(self, system_prompt):
        """Prepare messages for API call"""
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        # Add conversation history
        messages.extend(self.conversation_history)
        
        return messages
