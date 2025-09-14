import os
from dotenv import load_dotenv
from providers.openai import OpenAIAgent
from providers.ollama import OllamaAgent
from providers.langchain import LangchainAgent

load_dotenv()

def main():
    """ฟังก์ชันหลักสำหรับทดสอบ AI Agent"""
    
    print("🤖 Agent Chat")
    print("=" * 50)
    
    # Ask for provider
    print("เลือก AI provider:")
    print("1. Ollama (default)")
    print("2. OpenAI")
    print("3. Langchain")
    provider_choice = input("เลือก (1/2/3) [กด Enter เพื่อใช้ default]: ").strip()
    
    # Set provider based on choice
    if provider_choice == "2":
        provider = "openai"
    elif provider_choice == "3":
        provider = "langchain"
    else:
        provider = "ollama"  # Default or if user pressed Enter or chose 1
    
    # Set default models based on provider
    if provider == "openai":
        default_model = os.getenv("OPENAI_MODEL")
        print(f"\nเลือก OpenAI model (default: {default_model}):")
    
        model_name = input("เลือก model [กด Enter เพื่อใช้ default]: ").strip()
        if model_name =="":
            model_name=default_model
        
        agent = OpenAIAgent(api_key=os.getenv("OPENAI_API_KEY"), model=model_name)
        ai_name = "OpenAI"
    elif provider == "langchain":
        default_provider = os.getenv("LANGCHAIN_PROVIDER", "ollama")
        
        model_provider = input(f"เลือก model provider [ollama/openai] (default: {default_provider}): ").strip()
        if model_provider == "":
            model_provider = default_provider

        default_model = os.getenv("OLLAMA_MODEL", "scb10x/llama3.1-typhoon2-8b-instruct") if model_provider == "ollama" else os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"\nเลือก Langchain model (default: {default_model}):")
        model_name = input("เลือก model [กด Enter เพื่อใช้ default]: ").strip()
        if model_name == "":
            model_name = default_model
            
            
        agent = LangchainAgent(model=model_name, model_provider=model_provider)
        ai_name = "Langchain"
    else:  # ollama
        default_model = os.getenv("OLLAMA_MODEL")
        print(f"\nเลือก Ollama model (default: {default_model}):")

        model_name = input("เลือก model [กด Enter เพื่อใช้ default]: ").strip()
        if model_name =="":
            model_name=default_model
        
        agent = OllamaAgent(host=os.getenv("OLLAMA_HOST"), port=os.getenv("OLLAMA_PORT"), model=model_name)
        ai_name = "Ollama"
    
    if provider == "langchain":
        print(f"\n🤖 AI Agent - Using {provider.upper()} with model: {model_name} (provider: {model_provider})")
    else:
        print(f"\n🤖 AI Agent - Using {provider.upper()} with model: {model_name}")
    print("=" * 50)
    
    # System prompt
    system_prompt = os.getenv("SYSTEM_PROMPT")
    
    print("💬 พิมพ์ 'quit' เพื่อออกจากโปรแกรม")
    print("💬 พิมพ์ 'clear' เพื่อล้าง conversation history")
    print("💬 พิมพ์ 'history' เพื่อดู conversation history")
    print("-" * 50)
    
    while True:
        try:
            # รับ input จากผู้ใช้
            user_input = input("\n🧑‍💻 คุณ: ").strip()
            
            # ตรวจสอบคำสั่งพิเศษ
            if user_input.lower() == 'quit':
                print("👋 ลาก่อน!")
                break
            elif user_input.lower() == 'clear':
                agent.clear_history()
                continue
            elif user_input.lower() == 'history':
                history = agent.get_history()
                print("\n📝 Conversation History:")
                for i, msg in enumerate(history, 1):
                    role = "🧑‍💻" if msg["role"] == "user" else "🤖"
                    print(f"{i}. {role} {msg['role']}: {msg['content'][:100]}...")
                continue
            
            if not user_input:
                continue
                
            print(f"\n🤖 กำลังประมวลผล...")
            
            # ส่งข้อความไปหา AI
            response = agent.chat(user_input, system_prompt)
            
            if response:
                print(f"\n🤖 {ai_name}: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 ลาก่อน!")
            break
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()