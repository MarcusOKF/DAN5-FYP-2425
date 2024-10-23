import cv2


def extract_frames_from_video_path(video_path, interval_seconds):
    vidcap = cv2.VideoCapture(video_path)
    frame_rate = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(frame_rate * interval_seconds)
    
    success, image = vidcap.read()
    count = 0

    frames = []
    while success:
        if count % frame_interval == 0:
            frames.append({
                "timestamp": count/frame_rate,
                "image": image
            })
        success, image = vidcap.read()
        count += 1

    vidcap.release()

    return frames


