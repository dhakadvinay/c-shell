# Project Handover Documentation
## Legacy Knowledge AI Agent (Project Handover)

**Date**: June 2026
**Role**: Chief Company Historian / Institutional Memory Agent

---

## 1. Executive Summary
This project implements "Project Handover", a Legacy Knowledge AI Agent designed to retrieve undocumented decisions, past incident reports, and historical context. It is built using FastAPI for the backend, WebSockets for real-time streaming, and the `google-antigravity` SDK for AI interactions. 

The primary directive of this system is to act as **LegacyMind AI**, eliminating corporate knowledge loss by seamlessly querying the internal Hindsight Memory Database.

---

## 2. System Architecture

*   **Backend Framework:** Python 3.10+ with FastAPI.
*   **Data Validation:** Pydantic V2 enforcing strict type checking.
*   **Agent Framework:** `google-antigravity` SDK using `LocalAgentConfig`.
*   **Real-time Protocol:** WebSockets (`ws://`) for low-latency streaming of AI thoughts and tool execution statuses.
*   **Authentication:** OAuth2 with JSON Web Tokens (JWT).

---

## 3. The "LegacyMind AI" Intelligence

The agent is driven by a strict system prompt and toolset:

**Core Rules:**
1. **The Hindsight Rule**: Must use the `search_hindsight` tool before answering architectural or historical queries.
2. **The Honesty Rule**: Must state "No relevant internal memory found." if no data exists.
3. **The Expertise Rule**: Always credit the original engineer/PM.

**Tool Integration:**
A tool named `search_hindsight` is registered with the agent, which mocks fetching historical reports (e.g., incident #4092 regarding MongoDB sharding by Sarah Jenkins).

---

## 4. Setup & Deployment Instructions

1. **Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate
```

2. **Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Variables:**
Create a `.env` file based on `.env.example`:
```ini
HINDSIGHT_API_KEY=your_key
ANTIGRAVITY_API_KEY=your_key
JWT_SECRET_KEY=super_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Running the Server:**
```bash
uvicorn main:app --reload
```

5. **Testing:**
```bash
pytest test_main.py -v
```

---

## 5. Source Code

### `requirements.txt`
```text
fastapi
uvicorn[standard]
pydantic>=2.0.0
pydantic-settings
google-antigravity
PyJWT
passlib[bcrypt]
python-dotenv
pytest
httpx
pytest-asyncio
```

### `schemas.py`
```python
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str = Field(..., pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str

class AgentQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    
class AgentResponse(BaseModel):
    message: str
```

### `security.py`
```python
import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_fallback_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise HTTPException(status_code=401)
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401)
```

### `agent.py`
```python
import os
import asyncio
from google_antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

load_dotenv()

async def search_hindsight(query: str) -> str:
    await asyncio.sleep(0.5)
    if "incident" in query.lower() or "architecture" in query.lower():
        return """
        Date: October 2023
        Owner: Sarah Jenkins (Lead DevOps)
        Memory: We migrated from a monolithic PostgreSQL database to a sharded MongoDB cluster to handle the sudden 10x surge in telemetry data. The legacy SQL DB was causing severe connection pooling issues (incident #4092).
        """
    return "No relevant internal memory found."

def get_agent() -> Agent:
    api_key = os.getenv("ANTIGRAVITY_API_KEY", "dummy_key")
    config = LocalAgentConfig(model="gemini-3.1-pro", api_key=api_key)
    
    system_prompt = \"\"\"You are LegacyMind AI, the Chief Company Historian...
[Refer to the actual source file for full prompt rules and The "Wow" Protocol]\"\"\"

    return Agent(config=config, tools=[search_hindsight], system_prompt=system_prompt)
```

### `main.py`
```python
import asyncio
import json
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from schemas import Token, AgentQuery
from security import verify_password, create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from agent import get_agent

app = FastAPI(title="Project Handover API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

fake_users_db = {"admin": {"username": "admin", "hashed_password": get_password_hash("secret")}}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=401)
    access_token = create_access_token(data={"sub": user_dict["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        username = verify_token(token)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
        
    await websocket.accept()
    agent = get_agent()
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                query_data = AgentQuery(**json.loads(data))
            except Exception:
                await websocket.send_json({"type": "error", "content": "Invalid input"})
                continue
                
            try:
                response = await agent.generate(query_data.query)
                async for thought in response.thoughts: await websocket.send_json({"type": "thought", "content": thought})
                async for tool_call in response.tool_calls: await websocket.send_json({"type": "tool_call", "content": f"Tool: {tool_call.name}"})
                await websocket.send_json({"type": "message", "content": response.content})
            except Exception as e:
                 await websocket.send_json({"type": "error", "content": str(e)})
    except WebSocketDisconnect:
        pass
```
