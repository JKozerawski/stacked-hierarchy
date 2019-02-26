import os
import shutil
from glob import glob
import scipy.io as sio

def load_meta():
	meta_file = "/media/jedrzej/Seagate/DATA/ILSVRC2012/ILSVRC2012_devkit_t12/data/meta.mat"
	data = sio.loadmat(meta_file)
	print len(data)
	synsets = data['synsets']
	print len(synsets)
	for i in xrange(1000):
		
'''
val_dir = "/media/jedrzej/Seagate/DATA/ILSVRC2012/VALIDATION/"

val_labels_file = "/media/jedrzej/Seagate/DATA/ILSVRC2012/ILSVRC2012_devkit_t12/data/ILSVRC2012_validation_ground_truth.txt"
with open(val_labels_file, 'r') as f:
	val_labels = f.readlines()
print min(val_labels), max(val_labels)
print len(val_labels)

for i in xrange(50000):
	label = int(val_labels[i])
	directory = val_dir+str(label)
	image = "ILSVRC2012_val_"+str(i+1).zfill(8)+".JPEG"
	if not os.path.exists(directory):
		os.makedirs(directory)
	if os.path.isfile(val_dir+image):
		shutil.move(val_dir+image, directory+"/"+image)
	else:
		print "File not found", i
	if(i%100==0):
		print i

#for img in glob(val_dir+"*"):
	#print img
	#os.rename(img, val_dir+img[-28:])
	

for i in xrange(1000):
	images = glob(val_dir+str(i+1)+"/*")
	#print val_dir+str(i+1)+"/*"
	print len(images)
	for img in images:
		end_img_name = img.split("/")[-1]
		print end_img_name#shutil.move(val_dir+image, directory+image)
'''
load_meta()
