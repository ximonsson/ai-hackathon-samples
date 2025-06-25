from datetime import datetime
import httpx
import requests
import pandas as pd
from typing import Dict, Any, Optional


async def geocode_location(query: str, limit: int = 1) -> Optional[Dict[str, Any]]:
    """
    Geocode a location using the Nominatim API.
    
    Args:
        query: The location to search for (e.g., "Paris, France")
        limit: Maximum number of results to return (default: 1)
    
    Returns:
        Dictionary containing the geocoding result or None if not found
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": query,
        "format": "json",
        "limit": limit,
        "addressdetails": 1
    }
    
    headers = {
        "User-Agent": "stormy-mcweatherface/0.1.0"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            results = response.json()
            return results[0] if results else None
            
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


            



def get_weather(lat, lon, user_agent="MyApp/1.0 (oda.johanne.kristensen[at]posten.no)"):
    """
    Get weather forecast from met.no API
    
    Args:
        lat: Latitude
        lon: Longitude  
        user_agent: Your app name and contact info (REQUIRED)
    
    Returns:
        Weather data dictionary or None if failed
    """
    # Round coordinates to 4 decimals (API requirement)
    lat = round(lat, 4)
    lon = round(lon, 4)
    
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    
    headers = {
        'User-Agent': user_agent
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("Error: Invalid User-Agent. Please use your real app name and contact info.")
        elif response.status_code == 429:
            print("Error: Too many requests. Please wait before trying again.")
        else:
            print(f"Error: HTTP {response.status_code}")
            
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    



def main() -> None:
    print("Hello from stormy-mcweatherface!")
