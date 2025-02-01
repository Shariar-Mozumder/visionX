# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from pydantic import BaseModel
# from typing import List, Dict, Optional
# from phi.agent import Agent
# from langchain_community.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import JSONLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# from phi.knowledge.langchain import LangChainKnowledgeBase
# from phi.model.groq import Groq
# from uuid import uuid4
# from datetime import datetime

# app = FastAPI()
# security = HTTPBasic()

# # Mock user database
# users_db = {
#     "shmozumder2@gmail.com": {
#         "password": "password123",
#         "session_id": None,
#         "chat_history": []
#     }
# }

# # Session management
# sessions = {}

# class ChatMessage(BaseModel):
#     email: str
#     message: str

# class ChatResponse(BaseModel):
#     response: str

# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = users_db.get(credentials.username)
#     if user and user["password"] == credentials.password:
#         return credentials.username
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorrect email or password",
#         headers={"WWW-Authenticate": "Basic"},
#     )

# def get_session(email: str):
#     if email not in users_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not users_db[email]["session_id"]:
#         users_db[email]["session_id"] = str(uuid4())
#     session_id = users_db[email]["session_id"]
#     if session_id not in sessions:
#         sessions[session_id] = {"email": email, "last_activity": datetime.now()}
#     return session_id

# def update_chat_history(email: str, message: str, response: str):
#     if len(users_db[email]["chat_history"]) >= 5:
#         users_db[email]["chat_history"].pop(0)
#     users_db[email]["chat_history"].append((message, response))

# # Load documents
# loader = JSONLoader(file_path="HR_module/FAQs.json", jq_schema=".", text_content=False)
# docs = loader.load()

# # Split text into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# docs = text_splitter.split_documents(docs)

# # Create Chroma vector store
# db = Chroma(embedding_function=HuggingFaceEmbeddings(), persist_directory="./chroma_db")
# db.add_documents(docs)

# # Set up the retriever
# retriever = db.as_retriever()

# # Create a knowledge base
# knowledge_base = LangChainKnowledgeBase(retriever=retriever)
# from rag_db import get_candidate_info
# def query_database(query,email):
#     result=get_candidate_info(email,query)
#     return result
# # Create the Knowledge Base Agent
# knowledge_agent = Agent(
#     name="Company Inquery Agent",
#     role="Answers FAQs from knowledge base, recruitment questions and candidate progress queries from query db tool.",
#     instructions=[
#          "If the question is about company or company policy or any Frequently Asked Questions(FAQs) about the company use the knowledge base to answer the question.",
#          "If the question is about specific individual's data such as interview and requires querying the database, extract the email and question from the input and use the `query_database` tool.",
#          "You will be given the candidate's email, identify the candidate by email and answer the question from his information.",
#          "Do not answer anything without the knowledge base or database query. follow this strictly. If the answer is not available, just say 'Sorry I have no information about this, please contact ESAP for details.'",
#          "Always call the user as 'You' or 2nd person perspective."
#          "Follow the conversation context.",
#      ],
#     model=Groq(id='gemma2-9b-it'),
#     knowledge=knowledge_base,
#     tools=[query_database],  # Add the tool here
#     add_context=True,
#     search_knowledge=True,
#     debug=True,
#     markdown=True,
# )

# @app.post("/chat", response_model=ChatResponse)
# async def chat(chat_message: ChatMessage, email: str = Depends(authenticate_user)):
#     session_id = get_session(email)
#     prompt = f"My email is {email}. Answer my question from the provided knowledge base: {chat_message.message}."
#     result = knowledge_agent.run(prompt)
#     update_chat_history(email, chat_message.message, result)
#     return ChatResponse(response=result.content)

# @app.get("/chat_history", response_model=List[Dict[str, str]])
# async def get_chat_history(email: str = Depends(authenticate_user)):
#     return [{"question": q, "answer": a} for q, a in users_db[email]["chat_history"]]

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Dict, Optional
from phi.agent import Agent
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from phi.knowledge.langchain import LangChainKnowledgeBase
from phi.model.groq import Groq
from uuid import uuid4
from datetime import datetime
import json
import os

app = FastAPI()
security = HTTPBasic()

# Path to the JSON file for user database
USER_DB_FILE = "users_db.json"

# Load user database from JSON file
def load_user_db():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user database to JSON file
def save_user_db(users_db):
    with open(USER_DB_FILE, "w") as file:
        json.dump(users_db, file, indent=4)

# Initialize user database
users_db = load_user_db()

# Session management
sessions = {}

class ChatMessage(BaseModel):
    email: str
    message: str

class ChatResponse(BaseModel):
    response: str

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    # If the user doesn't exist, create a new user
    if credentials.username not in users_db:
        users_db[credentials.username] = {
            "password": credentials.password,  # Save the provided password
            "session_id": None,
            "chat_history": []
        }
        save_user_db(users_db)  # Save updated user database
    user = users_db.get(credentials.username)
    if user and user["password"] == credentials.password:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )

def get_session(email: str):
    if email not in users_db:
        # Add new user to the database
        users_db[email] = {
            "password": "password123",  # Default password, you can customize this
            "session_id": None,
            "chat_history": []
        }
        save_user_db(users_db)  # Save updated user database
    if not users_db[email].get("session_id"):
        users_db[email]["session_id"] = str(uuid4())
        save_user_db(users_db)  # Save updated user database
    session_id = users_db[email]["session_id"]
    if session_id not in sessions:
        sessions[session_id] = {"email": email, "last_activity": datetime.now()}
    return session_id

def update_chat_history(email: str, message: str, response: str):
    if "chat_history" not in users_db[email]:
        users_db[email]["chat_history"] = []
    if len(users_db[email]["chat_history"]) >= 5:
        users_db[email]["chat_history"].pop(0)
    users_db[email]["chat_history"].append((message, response))
    save_user_db(users_db)  # Save updated user database

# Load documents
loader = JSONLoader(file_path="HR_module/FAQs.json", jq_schema=".", text_content=False)
docs = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(docs)

# Create Chroma vector store
db = Chroma(embedding_function=HuggingFaceEmbeddings(), persist_directory="./chroma_db")
db.add_documents(docs)

# Set up the retriever
retriever = db.as_retriever()

# Create a knowledge base
knowledge_base = LangChainKnowledgeBase(retriever=retriever)

# Define a tool for querying the database
from rag_db import get_candidate_info
def query_database(query,email):
    result=get_candidate_info(email,query)
    return result

# Create the Knowledge Base Agent
knowledge_agent = Agent(
    name="Company Inquiry Agent",
    role="Answers FAQs from knowledge base, recruitment questions, and candidate progress queries from query db tool.",
    instructions=[
         "If the question is about the company or company policy or any Frequently Asked Questions (FAQs) about the company, use the knowledge base to answer the question.",
         "If the question is about specific individual's data such as interview status and requires querying the database, extract the email and question from the input and use the `query_database` tool.",
         "You will be given the candidate's email, identify the candidate by email and answer the question from their information.",
         "Do not answer anything without the knowledge base or database query. Follow this strictly. If the answer is not available, just say 'Sorry, I have no information about this. Please contact ESAP for details.'",
         "Always address the user as 'You' or from a 2nd person perspective.",
         "Follow the conversation context and use the chat history to maintain context.",
     ],
    model=Groq(id='gemma2-9b-it'),
    knowledge=knowledge_base,
    tools=[query_database],  # Add the tool here
    add_context=True,
    search_knowledge=True,
    debug=True,
    markdown=True,
)

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage, email: str = Depends(authenticate_user)):
    session_id = get_session(email)
    chat_history = users_db[email].get("chat_history", [])
    
    # Build the prompt with chat history for context
    context = "\n".join([f"Q: {q}\nA: {a}" for q, a in chat_history])
    prompt = (
        f"My email is {email}. Here is our conversation history:\n{context}\n"
        f"Answer my question from the provided knowledge base.: {chat_message.message}."
    )
    
    result = knowledge_agent.run(prompt)
    update_chat_history(email, chat_message.message, result.content)
    return ChatResponse(response=result.content)

@app.get("/chat_history", response_model=List[Dict[str, str]])
async def get_chat_history(email: str = Depends(authenticate_user)):
    return [{"question": q, "answer": a} for q, a in users_db[email].get("chat_history", [])]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)