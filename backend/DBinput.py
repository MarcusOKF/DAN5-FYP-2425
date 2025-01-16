from databaseClient import supabase
from databaseModels import Moment

def insert_data_into_table(youtube_url,start_time,end_time,CLIP_embedding,CLIP4CLIP_embedding):
    response = (
    supabase.from_("moment_nathan")
    .insert(
        [
            {
                "youtube_url": youtube_url,
                "start_time": start_time,
                "end_time": end_time,
                "CLIP_embedding": CLIP_embedding,
                "CLIP4CLIP_embedding": CLIP4CLIP_embedding,
            }
        ]
    )
    .execute()
    )

import os, fnmatch
def find(pattern):
    path= os.getcwd()
    result = None
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result=os.path.join(root, name)
    return result
