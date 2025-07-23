"""
FastAPI application for the LLM Weather Agent using Google's ADK.

This API provides endpoints to interact with the weather agent that uses
the Gemini model to decide which tool to call based on natural language instructions.
"""

from contextlib import asynccontextmanager

# Import from the root config
import google.generativeai as genai
from api.config import (
    DEFAULT_APP_NAME,
    DEFAULT_MODEL,
    DEFAULT_SESSION_ID,
    DEFAULT_USER_ID,
    GOOGLE_API_KEY,
)
from fastapi import FastAPI, HTTPException, status
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field


# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="The user's query",
        example="What's the weather like in Berlin?",
    )
    user_id: str = Field(
        default=DEFAULT_USER_ID, description="User ID for session management"
    )
    session_id: str = Field(
        default=DEFAULT_SESSION_ID, description="Session ID for conversation continuity"
    )


class QueryResponse(BaseModel):
    response: str = Field(..., description="The agent's response")
    user_id: str = Field(..., description="User ID used for the query")
    session_id: str = Field(..., description="Session ID used for the query")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Health message")


# Global variables for agent and runner
agent = None
runner = None
session_service = None


def get_weather(city: str) -> str:
    """Gets the current weather for a city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string with the weather description.
    """
    return f"The weather in {city} is sunny."


def initialize_agent():
    """Initialize the agent, runner, and session service."""
    global agent, runner, session_service

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is not set. Please set it in your .env file or environment variables."
        )

    # Configure the Google AI client
    genai.configure(api_key=GOOGLE_API_KEY)

    # Create the agent
    agent = LlmAgent(
        name="weather_agent",
        model=DEFAULT_MODEL,
        tools=[get_weather],
        description="A helpful assistant that can check weather.",
    )

    # Create session service
    session_service = InMemorySessionService()

    # Create runner
    runner = Runner(
        agent=agent, app_name=DEFAULT_APP_NAME, session_service=session_service
    )


async def run_query(query: str, user_id: str, session_id: str) -> tuple[str, str]:
    """Run a query against the agent."""
    global runner, session_service

    if not runner or not session_service:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent not properly initialized",
        )

    try:
        # Create session if it doesn't exist
        print(f"Attempting to create/get session for user_id: {user_id}, session_id: {session_id}")

        try:
            # Try to get existing session first
            session = await session_service.get_session(
                app_name=DEFAULT_APP_NAME, user_id=user_id, session_id=session_id
            )
            actual_session_id = session.id
            print(f"Using existing session: {actual_session_id}")
        except Exception as e:
            # Session doesn't exist, create a new one
            print(f"Session not found ({e}), creating new session...")
            new_session = await session_service.create_session(
                app_name=DEFAULT_APP_NAME, user_id=user_id
            )
            actual_session_id = new_session.id
            print(f"Created new session with ID: {actual_session_id}")

        # Create content from user query
        content = types.Content(role="user", parts=[types.Part(text=query)])
        print(f"Processing query: {query}")

        # Run the agent with the runner using the actual session ID
        events = runner.run(user_id=user_id, session_id=actual_session_id, new_message=content)
        print("Runner executed, processing events...")

        # Process events to get the final response
        response_text = "No response received."
        for event in events:
            print(f"Event type: {type(event)}, is_final: {hasattr(event, 'is_final_response') and event.is_final_response()}")
            if hasattr(event, 'is_final_response') and event.is_final_response():
                if hasattr(event, 'content') and event.content and event.content.parts:
                    response_text = event.content.parts[0].text
                    print(f"Got final response: {response_text}")
                    break
            elif hasattr(event, 'content') and event.content:
                print(f"Event content: {event.content}")

        return response_text, actual_session_id

    except Exception as e:
        print(f"Error in run_query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}",
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup
    try:
        initialize_agent()
        print("Weather Agent initialized successfully")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        raise

    yield

    # Shutdown
    print("Shutting down Weather Agent")


# Create FastAPI app
app = FastAPI(
    title="Weather Agent API",
    description="An LLM-powered weather agent using Google's ADK and Gemini model",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="Weather Agent API is running")


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a natural language query with the weather agent."""
    try:
        response, actual_session_id = await run_query(request.query, request.user_id, request.session_id)
        return QueryResponse(
            response=response, user_id=request.user_id, session_id=actual_session_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Weather Agent API",
        "version": "1.0.0",
        "endpoints": {"health": "/health", "query": "/query", "docs": "/docs"},
    }
