import logging
from datetime import datetime

import openmeteo_requests
import pandas as pd
import pytz
import requests_cache
from geopy.geocoders import Nominatim
from google.adk.agents import Agent
from retry_requests import retry
from timezonefinder import TimezoneFinder

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
INSTRUCTION = """
You are a helpful weather assistant.

When a user asks for the weather in a city, follow these steps using the available tools:

1. Use `get_coordinates(city, country)` to retrieve the geographic coordinates (latitude and longitude) of the location.
2. Use `get_local_time_info(latitude, longitude)` to determine the timezone of the location.
3. Then use `get_weather_forecast(latitude, longitude, timezone)` to get the hourly weather forecast.
4. If any tool returns an error, politely inform the user that the data couldn't be retrieved.
5. If the forecast is available:
   • Mention the city and country.
   • Display the next few hourly temperature readings in a clear format (e.g., "14:00 — 17°C").
   • Keep your response concise and user-friendly.
6. Never fabricate data. Only use information returned by the tools.
"""

logger = logging.getLogger("tools")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
)
console_handler.setFormatter(formatter)

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Add handler (prevent duplicates)
if not logger.handlers:
    logger.addHandler(console_handler)


def get_local_time_info(latitude: float, longitude: float) -> dict:
    """Retrieves the local time and timezone for the given coordinates.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        dict: {
            "status": "success",
            "timezone": "America/Santiago",
            "local_time": "2025-07-08T14:52:00",
        }
        or {
            "status": "error",
            "error_message": "..."
        }
    """
    logger.info(f"Tool: get_local_time_info called for ({latitude}, {longitude})")

    try:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

        if not timezone_str:
            return {
                "status": "error",
                "error_message": "Could not determine timezone for the coordinates.",
            }

        tz = pytz.timezone(timezone_str)
        local_time = datetime.now(tz).isoformat(timespec="seconds")

        return {
            "status": "success",
            "timezone": timezone_str,
            "local_time": local_time,
        }

    except Exception as e:
        logger.error(f"Timezone resolution error: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to determine timezone or time: {str(e)}",
        }


def get_coordinates(city: str, country: str = "") -> dict:
    """Retrieves the geographic coordinates (latitude and longitude) of a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London").
        country (str, optional): The name of the country to disambiguate (e.g., "USA", "UK").

    Returns:
        dict: A dictionary containing the status and coordinates.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'coordinates' key with (latitude, longitude).
              If 'error', includes an 'error_message' key.
    """
    print(
        f"--- Tool: get_coordinates called for city: {city}, country: {country} ---"
    )  # Log tool execution
    city_normalized = city.strip().title()
    country_normalized = country.strip().title()

    geolocator = Nominatim(user_agent="geoapi")
    query = (
        f"{city_normalized}, {country_normalized}"
        if country_normalized
        else city_normalized
    )

    try:
        location = geolocator.geocode(query)
        if location:
            return {
                "status": "success",
                "coordinates": (location.latitude, location.longitude),  # pyright: ignore
            }
        else:
            return {
                "status": "error",
                "error_message": f"Could not find coordinates for '{query}'.",
            }
    except Exception as e:
        return {"status": "error", "error_message": f"An error occurred: {str(e)}"}


def get_weather_forecast(latitude: float, longitude: float, timezone: str) -> dict:
    """Fetches the current weather forecast for a given location using Open-Meteo API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (str): Timezone string (e.g., 'America/Santiago').

    Returns:
        dict: A dictionary with weather data or error details.
              {
                  "status": "success",
                  "coordinates": (lat, lon),
                  "report": hourly_dataframe (as dict)
              }
              or
              {
                  "status": "error",
                  "error_message": "..."
              }
    """
    logger.info(
        f"Tool: get_weather_forecast called for coordinates: ({latitude}, {longitude}) and timezone: {timezone}"
    )

    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m",
            "timezone": timezone,
        }

        responses = openmeteo.weather_api(FORECAST_API_URL, params=params)
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "temperature_2m": hourly_temperature_2m,
        }

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        return {
            "status": "success",
            "coordinates": (latitude, longitude),
            "report": hourly_dataframe.to_dict(orient="records"),
        }

    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to retrieve weather data: {str(e)}",
        }


root_agent = Agent(
    name="weather_agent_v1",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Provides weather information for any city.",
    instruction=INSTRUCTION,
    tools=[
        get_coordinates,
        get_weather_forecast,
        get_local_time_info,
    ],
)
