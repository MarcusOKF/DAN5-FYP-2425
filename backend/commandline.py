##scene-detect -s 00:00:10 -i test2.mp4 -e 00:00:50 -t 0.1 -f sec -o time.txt


##scene-images -i test2.mp4 -c time.txt
#made to images for clip models

##scene-time -i output -o cutlist.txt
#format: starttime,duration

##scene-cut -i test2.mp4 -c cutlist.txt
#cut the video according to the cutlist.txt