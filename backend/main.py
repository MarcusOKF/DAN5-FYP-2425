from fastapi import FastAPI, status
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List

url = config("SUPABASE_URL")
key = config("SUPABASE_KEY")

app = FastAPI()
supabase: Client = create_client(url, key)

@app.get("/moments")
def get_moments():
    moments = supabase.table("moment").select("*").execute()

    return moments

@app.get("/moment/{id}")
def get_moment(id: int):
    moment = supabase.table("moment").select("*").eq("id", id).execute()
    return moment

class Moment(BaseModel):
    video_name: str
    time_start: float
    time_end: float
    embedding: List[float]
    audio_embedding: List[float]


@app.post("/moments", status_code=status.HTTP_201_CREATED)
def create_moment(moment: Moment):
    id = 3
    moment = supabase.table("moment").insert({
        "id": id,
        "video_name": moment.video_name,
        "time_start": moment.time_start,
        "time_end": moment.time_end,
        "embedding": moment.embedding,
        "audio_embedding": moment.audio_embedding
    }).execute()
    return moment

@app.delete("/moment/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_moment(id: int):
    moment = supabase.table("moment").delete().eq("id", id).execute()
    return {"msg": "deleted"}