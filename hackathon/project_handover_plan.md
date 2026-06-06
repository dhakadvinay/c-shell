# Project Handover: Legacy Knowledge AI Agent - Implementation Plan

## 1. Architecture Overview

### Backend Framework
*   **Language & Web Server:** Python 3.10+ with FastAPI. Selected for its non-blocking asynchronous event loop, excellent performance, and native support for WebSockets and Pydantic.
*   **Data Validation:** Pydantic V2 will enforce strict request and response schemas, ensuring all input and output data conforms to expected types.

### Agent Framework
*   **SDK:** `google-antigravity` SDK.
*   **Initialization:** The agent will be initialized using `LocalAgentConfig`.
*   **Memory Integration (Tool):** A custom Python asynchronous function, `query_hindsight_api`, will be implemented to fetch historical employee incident reports. This function will be registered as a Tool within the Antigravity SDK, allowing autonomous data retrieval.

### Frontend Integration (Real-Time)
*   **Protocol:** WebSockets for bidirectional, low-latency communication.
*   **Streaming Features:**
    *   **Reasoning Stream:** The frontend will receive and display the agent's internal reasoning process by iterating over `response.thoughts`.
    *   **Tool Execution Status:** Background tool usage will be streamed to the UI by listening to `response.tool_calls`, providing transparency into the agent's actions.

## 2. Enterprise Cybersecurity Posture

*   **Authentication & Authorization:** 
    *   OAuth2 with JSON Web Tokens (JWT).
    *   All protected endpoints (including WebSocket handshake) will require a valid Bearer token.
    *   Dependencies: `PyJWT`, `passlib`.
*   **Input Sanitization & Threat Prevention:**
    *   System prompts will be designed to mitigate prompt injection.
    *   Pydantic validators will strictly sanitize all incoming string inputs to prevent XSS and SQL/NoSQL injection variants before they reach the agent or database.
*   **Secrets Management:**
    *   Environment variables will be managed via `.env` and loaded using `python-dotenv`.
    *   API keys, JWT secrets, and database URIs will *never* be hardcoded in the repository. An `.env.example` will be provided for secure onboarding.

## 3. Execution Plan (Task List)

### Phase 1: Planning (Current)
- [x] Draft and finalize the Implementation Plan.
- [ ] Receive formal approval from stakeholders (USER).

### Phase 2: Scaffolding and Security Foundation
- [ ] Initialize project directory (`/home/vinaydhakad/Desktop/hackathon/project_handover`).
- [ ] Set up virtual environment and install dependencies (`requirements.txt`).
- [ ] Create `.env.example` and standard `.gitignore`.
- [ ] Implement core security utilities: JWT generation/validation and Pydantic base models with sanitization.

### Phase 3: Core Application Logic
- [ ] Implement the `query_hindsight_api` function mock/stub.
- [ ] Initialize the Antigravity Agent with `LocalAgentConfig` and register the Tool.
- [ ] Develop the FastAPI application and REST endpoints (e.g., login/token generation).
- [ ] Implement the WebSocket endpoint for real-time agent interaction (streaming `thoughts` and `tool_calls`).

### Phase 4: Quality Assurance & Testing
- [ ] Write `pytest` unit tests for JWT authentication.
- [ ] Write unit tests for Pydantic input sanitization.
- [ ] Write unit tests for the Antigravity SDK tool-calling logic and mocked Hindsight API responses.

### Phase 5: Documentation
- [ ] Draft a comprehensive `README.md` covering system requirements, setup instructions, security guidelines, and local execution steps.
