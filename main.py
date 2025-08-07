from fastapi import FastAPI
import asyncio

app = FastAPI()

# Don't load model at startup
model = None
tokenizer = None

async def load_model():
    global model, tokenizer
    if model is None:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        model_name = "Qwen/Qwen2-1.5B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    await load_model()  # Load model only when needed
    # rest of your existing code
