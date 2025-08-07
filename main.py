from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Load Qwen2 model
model_name = "Qwen/Qwen2-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.2
    max_tokens: int = 150

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Qwen2 API Server", "status": "running"}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    # Format messages for Qwen2
    conversation = ""
    for message in request.messages:
        if message.role == "system":
            conversation += f"System: {message.content}\n"
        elif message.role == "user":
            conversation += f"User: {message.content}\n"
    
    conversation += "Assistant:"
    
    # Tokenize and generate
    inputs = tokenizer(conversation, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response.strip()
                }
            }
        ]
    }
