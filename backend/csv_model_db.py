from youtube import youtube_video_retrieve
from DBinput import insert_data_into_table,find
from CLIP4CLIP import CLIP4CLIP
from CLIP import CLIP
from microseconds import convert_microseconds_to_hms
import subprocess
import os
#read the excel video_cc_public then (1) separate into moments then run clip4clip, get frames and run clip, store into DB

#connect to csv
import csv

with open('video_cc_public.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Check if the row has at least 3 columns
        youtube_url = row[0]
        start_time = row[1]
        end_time = row[2]
        description = row[3]
        #download youtube vid
        youtube_video_retrieve(youtube_url)
        start_time = convert_microseconds_to_hms(int(start_time))
        end_time = convert_microseconds_to_hms(int(end_time))
        start_time_hms=str(start_time[0])+":"+str(start_time[1])+":"+str(start_time[2])
        end_time_hms=str(end_time[0])+":"+str(end_time[1])+":"+str(end_time[2])
        subprocess.run(["scene-detect", "-s",start_time_hms,"-i","%s.mp4"%youtube_url,"-e",end_time_hms,"-t","0.1","-f","sec","-o","time.txt"]) 
        subprocess.run(["scene-images","-i","%s.mp4"%youtube_url,"-c","time.txt"])
        subprocess.run(["scene-time","-i","time.txt","-o","cutlist.txt"])
        subprocess.run(["scene-cut","-i","%s.mp4"%youtube_url,"-c","cutlist.txt"])
        
        os.remove(youtube_url+".mp4")
        previous_time=0
        with open("time.txt") as file:
            for line in file:
                line=line.rstrip()
                mp4_path=find("%s-[[]%s-00:00:00[]].mp4"%(youtube_url,line))
                png_path=find("%s-[[]%s[]].png"%(youtube_url,line))
                print(mp4_path)
                print(png_path)
                video_embeddings=CLIP4CLIP(mp4_path)
                image_embeddings=CLIP(png_path)
                os.remove(mp4_path)
                os.remove(png_path)
                previous_time=line
                insert_data_into_table(youtube_url,previous_time,line,image_embeddings,video_embeddings)
                # os.remove("time.txt")
                # os.remove("cutlist.txt")
        break
#####################################################################################################
# #cut the video according to start time & end time 

# import os
# import ffmpeg
# start_time_microseconds = 5000000
# end_time_microseconds = 850000000
# def trim(in_file, out_file, start, end):
#     if os.path.exists(out_file):
#         os.remove(out_file)

#     in_file_probe_result = ffmpeg.probe(in_file)
#     in_file_duration = in_file_probe_result.get(
#         "format", {}).get("duration", None)
#     print(in_file_duration)

#     input_stream = ffmpeg.input(in_file)

#     pts = "PTS-STARTPTS"
#     video = input_stream.trim(start=start, end=end).setpts(pts)
#     audio = (input_stream
#              .filter_("atrim", start=start, end=end)
#              .filter_("asetpts", pts))
#     video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
#     output = ffmpeg.output(video_and_audio, out_file, format="mp4")
#     output.run()

#     out_file_probe_result = ffmpeg.probe(out_file)
#     out_file_duration = out_file_probe_result.get(
#         "format", {}).get("duration", None)
#     print(out_file_duration)
# trim("test1.mp4","output.mp4",start_time_microseconds/1000000,end_time_microseconds/1000000)
#####################################################################################################

