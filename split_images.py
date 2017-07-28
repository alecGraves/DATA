import os

foldername = "split_vids"

for i, img in enumerate( os.listdir(foldername)):
    for j in range(0, 10, 1)
        if (i%10) == j:
            if not os.path.exists(str(j)):
                os.makedirs(str(j))
            os.rename(os.path.join(foldername, img), os.path.join(str(j), img))
