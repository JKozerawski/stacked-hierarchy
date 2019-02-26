import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

import torch
from torchvision import datasets, models
from torch import nn
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch.optim as optim

imagenet_dir = "/media/jedrzej/Seagate/DATA/ILSVRC2012/"

#-----------------------------------------------------------------------------------------#
def imshow(img):
    img = img / 2 + 0.5  # unnormalize
    plt.imshow(np.transpose(img, (1, 2, 0)))  # convert from Tensor image
#-----------------------------------------------------------------------------------------#
# check if CUDA is available
def is_cuda():
	return torch.cuda.is_available()
#-----------------------------------------------------------------------------------------#
def get_imagenet_data(path):
	# import data
	print "TO DO"
# label mapping
def get_labels(path):
	print "TO DO"
#-----------------------------------------------------------------------------------------#
# label mapping
def get_labels(path):
	print "TO DO"
#-----------------------------------------------------------------------------------------#
# Define the network
'''
# Load the pretrained model from pytorch
model = models.inception_v3(pretrained=True)
# print out the model structure
print(model)

# if GPU is available, move the model to GPU
if is_cuda():
    model.cuda()
'''
with open("./classes.txt", 'r') as f:
	classes = f.readlines()
with open("./synsets.txt", 'r') as f:
	synsets = f.readlines()

classes = [c[:-1] for c in classes]
synsets_idx = [i.split()[0] for i in synsets]
synsets_names = [i.split()[1:] for i in synsets]

#synsets_idx = synsets_idx[1:]
#synsets_names = synsets_names[1:]

def map_prediction_to_id(prediction):
	name = synsets_idx[prediction]
	return classes.index(name)

def get_validation_data(main_dir):
	val_dir = main_dir+"VALIDATION/"
	val_labels_file = main_dir+"ILSVRC2012_devkit_t12/data/ILSVRC2012_validation_ground_truth.txt"
	with open(val_labels_file, 'r') as f:
		val_labels = f.readlines()
	assert len(val_labels)==50000

	batch_size = 1
	normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])

	data = datasets.ImageFolder(val_dir, transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ]))
	val_loader = torch.utils.data.DataLoader(
        data,
        batch_size=batch_size, shuffle=False,
		num_workers=1, pin_memory=False)
	#	print data.class_to_idx
	for key, value in data.class_to_idx.iteritems():
		if(value == 1):
			print key,value
		if(key == '1'):
			print key,value
	return val_loader, val_labels, data.classes

def test_on_validation(dataloader, model, ground_truth, mapping):
	count = 0
	correct = 0
	if is_cuda():
		model.cuda()
	for data, target in dataloader:
		#print data
		#print target
		if(is_cuda()):
			data = data.cuda()
		prediction = model(data)
		prediction = prediction.data.cpu().numpy()
		prediction = np.argmax(prediction)

		mapped = int(mapping[target.data.cpu().numpy()[0]]) 
		label = map_prediction_to_id(mapped)

		if(prediction==label):
			correct+=1

		count+=1
		if(count%100==0): print count, correct/float(count)
	print count, count/50000.

model = models.vgg16(pretrained=True)
val_loader, val_labels, mapping = get_validation_data(imagenet_dir)
test_on_validation(val_loader, model, val_labels, mapping)

