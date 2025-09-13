import openai
import os
from providers.base import BaseAgent

class OpenAIAgent(BaseAgent):
    def __init__(self, api_key, model):
        """
        ChatGPT Agent
        
        Args:
            api_key (str): OpenAI API key
            model (str): โมเดลที่จะใช้
        """
        super().__init__(model)
        self.client = openai.OpenAI(
            api_key=api_key
        )
        
    def chat(self, message, system_prompt):
        """
        ส่งข้อความไปหา ChatGPT และได้รับการตอบกลับ
        
        Args:
            message (str): ข้อความที่ต้องการส่ง
            system_prompt (str): system prompt
            
        Returns:
            str: การตอบกลับจาก ChatGPT
        """
        # เพิ่มข้อความของผู้ใช้ลงใน conversation history
        self._add_user_message(message)
        
        # สร้าง messages สำหรับ API call
        messages = self._prepare_messages(system_prompt)
        
        try:
            # เรียก OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=float(os.getenv("TEMPERATURE", 0.7))
            )
            
            # ดึงการตอบกลับ
            assistant_message = response.choices[0].message.content
            
            # แสดง token usage
            usage = response.usage
            print(f"\n📊 Token Usage:")
            print(f"   Input tokens: {usage.prompt_tokens}")
            print(f"   Output tokens: {usage.completion_tokens}")
            print(f"   Total tokens: {usage.total_tokens}")
            print("-" * 50)
            
            # เพิ่มการตอบกลับลงใน conversation history
            self._add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return None