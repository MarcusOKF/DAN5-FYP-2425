# packages
from fastapi import FastAPI, status
from decouple import config
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# modules
from databaseClient import supabase
from databaseModels import Moment

# Init FastAPI server
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[config("FRONTEND_URL")],allow_methods=["*"])

# Constants
CDNURL = "https://zmoyacveypqxzbgsqqky.supabase.co/storage/v1/object/public/videos"

################################## GET ##################################

@app.get("/moments")
def get_moments():
    moments = supabase.table("moment").select("*").execute()

    return moments

@app.get("/moment/{id}")
def get_moment(id: int):
    moment = supabase.table("moment").select("*").eq("id", id).execute()
    return moment

@app.get("/videos")
def get_videos():
    video = supabase.storage.from_('videos').get_public_url("https://zmoyacveypqxzbgsqqky.supabase.co/storage/v1/object/public/videos/test.mp4?t=2024-10-04T04%3A56%3A02.664Z")

    return video


################################## POST ##################################
@app.post("/vectorize/{video_name}", status_code=status.HTTP_201_CREATED)
def vectorize(video_name: str):
    video_path = f'{CDNURL}/{video_name}'


    return video_path
    # moment = supabase.table("moment").insert({
    #     "id": id,
    #     "video_name": moment.video_name,
    #     "time_start": moment.time_start,
    #     "time_end": moment.time_end,
    #     "embedding": moment.embedding,
    #     "audio_embedding": moment.audio_embedding
    # }).execute()
    # return moment

@app.post("/moments", status_code=status.HTTP_201_CREATED)
def create_moment(moment: Moment):
    id = 4
    moment = supabase.table("moment").insert({
        "id": id,
        "video_name": moment.video_name,
        "time_start": moment.time_start,
        "time_end": moment.time_end,
        "embedding": moment.embedding,
        "audio_embedding": moment.audio_embedding
    }).execute()
    return moment

################################## DELETE ##################################

@app.delete("/moment/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_moment(id: int):
    moment = supabase.table("moment").delete().eq("id", id).execute()
    return {"msg": "deleted"}