# Project Handover

Legacy Knowledge AI Agent built with FastAPI and Antigravity SDK.

## Features
- Real-time WebSocket connection for Agent streaming
- Live streaming of Agent `thoughts` and `tool_calls`
- Robust OAuth2 Authentication using JWT
- Strict Pydantic V2 Input validation and sanitization

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment variables:
Copy the `.env.example` to `.env` and provide your specific keys.
```bash
cp .env.example .env
```

4. Run the server locally:
```bash
uvicorn main:app --reload
```
The server will start on `http://127.0.0.1:8000`.

## Testing

You can run the full suite of unit tests with `pytest`:
```bash
pytest test_main.py -v
```
