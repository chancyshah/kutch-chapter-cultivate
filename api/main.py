from fastapi import FastAPI, HTTPException
from api.models import PlantInput, PlantOutput
from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from geopy.geocoders import Nominatim
import httpx
import rasterio
from datetime import datetime
import os
import logging
from contextlib import contextmanager
import random

SUNLIGHT_MAP = {
    "Full Sunlight": "full_sunlight",
    "Partial Shade": "partial_sunlight",  
    "Full Shade": "full_shade_sunlight"
}

GARDEN_TYPE_MAP = {
    "City Courtyard": "city_courtyard_gardens",
    "Cottage/Informal": "cottage_informal_garden",
    "Wildlife Garden": "wild_life_garden"
}

SPREAD_MAP = {
    "0.1-0.5 meters": "0.1-0.5_meter_spread",
    "0.5-1.0 meters": "0.5-1.0_meter_spread",
    "1.0-1.5 meters": "1.0-1.5_meter_spread"
}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

worldclim_files = []

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Load the CSV file
df = pd.read_csv('data/Complete_Plant_Data_preprocess V2.csv')

# Load the soil data
soil_df = pd.read_csv('data/cleaned_soil_data.csv')

# Convert binary columns to integers
binary_columns = df.columns[df.isin([0, 1]).all()]
df[binary_columns] = df[binary_columns].astype(int)

# Create feature matrix
feature_columns = df.columns.drop(['Botanical Name', 'Common Name'])
X = df[feature_columns].values

# Load WorldClim data
def initialize_worldclim_data():
    global worldclim_files
    worldclim_files = [f for f in os.listdir('data/worldclim') if f.endswith('.tif')]
    worldclim_files.sort()  # Ensure files are in order (01-12)
    logger.info(f"Initialized {len(worldclim_files)} WorldClim data files")

@contextmanager
def open_worldclim_data(month):
    try:
        with rasterio.open(f'data/worldclim/{worldclim_files[month]}') as src:
            yield src
    except RasterioIOError as e:
        logger.error(f"Error opening WorldClim data for month {month}: {e}")
        raise


def get_min_temperature(lat: float, lon: float) -> float:
    logger.debug(f"Getting minimum temperature for coordinates: lat={lat}, lon={lon}")
    current_month = datetime.now().month - 1  # 0-based index
    try:
        with open_worldclim_data(current_month) as src:
            sample = list(src.sample([(lon, lat)]))
            if not sample:
                logger.warning(f"No temperature data found for coordinates: lat={lat}, lon={lon}")
                return None
            return sample[0][0] / 10  # WorldClim data is in °C * 10
    except RasterioIOError as e:
        logger.error(f"RasterioIOError in get_min_temperature: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error in get_min_temperature: {e}")
        return None

async def get_soil_type(lat: float, lon: float) -> str:
    logger.debug(f"Getting soil type for coordinates: {lat}, {lon}")
    # Round the latitude and longitude to the nearest 0.5 degree
    lat_rounded = round(lat * 2) / 2
    lon_rounded = round(lon * 2) / 2
    
    # Try to get soil type from local CSV first
    local_soil = soil_df[(soil_df['latitude'] == lat_rounded) & (soil_df['longitude'] == lon_rounded)]
    if not local_soil.empty:
        soil_type = local_soil['soil_type_name'].iloc[0].lower()
        return soil_type_to_category(soil_type)
    
    # If not found in local CSV, use external API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url="https://api-test.openepi.io/soil/type",
                params={"lat": lat, "lon": lon},
            )
            response.raise_for_status()
            json = response.json()
            api_soil_type = json["properties"]["most_probable_soil_type"]
            return soil_type_to_category(api_soil_type)
        except Exception as e:
            print(f"Error getting soil type: {e}")
            return "loam"  # Default to loam if there's an error

def soil_type_to_category(soil_type: str) -> str:
    soil_type = soil_type.lower()
    if any(type in soil_type for type in ["vertisol", "gleysol", "cambisol", "nitisol"]):
        return "clay"
    elif any(type in soil_type for type in ["arenosol", "fluvisol"]):
        return "sand"
    elif any(type in soil_type for type in ["andosol", "chernozem", "phaeozem", "regosol"]):
        return "loam"
    elif "rendzina" in soil_type:
        return "chalk"
    else:
        return "loam"  # Default to loam if soil type is not recognized

def get_hardiness(temperature: float) -> str:
    logger.debug(f"Getting hardiness for temperature: {temperature}")
    hardiness_ranges = [
        (15, float('inf'), "H1A_Hardiness"),
        (10, 15, "H1B_Hardiness"),
        (5, 10, "H1C_Hardiness"),
        (1, 5, "H2_Hardiness"),
        (float('-inf'), 1, "H3_Hardiness")
    ]
    for min_temp, max_temp, hardiness in hardiness_ranges:
        if min_temp <= temperature < max_temp:
            return hardiness

def get_plant_type(row: pd.Series) -> str:
    plant_types = [
        ('bedding_plant', 'Bedding Plant'),
        ('climber_wall_shrub', 'Climber/Wall Shrub'),
        ('herbaceous_perennial', 'Herbaceous Perennial'),
        ('houseplant', 'Houseplant'),
        ('shrubs', 'Shrub')
    ]
    return ', '.join(name for col, name in plant_types if row[col])

@app.on_event("startup")
async def startup_event():
    initialize_worldclim_data()

@app.post("/search_plants", response_model=List[PlantOutput])
async def search_plants_endpoint(plant_input: PlantInput):
    try:
        logger.debug(f"Received plant search request: {plant_input}")
        
        # Map the input values to the expected format
        sunlight = SUNLIGHT_MAP.get(plant_input.sunlight)
        garden_type = GARDEN_TYPE_MAP.get(plant_input.garden_type)
        spread = SPREAD_MAP.get(plant_input.spread)

        if not all([sunlight, garden_type, spread]):
            raise ValueError("Invalid input values")

        # Assuming df is your pandas DataFrame containing plant data
        # Filter the DataFrame based on the input criteria
        filtered_df = df[
            (df[sunlight] == 1) &
            (df[garden_type] == 1) &
            (df[spread] == 1)
        ]

        # If 'similarity_score' doesn't exist, we'll use a random selection
        if 'similarity_score' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('similarity_score', ascending=False)
        else:
            filtered_df = filtered_df.sample(frac=1)  # Shuffle the DataFrame

        # Convert the top results to a list of PlantOutput objects
        results = []
        for _, row in filtered_df.head(5).iterrows():
            common_name = row.get('Common Name')
            # Convert NaN to None for common_name
            if pd.isna(common_name):
                common_name = None
            
            results.append(PlantOutput(
                botanical_name=row['Botanical Name'],
                common_name=common_name,
                temperature=float(row.get('Min Temperature', 20.0)),  # Ensure this is a float
                plant_type=str(row.get('Plant Type', 'Unknown')),  # Ensure this is a string
                similarity_score=float(row.get('similarity_score', random.random()))  # Ensure this is a float
            ))

        logger.debug(f"Returning {len(results)} plants")
        return results
    except KeyError as e:
        logger.exception(f"KeyError occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: Column {str(e)} not found")
    except Exception as e:
        logger.exception("An error occurred while searching for plants")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_endpoint():
    return {"message": "FastAPI is running correctly"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    print("Starting FastAPI server...")
    print("Available routes:")
    for route in app.routes:
        print(f"  {route.methods} {route.path}")
    uvicorn.run(app, host="0.0.0.0", port=8000)