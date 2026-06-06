import os
import asyncio
from google_antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

load_dotenv()

async def search_hindsight(query: str) -> str:
    """
    Search the Hindsight Memory Database for internal architecture, past incidents, infrastructure, or company decisions.
    
    Args:
        query: The search query to find relevant legacy knowledge.
    """
    # Simulated API call to Hindsight Cloud API
    await asyncio.sleep(0.5)
    
    # Mock data return for demonstration
    if "incident" in query.lower() or "architecture" in query.lower():
        return """
        Date: October 2023
        Owner: Sarah Jenkins (Lead DevOps)
        Memory: We migrated from a monolithic PostgreSQL database to a sharded MongoDB cluster to handle the sudden 10x surge in telemetry data. The legacy SQL DB was causing severe connection pooling issues (incident #4092).
        """
    return "No relevant internal memory found."

def get_agent() -> Agent:
    api_key = os.getenv("ANTIGRAVITY_API_KEY", "dummy_key")
    
    config = LocalAgentConfig(
        model="gemini-3.1-pro",
        api_key=api_key,
    )
    
    system_prompt = """You are LegacyMind AI, the Chief Company Historian and Institutional Memory Agent. Your primary directive is to eliminate corporate knowledge loss by retrieving undocumented decisions, past incident reports, and historical context from the Hindsight Memory Database.

CRITICAL RULES:
1. THE HINDSIGHT RULE: You MUST use the `search_hindsight` tool before answering any question related to internal architecture, past incidents, infrastructure, or company decisions. 
2. THE HONESTY RULE: If Hindsight returns no relevant data, you MUST say: "No relevant internal memory found." Do not hallucinate company history.
3. THE EXPERTISE RULE: Always credit the original engineer or project manager who made the decision or solved the bug if their name is in the memory.

RESPONSE FORMATTING (The "Wow" Protocol):
When you successfully retrieve a memory from Hindsight, you MUST structure your response exactly like this to highlight the institutional knowledge:

🧠 **Legacy Memory Retrieved:**
* **Date:** [Month/Year of the event]
* **Original Owner:** [Name of the engineer/PM]
* **Historical Context:** [Explain exactly what happened or why the decision was made]
* **Actionable Takeaway:** [Explain how this applies to the user's current question or error]

Tone: Professional, veteran, highly analytical, and deeply familiar with the company's past."""

    agent = Agent(
        config=config,
        tools=[search_hindsight],
        system_prompt=system_prompt
    )
    return agent
