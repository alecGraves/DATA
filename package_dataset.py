'''
    This program packages the labels and images 
from the underwater dataset and converts them 
to a hdf5 database file.

    Thanks, Thomas, for labeling all of those images.
        -shadySource
'''
import os
import h5py
import PIL.Image
import numpy as np



label_dict = {"red_buoy":0, "green_buoy":1, "yellow_buoy":2, 
            "path_marker":3, "start_gate":4, "channel":5}


text = ''
for filename in os.listdir('labels'):
    f = open(os.path.join('labels', filename), 'r')
    text += f.read()[3:] # index to remove garbage at beginning of files
text = text.replace('\n\n\n','\n\n')
image_labels = text.split('\n\n')
image_labels = [i.split('\n') for i in image_labels]

dataset_start = image_labels[0][0].find('underwater') # where the URL becomes = to path

for i, s in enumerate(image_labels):# all labels
    if 'http' in s[0]: # replace with path strings, easier to get to

        image_labels[i][0] = s[0][dataset_start:].split("/")

        for j, box in enumerate(s):# box positions
            if j != 0: # not the URL
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

#convert to numpy for saving
images = np.asarray(images)
image_labels = [np.asarray(i[1:]) for i in image_labels]# remove the file names


#save dataset
split = int(len(images)*.8)

f = h5py.File("underwater.hdf5", "w")

train = f.create_group("train")
test = f.create_group("test")

train_images = train.create_dataset("images", data=images[:split])
test_images = test.create_dataset("images", data=images[split:])

dt = h5py.special_dtype(vlen=np.dtype('int32'))
train_boxes = train.create_dataset("boxes", (len(image_labels[:split]),), dtype=dt)
train_boxes[:split] = image_labels[:split]
test_boxes = test.create_dataset("boxes", (len(image_labels[split:]),), dtype=dt)
train_boxes[split:] = image_labels[split:]
