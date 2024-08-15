from pydantic import BaseModel
from typing import Optional

class PlantInput(BaseModel):
    location: str
    sunlight: str
    garden_type: str
    spread: str

class PlantOutput(BaseModel):
    botanical_name: str
    common_name: Optional[str] = None
    temperature: float
    plant_type: str
    similarity_score: float