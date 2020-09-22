# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
import matplotlib.image as mpimg
import os
import PIL.Image as Image
from os import listdir
from os.path import isfile, join
import json
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# %%
label_dir = '/home/marvin/tlt-forklift/data/training/label_2/'
files = [f for f in listdir(label_dir) if isfile(join(label_dir, f))]
filedata = []
width = 640
height = 368

forkliftID = 0
palletID = 1

def parseFile(dir, filename):
    f = open(dir+filename,"r")
    line = f.readline()
    words = line.split()
    label = words[0]
    bbox = [float(i) for i in words[4:8]]
    image_id = filename[0:6]
    return (image_id,label,bbox)


# %%
coco_json = {}
coco_json['images'] = []
coco_json['annotations'] = []
coco_json['categories'] = []
for file in files:
    fullpath = label_dir+file
    if (os.path.getsize(fullpath)>0 and file != '.directory'):
        item = parseFile(label_dir, file)
        image_record = {}
        image_record['id'] = int(item[0])
        image_record['width'] = width
        image_record['height'] = height
        image_record['file_name'] = item[0]+".png"
        coco_json['images'].append(image_record)
        annotation_record = {}
        annotation_record['id'] = int(item[0])
        annotation_record['iscrowd'] = 0
        annotation_record['category_id'] = forkliftID if item[1] == 'forklift' else palletID
        annotation_record['image_id'] = annotation_record['id']
        annotation_record['bbox'] = item[2]
        coco_json['annotations'].append(annotation_record)


# %%
category = {}
category['supercategory'] = 'forklift'
category['id'] = forkliftID
category['name'] = 'forklift'
coco_json['categories'].append(category)
category = {}
category['supercategory'] = 'pallet'
category['id'] = palletID
category['name'] = 'pallet'
coco_json['categories'].append(category)


# %%
with open('/home/marvin/coco.json', 'w') as fp:
    json.dump(coco_json, fp)


# %%



