import sys
import os

foldername = 'footage'

os.mkdir('1')
os.mkdir('2')

for i, img in enumerate( os.listdir(foldername)):
    if (i%2)==0:
        os.rename(os.path.join(foldername, img), os.path.join('1', img))
    else:
        os.rename(os.path.join(foldername, img), os.path.join('2', img))
