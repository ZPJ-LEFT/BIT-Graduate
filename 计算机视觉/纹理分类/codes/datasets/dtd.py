##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Created by: Hang Zhang
## ECE Department, Rutgers University
## Email: zhang.hang@rutgers.edu
## Copyright (c) 2017
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree 
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
from PIL import Image
import numpy as np
import torch
import torch.utils.data as data

class DTDDataset(data.Dataset):
    NUM_CLASS = 23
    def __init__(self, root=os.path.expanduser('~/.encoding/data/'),
                 split='train', transform=None, no=1):
        root = os.path.join(root, 'dtd')
        
        self.transform = transform
        classes, class_to_idx = find_classes(os.path.join(root, 'images'))
        if split=='train':
            filename = os.path.join(root, 'labels/train'+str(no)+'.txt')
        elif split=='test':
            filename = os.path.join(root, 'labels/test'+str(no)+'.txt')
        else:
            filename = os.path.join(root, 'labels/val'+str(no)+'.txt')

        self.images, self.labels = make_dataset(filename, root, class_to_idx)
        assert (len(self.images) == len(self.labels))

    def __getitem__(self, index):
        _img = Image.open(self.images[index]).convert('RGB')
        _label = self.labels[index]
        if self.transform is not None:
            _img = self.transform(_img)
        else:
            _img = np.array(_img).transpose(2,0,1)

        return _img, _label

    def __len__(self):
        return len(self.images)

def find_classes(dir):
    classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


def make_dataset(filename, datadir, class_to_idx):
    images = []
    labels = []
    with open(os.path.join(filename), "r") as lines:
        for line in lines:
            _image = os.path.join(datadir, 'images', line.rstrip('\n'))
            _dirname = os.path.split(os.path.dirname(_image))[1]
            assert os.path.isfile(_image)
            label = class_to_idx[_dirname]
            images.append(_image)
            labels.append(label)

    return images, labels

