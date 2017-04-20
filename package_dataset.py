import os
import h5py
import numpy as np

# create dataset file:
# f = h5py.File("dataset.hdf5", "w")

# get label text
text = ''
for filename in os.listdir('labels'):
    f = open(os.path.join('labels', filename), 'r')
    text += f.read()[3:] # index to remove garbage at beginning of files
text = text.replace('\n\n\n','\n\n')
image_labels = text.split('\n\n')
image_labels = [i.split('\n') for i in image_labels]

print(image_labels[2])
