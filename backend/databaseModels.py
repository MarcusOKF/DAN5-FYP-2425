from pydantic import BaseModel
from typing import List

class Moment(BaseModel):
    video_name: str
    time_start: float
    time_end: float
    embedding: List[float]
    audio_embedding: List[float]