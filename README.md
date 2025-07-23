# AI Agents Course

A comprehensive hands-on course for building intelligent agents using Google's ADK (Agent Development Kit) and various APIs. This repository contains practical examples and implementations of AI agents ranging from simple prototypes to production-ready services.

## Overview

This course demonstrates how to build AI agents with different capabilities and deployment patterns:

- **Weather Agent**: A comprehensive weather assistant with real-time forecasts
- **Multi-Tool Agent**: A basic agent demonstrating fundamental tool integration
- **FastAPI Application**: Production-ready web service with LLM agents
- **MCP Agent**: Advanced agent using Model Context Protocol for external tool integration

## Examples

### 🚀 **FastAPI Application** (`api/`)
- **Production-ready web service** with FastAPI
- Session management using `InMemorySessionService`
- RESTful endpoints for agent interactions
- Health checks and API documentation
- **Use case**: Scalable web service for agent deployment

### 🔧 **MCP Agent** (`mcp_agent/`)
- **Model Context Protocol** integration for external tools
- Filesystem operations (list directories, read files)
- Google Maps API integration for location services
- Dynamic tool loading from MCP servers
- **Use case**: Enterprise integrations with existing tools and services

### 🌤️ **Weather Agent** (`weather_agent/`)
- **Real weather data** via Open-Meteo API
- Geographic intelligence with geocoding
- Timezone awareness and localization
- Comprehensive error handling and logging
- **Use case**: Production weather service with real-time data

### ⚡ **Multi-Tool Agent** (`multi_tool_agent/`)
- Simple weather and time functions
- Basic tool integration patterns
- Educational implementation
- **Use case**: Learning agent fundamentals and prototyping

## Features

### Core ADK Components Demonstrated
- **LlmAgent & Agent classes**: Different agent types and configurations
- **Runner**: Execution engine for agent workflows
- **SessionService**: State management and conversation continuity
- **Tool Integration**: Multiple patterns for external API integration

### Advanced Features
- **Caching**: Intelligent HTTP caching to reduce API calls
- **Retry Logic**: Automatic retry with exponential backoff
- **Error Handling**: Robust error handling with user-friendly messages
- **Logging**: Comprehensive logging for debugging and monitoring
- **Session Management**: Multi-user conversation state handling

## Requirements

- Python 3.11+
- Google ADK (Agent Development Kit)
- Internet connection for API access
- Optional: Google Maps API key (for MCP agent)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd course
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

3. Set up environment variables (optional):

Follow the `.env.example` in each folder.

## Quick Start

### FastAPI Web Service

```bash
# Start the web service
uvicorn api.main:app --reload

# Test the API
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What'\''s the weather in Tokyo?"}'
```

### Weather Agent (Advanced)

```python
from weather_agent.agent import root_agent

# Natural language weather queries
response = root_agent.query("What's the weather in Paris, France?")
print(response)
```

### MCP Agent (Filesystem + Maps)

```python
from mcp_agent.agent import root_agent

# File operations and mapping queries
response = root_agent.query("List files in the current directory")
print(response)

response = root_agent.query("Find directions from New York to Boston")
print(response)
```

### Multi-Tool Agent (Basic)

```python
from multi_tool_agent.agent import root_agent

# Simple queries for demonstration
response = root_agent.query("What time is it in New York?")
print(response)
```

## API Endpoints (FastAPI Application)

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /query` - Process natural language queries
- `GET /docs` - Interactive API documentation

### Example API Usage

```python
import requests

# Query the weather agent via REST API
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What's the weather like in Berlin?",
        "user_id": "user123",
        "session_id": "session456"
    }
)

result = response.json()
print(result["response"])
```

## Dependencies

### Core Dependencies
- **google-adk**: Agent Development Kit framework
- **fastapi**: Modern web framework for APIs
- **pydantic**: Data validation and settings management

### Weather & Location Services
- **openmeteo-requests**: Weather data API client
- **geopy**: Geocoding services for location resolution
- **timezonefinder**: Timezone detection from coordinates

### Data Processing & Utilities
- **pandas**: Data manipulation and analysis
- **requests-cache**: HTTP caching for improved performance
- **retry-requests**: Automatic retry logic for HTTP requests

### Development & Documentation
- **uvicorn**: ASGI server for FastAPI
- **docling**: Document processing capabilities

## Architecture

### FastAPI Application Architecture

1. **Lifespan Management**: Automatic agent initialization on startup
2. **Session Handling**: Per-user conversation state management
3. **Error Handling**: Comprehensive HTTP error responses
4. **API Documentation**: Auto-generated OpenAPI documentation

### MCP Integration Pattern

1. **Tool Discovery**: Dynamic loading of tools from MCP servers
2. **Process Management**: Handles external process communication
3. **Environment Isolation**: Secure execution of external tools
4. **Error Recovery**: Graceful handling of tool failures

### Weather Agent Workflow

1. **Location Resolution**: Geocoding city names to coordinates
2. **Timezone Detection**: Determining local timezone from coordinates
3. **Data Fetching**: Retrieving weather forecasts from Open-Meteo
4. **Response Generation**: AI-powered natural language responses

## Project Structure

```
course/
├── api/                   # FastAPI web service
│   ├── __init__.py
│   ├── main.py           # FastAPI application with agent integration
│   └── config.py         # Configuration settings
├── mcp_agent/            # Model Context Protocol agent
│   ├── __init__.py
│   └── agent.py          # MCP agent with filesystem and maps tools
├── weather_agent/        # Advanced weather agent
│   ├── __init__.py
│   └── agent.py          # Real weather data with full functionality
├── multi_tool_agent/     # Basic multi-tool example
│   ├── __init__.py
│   └── agent.py          # Simple weather and time agent
├── data/                 # Sample documents and training data
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Dependency lock file
└── README.md            # This documentation
```

## Configuration

### Environment Variables

```bash
# Required for MCP agent with Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Required for FastAPI application
GOOGLE_API_KEY=your_gemini_api_key

# Optional: Custom model selection
DEFAULT_MODEL=gemini-2.0-flash
```

### Caching Configuration
- **Weather data**: Cached for 1 hour to reduce API calls
- **Geocoding results**: Cached to improve response times
- **Session data**: In-memory storage for development

## Usage Examples

### Production Deployment

```python
# FastAPI production deployment
from api.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4
    )
```

### Batch Processing

```python
from weather_agent.agent import root_agent

# Process multiple cities
cities = [
    "Tokyo, Japan",
    "London, UK",
    "New York, USA",
    "Sydney, Australia"
]

for city in cities:
    response = root_agent.query(f"What's the weather in {city}?")
    print(f"{city}: {response}\n")
```

### Custom Tool Integration

```python
from google.adk.agents import LlmAgent

def custom_tool(parameter: str) -> str:
    """Custom tool implementation."""
    return f"Processed: {parameter}"

# Create agent with custom tools
agent = LlmAgent(
    name="custom_agent",
    model="gemini-2.0-flash",
    tools=[custom_tool],
    description="Agent with custom functionality"
)
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_weather_agent.py

# Run with coverage
python -m pytest --cov=course
```

### Development Setup

```bash
# Create development environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv sync --dev

# Run linting
ruff check course/
ruff format course/
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration

```bash
# Production environment variables
export GOOGLE_API_KEY=your_production_api_key
export GOOGLE_MAPS_API_KEY=your_maps_api_key
export DEFAULT_MODEL=gemini-2.0-flash
export LOG_LEVEL=INFO
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## License

This project is for educational purposes. Please check individual API terms of service for commercial usage.

## APIs Used

- **Open-Meteo**: Free weather API (no API key required)
- **Nominatim**: OpenStreetMap geocoding service
- **Google Maps API**: Location and directions services
- **Google ADK**: Agent Development Kit for AI agents
- **Model Context Protocol**: Tool integration standard

## Troubleshooting

### Common Issues

1. **ImportError**: Ensure you've installed dependencies with `uv sync`
2. **API Key Issues**: Check environment variables are set correctly
3. **Network Errors**: Verify internet connection and API availability
4. **MCP Server Issues**: Ensure Node.js is installed for npx commands

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m uvicorn api.main:app --log-level debug
```

## Support

For questions or issues:
1. Check the existing documentation and examples
2. Review the troubleshooting section
3. Search existing issues in the repository
4. Create a new issue with detailed information

---

*This course demonstrates practical AI agent development patterns using Google's ADK, from simple prototypes to production-ready services with comprehensive tool integration.*
