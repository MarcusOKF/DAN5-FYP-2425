# packages
from fastapi import FastAPI, status
from decouple import config
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uuid
import secrets
import torch
import json

# modules
from databaseClient import supabase
from databaseModels import Moment
from models.CLIP.CLIP import vectoriz_text_CLIP, vectorize_frame_CLIP, batch_vectorize_frames_CLIP
from frame_extractor import extract_frames_from_video_path

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
@app.post("/vectorize/{name}", status_code=status.HTTP_201_CREATED)
def vectorize(name: str):
    path = f'{CDNURL}/{name}'

    frames = extract_frames_from_video_path(path, 2) # frames = [{timestamp: float, image: ndarray}]

    frames_rbg_vals = list(map(lambda f: f["image"], frames))

    frame_vectors = batch_vectorize_frames_CLIP(frames_rbg_vals)

    # Map all the info to a database model
    for i in range(len(frames)):
        frames[i] = {
            "id": secrets.randbelow(10**8),
            "video_name": name,
            "timestamp": frames[i]["timestamp"],
            "embedding": frame_vectors[i].tolist(),
        }

    supabase.table("frame").insert(frames).execute()

    print(frames[3])

    return "OK"
 

@app.post("/moments", status_code=status.HTTP_201_CREATED)
def create_moment(moment: Moment):
    moment = supabase.table("moment").insert({
        "id": secrets.randbelow(10**8),
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

