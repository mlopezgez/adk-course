# AI Agents Course

A hands-on course for building intelligent agents using Google's ADK (Agent Development Kit) and various APIs. This repository contains practical examples and implementations of AI agents that can interact with external services and provide useful information to users.

## Overview

This course demonstrates how to build AI agents with different capabilities:

- **Weather Agent**: A comprehensive weather assistant that provides real-time weather forecasts for any city worldwide
- **Multi-Tool Agent**: A simpler agent that demonstrates basic tool integration for weather and time information

## Features

### Weather Agent (`weather_agent/`)
- **Real-time Weather Data**: Uses Open-Meteo API for accurate weather forecasts
- **Geographic Intelligence**: Automatically resolves city names to coordinates using geocoding
- **Timezone Awareness**: Provides localized time information for any location
- **Caching**: Implements intelligent caching to reduce API calls and improve performance
- **Error Handling**: Robust error handling with informative user feedback

### Multi-Tool Agent (`multi_tool_agent/`)
- **Simplified Interface**: Basic weather and time queries
- **Tool Integration**: Demonstrates fundamental agent-tool interaction patterns
- **Educational Focus**: Perfect for understanding core agent concepts

## Requirements

- Python 3.11+
- Google ADK (Agent Development Kit)
- Internet connection for API access

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

Or using pip:
```bash
pip install -e .
```

## Quick Start

### Weather Agent

```python
from weather_agent.agent import root_agent

# The agent can handle natural language queries like:
# "What's the weather in Tokyo?"
# "How's the weather in London, UK?"
# "Temperature forecast for New York"

response = root_agent.query("What's the weather in Paris?")
print(response)
```

### Multi-Tool Agent

```python
from multi_tool_agent.agent import root_agent

# Simple queries for demonstration
response = root_agent.query("What time is it in New York?")
print(response)

response = root_agent.query("What's the weather like in New York?")
print(response)
```

## Dependencies

- **google-adk**: Core agent framework
- **openmeteo-requests**: Weather data API client
- **geopy**: Geocoding services for location resolution
- **pandas**: Data manipulation and analysis
- **timezonefinder**: Timezone detection from coordinates
- **requests-cache**: HTTP caching for improved performance
- **litellm**: LLM integration layer
- **docling**: Document processing capabilities

## Architecture

### Weather Agent Architecture

1. **Location Resolution**: Uses Nominatim geocoder to convert city names to coordinates
2. **Timezone Detection**: Determines local timezone using coordinate-based lookup
3. **Weather Data**: Fetches hourly forecasts from Open-Meteo API
4. **Response Generation**: AI agent processes the data and provides natural language responses

### Tool Functions

- `get_coordinates(city, country)`: Resolves geographic coordinates
- `get_local_time_info(latitude, longitude)`: Determines timezone and local time
- `get_weather_forecast(latitude, longitude, timezone)`: Fetches weather data

## Data Directory

The `data/` directory contains sample documents and files that can be used for:
- Document processing examples
- RAG (Retrieval Augmented Generation) implementations
- Company policy and procedure documents (in Spanish)
- Training data for specialized agents

## Configuration

- **Caching**: Weather data is cached for 1 hour to reduce API calls
- **Retry Logic**: Automatic retry with exponential backoff for network requests
- **Logging**: Comprehensive logging for debugging and monitoring

## Development

### Project Structure

```
course/
├── weather_agent/          # Advanced weather agent implementation
│   ├── __init__.py
│   └── agent.py           # Main weather agent with full functionality
├── multi_tool_agent/      # Simple multi-tool agent example
│   ├── __init__.py
│   └── agent.py          # Basic agent implementation
├── data/                 # Sample documents and training data
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

### Environment Setup

1. Create a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install in development mode:
```bash
uv sync
```

## Usage Examples

### Basic Weather Query
```python
from weather_agent.agent import root_agent

# Natural language weather queries
queries = [
    "What's the current weather in Santiago, Chile?",
    "How's the temperature in Mumbai?",
    "Weather forecast for Berlin, Germany",
    "Tell me about the weather in São Paulo"
]

for query in queries:
    response = root_agent.query(query)
    print(f"Query: {query}")
    print(f"Response: {response}\n")
```

### Error Handling
The agents gracefully handle various error conditions:
- Invalid city names
- Network connectivity issues
- API rate limits
- Timezone resolution failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please check individual API terms of service for commercial usage.

## APIs Used

- **Open-Meteo**: Free weather API (no API key required)
- **Nominatim**: OpenStreetMap geocoding service
- **Google ADK**: Agent Development Kit for AI agents

## Support

For questions or issues:
1. Check the existing documentation
2. Review the example implementations
3. Create an issue in the repository

---

*This course is designed to teach practical AI agent development using real-world APIs and modern Python tools.*
