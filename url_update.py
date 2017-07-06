"""
updates url.txt for the open data labeling tool on shadysource.github.io
"""
import os

try:
    os.remove('url.txt')
except:
    pass
dirs = os.listdir('data')
dirs.sort()

for i in dirs:
    if '.' in i:
        dirs.remove(i)

with open('url.txt', 'w') as f:
    for i in dirs:
        f.write(i + ' ')
    f.write('\n')

    for i in dirs:
        images = os.listdir(os.path.join('data',i))
        for name in images:
            if " " in name:
                os.rename(os.path.join('data',i, name), os.path.join('data',i, name.replace(" ", "_")))
            f.write('https://github.com/shadySource/DATA/raw/master/data/'+i+'/'+name+' ')
        f.write('\n')
