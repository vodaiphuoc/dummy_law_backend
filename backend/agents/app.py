import pathlib
from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
import fastapi.exceptions
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import os
from pydantic import BaseModel
from datetime import datetime
import uuid
from collections import deque

from agents.search_agent import SearchAgent
from agents.reasoning_agent import FinalAnswerAgent
from agents.intent_agent import IntentAgent
from agents.configs import Configuration
import asyncio
import json
from contextlib import asynccontextmanager
import dataclasses

@dataclasses.dataclass
class AgentHolder:
    intent_clf_agent: IntentAgent
    search_agent: SearchAgent
    final_agent: FinalAnswerAgent

@asynccontextmanager
async def lifespan(app: FastAPI):
    main_config = Configuration()
    agent_holder: AgentHolder = AgentHolder(
        intent_clf_agent = IntentAgent(config = main_config),
        search_agent = SearchAgent(config = main_config),
        final_agent = FinalAnswerAgent(config = main_config),
    )
    app.state.agent_holder = agent_holder

    yield
    app.state = None
    

# Define the FastAPI app
app = FastAPI(
    title="Chatbot API",
    description="API for Chatbot with document processing and chat capabilities",
    version="1.0.0",
    lifespan= lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat sessions
class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.chain = None
        self.memory = None
        self.history = []
        self.message_history = deque(maxlen=10)  # For LLM context
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    def add_to_history(self, role: str, content: str):
        """Add a message to history and maintain size limit"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        })
        
        # Keep only the last MAX_HISTORY_MESSAGES messages
        if len(self.history) > MAX_HISTORY_MESSAGES:
            self.history = self.history[-MAX_HISTORY_MESSAGES:]

# Store all active sessions
active_sessions: Dict[str, ChatSession] = {}
MAX_SESSIONS = 100  # Maximum number of active sessions
SESSION_TIMEOUT = 3600  # Session timeout in seconds (1 hour)

# Constants for chat configuration
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_P = 0.95
DEFAULT_LANGUAGE = "vietnamese"
MAX_HISTORY_MESSAGES = 100  # Maximum number of messages to keep in history per session

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: str = None  # Optional session_id

class ChatResponse(BaseModel):
    answer: str
    session_id: str

class ChatHistoryResponse(BaseModel):
    messages: List[Dict]
    session_id: str

# Helper functions
def create_new_session() -> str:
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = ChatSession(session_id)
    return session_id

def get_session(session_id: str) -> ChatSession:
    """Get an existing session or create a new one"""
    if session_id not in active_sessions:
        if len(active_sessions) >= MAX_SESSIONS:
            # Remove oldest inactive session
            oldest_session = min(
                active_sessions.values(),
                key=lambda s: s.last_activity
            )
            del active_sessions[oldest_session.session_id]
        session_id = create_new_session()
    return active_sessions[session_id]

def cleanup_inactive_sessions():
    """Remove sessions that have been inactive for too long and their chat history"""
    current_time = datetime.now()
    inactive_sessions = [
        session_id for session_id, session in active_sessions.items()
        if (current_time - session.last_activity).total_seconds() > SESSION_TIMEOUT
    ]
    
    for session_id in inactive_sessions:
        try:
            # Clear chat history for the session
            session = active_sessions[session_id]
            session.history = []
            session.message_history.clear()
            
            # Remove the session
            del active_sessions[session_id]
            print(f"Cleaned up inactive session {session_id} and its chat history")
        except Exception as e:
            print(f"Error cleaning up session {session_id}: {str(e)}")
            continue

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, api_request: Request):
    """
    Chat with the bot
    
    - **message**: The message to send to the bot
    - **session_id**: Session ID to continue conversation (optional)
    """

    try:
        # Get or create session
        session = get_session(chat_request.session_id)
        session.last_activity = datetime.now()

        query = chat_request.message
        try:
            agent_holder: AgentHolder = api_request.app.state.agent_holder
            intent, msg = await agent_holder.intent_clf_agent.run(query = query)
            if intent:
                search_result = await agent_holder.search_agent.run(query = query)
                answer = await agent_holder.final_agent.run(
                    query = query,
                    search_agent_outputs=search_result
                )
            else:
                answer = msg

        except Exception as e:
            print(f"Error in graph processing: {str(e)}")
            answer = f"I apologize, but I encountered an error: {str(e)}"

        # Add messages to history
        session.add_to_history("user", chat_request.message)
        session.add_to_history("assistant", answer)

        # Add to message history queue for LLM context
        session.message_history.append({
            "input": chat_request.message,
            "output": answer
        })

        # Cleanup inactive sessions
        cleanup_inactive_sessions()

        return ChatResponse(
            answer=answer,
            session_id=session.session_id
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get chat history endpoint
@app.get("/chat/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    """
    Get chat history for a specific session
    
    - **session_id**: Session ID to get history for
    """
    try:
        if session_id not in active_sessions:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
            
        session = active_sessions[session_id]
        session.last_activity = datetime.now()
        
        return ChatHistoryResponse(
            messages=session.history,
            session_id=session_id
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

