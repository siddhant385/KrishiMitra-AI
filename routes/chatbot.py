#route/chatbot.py
# routes/simple_routes.py
from typing import List, Optional
from fastapi import APIRouter,Depends
from dependencies.auth import authenticate_and_get_user_details
from pydantic import BaseModel
from groq import Groq
from constants import GROQ_API_KEY

# from ai.general_chat_agent import simple_agent_run

class Message(BaseModel):
    text: str



# class ChatRequest(BaseModel):
#     message: str
#     context: dict = None  # optional

# # Response model
# class ChatResponse(BaseModel):
#     reply: str


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# user=Depends(authenticate_and_get_user_details)

client = Groq(api_key=GROQ_API_KEY)





@router.post("/chat")
async def chat(message: Message,user=Depends(authenticate_and_get_user_details)):
    try:
        user_input = message.text


        # Simple call without streaming
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "Hello! 👋 How can I help you today?"},
                {"role": "user", "content": user_input}
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False  # streaming off
        )

        # Get the final reply
        bot_reply = completion.choices[0].message.content
        return {"reply": bot_reply}
    except Exception as e:
        print(e)



