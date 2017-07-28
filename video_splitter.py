import os
import sys

debug=True

if len(sys.argv) > 1:
    videoDir = sys.argv[1]
else:
    videoDir = 'videos'

vids = os.listdir(videoDir)
if debug:
    print(vids)

for vid in vids:
    if vid[-4:].lower() == ".mp4":
        if not os.path.exists("split_vids"):
            os.makedirs("split_vids")
        os.system('ffmpeg -i ' + os.path.join(videoDir, vid)  + ' -s  640x480 -r 1 ' + os.path.join("split_vids", vid[:-4]+'images%4d.jpg'))


