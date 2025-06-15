from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from openai import OpenAI

openai_client = OpenAI(api_key="xxx")

 # Replace this with your actual key

# FastAPI app instance
app = FastAPI()

# CORS settings for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB (local instance)
client = MongoClient("mongodb://localhost:27017")
db = client["campus_bot"]
report_collection = db["reports"]

# Pydantic models for request bodies
class ChatRequest(BaseModel):
    message: str

class ReportRequest(BaseModel):
    description: str
    department: str
    contact: str = ""  # Optional

# Endpoint: POST /chat
@app.post("/chat")
def chat(req: ChatRequest):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a supportive and helpful chatbot giving emotional and legal support to students facing bullying on campus."},
            {"role": "user", "content": req.message}
        ]
    )
    return {"reply": response.choices[0].message.content}



# Endpoint: POST /report
@app.post("/report")
def report(req: ReportRequest):
    report_collection.insert_one(req.dict())
    return {"status": "Report submitted anonymously"}
