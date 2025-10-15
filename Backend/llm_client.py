import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.preferred_models = [m.strip() for m in os.getenv("PREFERRED_MODELS", "").split(",") if m.strip()]
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set in environment")

    async def get_current_model(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(GROQ_MODELS_URL, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"Model list fetch failed: {resp.text}")
            data = resp.json()
            available = [m["id"] for m in data.get("data", [])]
            for pref in self.preferred_models:
                for model_id in available:
                    if pref in model_id:
                        return model_id
            if available:
                return available[0]
            raise RuntimeError("No models available from Groq API")

    async def generate(self, prompt):
        model_name = await self.get_current_model()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(GROQ_API_URL, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Groq API error: {resp.text}")
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
