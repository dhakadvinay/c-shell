import asyncio
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import json

from schemas import Token, AgentQuery
from security import verify_password, create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from agent import get_agent

app = FastAPI(title="Project Handover API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy user db for demonstration
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("secret"), 
    }
}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-data")
async def read_secure_data(username: str = Depends(verify_token)):
    return {"message": f"Hello {username}, you are authenticated."}

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
                payload = json.loads(data)
                query_data = AgentQuery(**payload)
            except Exception as e:
                await websocket.send_json({"type": "error", "content": "Invalid input format. Must be JSON with 'query' field."})
                continue
                
            try:
                # Assuming google-antigravity syntax for generation and streaming
                response = await agent.generate(query_data.query)
                
                # Streaming thoughts
                async for thought in response.thoughts:
                    await websocket.send_json({"type": "thought", "content": thought})
                    
                # Streaming tool execution
                async for tool_call in response.tool_calls:
                    await websocket.send_json({"type": "tool_call", "content": f"Tool invoked: {tool_call.name}"})
                    
                await websocket.send_json({"type": "message", "content": response.content})
                
            except Exception as e:
                 await websocket.send_json({"type": "error", "content": str(e)})
            
    except WebSocketDisconnect:
        print("Client disconnected")
