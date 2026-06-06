from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    # Strict validation: prevent XSS, SQLi by only allowing alphanumeric and some special chars
    username: str = Field(..., pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str

class AgentQuery(BaseModel):
    # Sanitize input: limit length, basic escaping if needed
    query: str = Field(..., min_length=1, max_length=1000)
    
class AgentResponse(BaseModel):
    message: str
