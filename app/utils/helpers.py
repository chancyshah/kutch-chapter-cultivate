from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import folium
import requests
import logging
import time
import re


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_coordinates(address, max_retries=3, delay=2):
    geolocator = Nominatim(user_agent="cultivate_app")
    
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                logger.info(f"Successfully geocoded address: {address}")
                return location.latitude, location.longitude
            else:
                logger.warning(f"No results found for address: {address}")
                return None, None
        except GeocoderTimedOut:
            logger.warning(f"Timeout error on attempt {attempt + 1} for address: {address}")
            if attempt + 1 == max_retries:
                logger.error(f"Max retries reached for address: {address}")
                return None, None
            time.sleep(delay)
        except GeocoderServiceError as e:
            logger.error(f"Service error for address {address}: {str(e)}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error for address {address}: {str(e)}")
            return None, None

    return None, None

def clean_plant_name(name):
    # Remove any content within parentheses
    name = re.sub(r'\([^)]*\)', '', name)
    # Remove any punctuation or symbols, except spaces
    name = re.sub(r'[^\w\s]', '', name)
    # Remove any extra whitespace
    name = ' '.join(name.split())
    return name

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon]).add_to(m)
    return m

def search_plants(backend_url, location, sunlight, garden_type, spread):
    logger.debug(f"Searching plants with params: location={location}, sunlight={sunlight}, garden_type={garden_type}, spread={spread}")
    try:
        response = requests.post(
            f"{backend_url}/search_plants",
            json={
                "location": location,
                "sunlight": sunlight,
                "garden_type": garden_type,
                "spread": spread
            },
            timeout=10
        )
        response.raise_for_status()
        results = response.json()
        logger.debug(f"API returned {len(results)} results")
        return results
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while fetching plant recommendations: {str(e)}")
        return None
