# Weather Agent API

A FastAPI-based REST API that provides natural language weather queries powered by Google's ADK (Agent Development Kit) and Gemini 2.0 Flash model.

## Features

- **Natural Language Processing**: Ask weather questions in plain English
- **Session Management**: Maintains conversation context across multiple queries
- **RESTful API**: Clean, documented endpoints with OpenAPI/Swagger integration
- **Error Handling**: Comprehensive error responses and logging
- **Health Monitoring**: Built-in health check endpoint

## Prerequisites

- Python 3.8+
- Google API Key with access to Gemini models
- FastAPI and dependencies (see requirements)

## Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd course/api
   ```

2. **Install dependencies**

   ```bash
   pip install fastapi uvicorn google-generativeai google-adk
   ```

3. **Set up environment variables**
   Create a `.env` file or set environment variables:
   ```bash
   export GOOGLE_API_KEY="your-google-api-key-here"
   ```

## Quick Start

1. **Start the server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What'\''s the weather like in Berlin?"}'
   ```

## API Endpoints

### Health Check

```http
GET /health
```

Returns the health status of the API.

**Response:**

```json
{
  "status": "healthy",
  "message": "Weather Agent API is running"
}
```

### Query Weather

```http
POST /query
```

Process a natural language weather query.

**Request Body:**

```json
{
  "query": "What's the weather like in Berlin?",
  "user_id": "user123",
  "session_id": "session456"
}
```

**Parameters:**

- `query` (required): Your weather question in natural language
- `user_id` (optional): User identifier for session management (default: "user123")
- `session_id` (optional): Session identifier for conversation continuity (default: "session456")

**Response:**

```json
{
  "response": "The weather in Berlin is sunny.",
  "user_id": "user123",
  "session_id": "session456"
}
```

### Root Endpoint

```http
GET /
```

Returns basic API information and available endpoints.

## Usage Examples

### Simple Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What'\''s the weather like in Berlin?"}'
```

### Follow-up Query with Session

```bash
# First query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What'\''s the weather like in Berlin?",
    "user_id": "user123",
    "session_id": "conversation1"
  }'

# Follow-up query in same session
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How about Paris?",
    "user_id": "user123",
    "session_id": "conversation1"
  }'
```

### Multiple Users

```bash
# User 1
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Weather in Tokyo?",
    "user_id": "alice",
    "session_id": "alice_session"
  }'

# User 2
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How about London?",
    "user_id": "bob",
    "session_id": "bob_session"
  }'
```

## Configuration

The API can be configured through environment variables or by modifying `config.py`:

```python
DEFAULT_APP_NAME = "agent"
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_SESSION_ID = "session456"
DEFAULT_USER_ID = "user123"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
```

## Architecture

The API consists of several key components:

- **FastAPI Application**: Web framework handling HTTP requests
- **LLM Agent**: Google ADK agent configured with weather tools
- **Session Service**: In-memory session management for conversation continuity
- **Runner**: Orchestrates agent execution and event processing
- **Weather Tool**: Simple function that returns weather information

## Session Management

Sessions allow the agent to maintain context across multiple queries:

- Sessions are created automatically when first accessed
- Each user can have multiple sessions
- Sessions store conversation history and context
- Use consistent `user_id` and `session_id` for conversation continuity

## Error Handling

The API provides detailed error responses:

- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Server-side errors with detailed messages
- **Initialization Errors**: Logged during startup if configuration is invalid

## Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Running with Debug Mode

```bash
uvicorn main:app --reload --log-level debug
```

### Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/

# Test query endpoint
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Test weather query"}'
```

## Limitations

- Currently returns mock weather data ("sunny" for all cities)
- Sessions are stored in memory (lost on restart)
- Single weather tool implementation
- No authentication or rate limiting

## Future Enhancements

- Integration with real weather APIs (OpenWeatherMap, etc.)
- Persistent session storage (Redis, database)
- Additional weather-related tools (forecasts, alerts, etc.)
- Authentication and authorization
- Rate limiting and caching
- More sophisticated weather data processing

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY is not set"**
   - Ensure your Google API key is properly set in environment variables
   - Verify the API key has access to Gemini models

2. **"Agent not properly initialized"**
   - Check server startup logs for initialization errors
   - Verify all dependencies are installed

3. **"No response received"**
   - Check server logs for event processing details
   - Ensure the agent and runner are properly configured

### Debug Mode

Enable detailed logging by setting log level to debug:

```bash
uvicorn main:app --reload --log-level debug
```
