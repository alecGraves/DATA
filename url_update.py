"""
updates url.txt for the data labeling tool on my website
"""
import os

os.remove('url.txt')
dirs = os.listdir()

for i in dirs:
    if '.' in i:
        dirs.remove(i)

for i in dirs:
    if not os.path.isdir(i):
        dirs.remove(i)

with open('url.txt', 'w') as f:
    for i in dirs:
        f.write(i + ' ')
    f.write('\n')

    for i in dirs:
        images = os.listdir(i)
        for name in images:
            if " " in name:
                os.rename(os.path.join(i, name), os.path.join(i, name.replace(" ", "_")))
            f.write('https://github.com/shadySource/DATA/raw/master/'+i+'/'+name+' ')
        f.write('\n')
