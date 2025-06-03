 

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.environ.get("OPENAI_API_KEY", "")

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    try:
        client = openai.OpenAI(api_key=openai.api_key)  # كائن جديد حسب النسخة الجديدة
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        reply = completion.choices[0].message.content
        return MessageResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

