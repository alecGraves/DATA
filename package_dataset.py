'''
    This program packages the labels and images 
from the underwater dataset and converts them 
to an hdf5 database file.

    Thanks, Thomas, for labeling all of those images.
        -shadySource
'''
import os
import sys
import json
import PIL.Image
import numpy as np

debug = False #only load 10 images

label_dict = {"red_buoy":0, "green_buoy":1, "yellow_buoy":2, 
            "path_marker":3, "start_gate":4, "channel":5}


text = ''
for filename in os.listdir('labels'):
    f = open(os.path.join('labels', filename), 'r')
    text += f.read()[:]
text = text.replace('\n\n\n','\n\n')
image_labels = text.split('\n\n')
image_labels = [i.split('\n') for i in image_labels]

dataset_start = image_labels[0][0].find('underwater') # where the URL becomes = to path
for i, s in enumerate(image_labels):# all labels
    if 'http' in s[0]:
        image_labels[i][0] = s[0][dataset_start:].split("/") #  replace with path strings, easier to get to
        for j, box in enumerate(s):# box positions
            if j != 0: # not the path string
                box = box.split(' ')

                box[0] = label_dict[box[0]] # convert labels to ints

                for k in  range(len(box)): # Change box boundaries from str to int
                    box[k] = int(box[k])

                # rearrange box to label, x_min, y_min, x_max, y_max
                if box[2] > box[4]:
                    box[2], box[4] = box[4], box[2]
                if box[1] > box[3]:
                    box[1], box[3] = box[3], box[1]

                image_labels[i][j] = box

    else: # first label is not a URL
        del image_labels[i] #invalid label

# load images
images = []
for i, label in enumerate(image_labels):
    img = np.array(PIL.Image.open(os.path.join('data', label[0][0], label[0][1])))
    images.append(img)
    if debug and i == 9:
        break

#shuffle dataset
np.random.seed(13)
shuffle = [(images[i], image_labels[i]) for i in range(len(images))]
np.random.shuffle(shuffle)
images = [pair[0] for pair in shuffle]
image_labels = [pair[1] for pair in shuffle]



#convert to numpy for saving
images = np.asarray(images, dtype=np.uint8)
image_labels = [np.array(i[1:]) for i in image_labels]# remove the file names
image_labels = np.array(image_labels)

#save dataset
np.savez("underwater_data", images=images, boxes=image_labels)
print('Data saved: underwater_data.npz')
