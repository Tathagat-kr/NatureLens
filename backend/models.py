from pydantic import BaseModel
from typing import Optional


class ObservationCreate(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[int] = None
    description: Optional[str] = None
    ecological_role: Optional[str] = None
    interesting_fact: Optional[str] = None
    look_closer: Optional[str] = None
    nature_mission: Optional[str] = None
    mission_type: Optional[str] = None
    xp_reward: Optional[int] = 10
    connection_message: Optional[str] = None
    safety_note: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None