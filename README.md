# AI Chat Agent

โปรเจกต์นี้เป็น AI Agent ที่สามารถใช้ models ได้ทั้ง OpenAI (ChatGPT) และ Ollama Providers เพื่อใช้ทำความเข้าใจ AI Agent อย่างง่าย ทดสอบ model ต่างๆ และแสดงจำนวน token ที่ใช้

## Features

- 🤖 รองรับทั้ง OpenAI และ Ollama Provider
- 🔄 เลือก model ได้ตามต้องการผ่านเมนูโต้ตอบ
- 💬 Chat interface แบบ interactive
- 📊 แสดง token usage (input/output tokens)
- 📝 เก็บ conversation history
- 🗑️ ล้าง conversation history ได้
- ⚙️ กำหนด system prompt ได้

## การติดตั้ง

1. สร้าง virtual environment และติดตั้ง dependencies:
```bash
# สร้าง virtual environment
uv venv

# เปิดใช้งาน virtual environment
# สำหรับ Windows
venv\Scripts\activate
# สำหรับ macOS/Linux
source venv/bin/activate

# ติดตั้ง dependencies
uv sync
```

2. ตั้งค่า API keys และ configuration ไฟล์ `.env` จาก `.env.example`:
```
# OpenAI Configuration
OPENAI_API_KEY=

# Ollama Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL = scb10x/llama3.1-typhoon2-8b-instruct

#Model configuration
TEMPERATURE=0.7
SYSTEM_PROMPT="""
คุณคือ มีชื่อว่า [ชื่อของagent]

ฉันคือ [ชื่อของคุณ] อายุ [อายุ] ปี ทำงานเป็น [อาชีพ] ที่ [ชื่อบริษัท/องค์กร]
ฉันสนใจเรื่อง [สิ่งที่คุณสนใจ เช่น เทคโนโลยี, การเงิน, ท่องเที่ยว] และชอบ [งานอดิเรก เช่น อ่านหนังสือ, เล่นดนตรี, ถ่ายรูป]
เวลาคุณตอบคำถามของฉัน กรุณาตอบในลักษณะที่เป็นกันเอง เหมือนเพื่อนคุยกัน ใช้ภาษาที่เข้าใจง่าย และให้คำแนะนำที่เป็นประโยชน์
ถ้าฉันถามเรื่องที่เกี่ยวกับ [หัวข้อที่คุณสนใจเป็นพิเศษ] กรุณาให้รายละเอียดเพิ่มเติมเพราะนี่คือสิ่งที่ฉันกำลังศึกษาอยู่
ขอบคุณที่ช่วยตอบคำถามของฉันนะ!"""
```

3. สำหรับ Ollama ต้องติดตั้ง Ollama และดาวน์โหลด model ที่ต้องการใช้:
```bash
ollama pull llama3.1-8b-instruct
```

## การใช้งาน

รันโปรแกรม:
```bash
uv run python main.py
```

เมื่อรันโปรแกรม คุณจะได้รับการถามเพื่อเลือก:
1. AI provider (Ollama หรือ OpenAI)
2. Model ที่ต้องการใช้

คุณสามารถกด Enter เพื่อใช้ค่า default ในแต่ละขั้นตอน

### คำสั่งพิเศษ

- `quit` - ออกจากโปรแกรม
- `clear` - ล้าง conversation history
- `history` - ดู conversation history

## ตัวอย่างการใช้งานใน Code

### OpenAI
```python
from models.openai import ChatGPTAgent

# สร้าง agent
agent = ChatGPTAgent(api_key="your_api_key", model="gpt-4o-mini")

# ส่งข้อความ
response = agent.chat("สวัสดี")
print(response)
```

### Ollama
```python
from models.ollama import OllamaAgent

# สร้าง agent
agent = OllamaAgent(model="llama3.1-8b-instruct")

# ส่งข้อความพร้อม system prompt
response = agent.chat(
    "อธิบายเรื่อง AI", 
    system_prompt="คุณเป็นผู้เชี่ยวชาญด้าน AI"
)
print(response)
```

## Token Usage

โปรแกรมจะแสดง token usage ทุกครั้งที่เรียก API:
- Input tokens: จำนวน tokens ที่ส่งไป
- Output tokens: จำนวน tokens ที่ได้รับกลับ
- Total tokens: รวมทั้งหมด