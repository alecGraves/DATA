'''
    This program packages the labels and images 
from the underwater dataset and converts them 
to a .npz numpy array file.

    Thanks, Thomas, for labeling all of those images.
        -shadySource
'''
import os
import sys
import json
import PIL.Image
import numpy as np

debug = False #only load 10 images
shuffle = False # shuffle dataset

label_dict = {"red_buoy":0, "green_buoy":1, "yellow_buoy":2, 
            "path_marker":3, "start_gate":4, "channel":5}

text = []
for filename in os.listdir('labels'):
    f = open(os.path.join('labels', filename), 'r')
    text.append(f.read())
text = '\n\n'.join(text)
image_labels = text.split('\n\n')
image_labels = [i.split('\n') for i in image_labels]

for i, s in enumerate(image_labels):# all labels
    dataset_start = image_labels[i][0].find('data') # where the URL becomes = to path
    image_labels[i][0] = s[0][dataset_start:].split("/") # replace with path strings, easier to get to
    for j, box in enumerate(s):# box positions
        if j != 0: # not the path string
            box = box.split(' ')

            box[0] = label_dict[box[0]] # convert labels to ints

            for k in  range(1, 5): # Change box boundaries from str to int
                box[k] = int(box[k])

            # rearrange box to label, x_min, y_min, x_max, y_max
            if box[2] > box[4]:
                box[2], box[4] = box[4], box[2]
            if box[1] > box[3]:
                box[1], box[3] = box[3], box[1]

            image_labels[i][j] = box

# load images
images = []
for i, label in enumerate(image_labels):
    img = np.array(PIL.Image.open(os.path.join(label[0][0], label[0][1], label[0][2])))
    images.append(img)
    if debug and i == 9:
        break

#convert to numpy for saving
images = np.asarray(images, dtype=np.uint8)
image_labels = [np.array(i[1:]) for i in image_labels]# remove the file names
image_labels = np.array(image_labels)

#shuffle dataset
if shuffle:
    np.random.seed(13)
    indices = np.arange(len(images))
    np.random.shuffle(indices)
    images, image_labels = images[indices], image_labels[indices]

#save dataset
np.savez("my_dataset", images=images, boxes=image_labels)
print('Data saved: my_dataset.npz')
