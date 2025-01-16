from pytubefix import YouTube
from pytubefix.cli import on_progress

def youtube_video_retrieve(youtube_url):
    url = "https://www.youtube.com/watch?v="+youtube_url
    
    yt = YouTube(url, on_progress_callback = on_progress)
    yt.title=youtube_url
    
    ys = yt.streams.get_highest_resolution()
    ys.download()