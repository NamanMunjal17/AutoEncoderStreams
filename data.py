import pickle
import cv2
import os

path="D:/Programs/autoencstream/dinosaur/"

images=[]

for image in os.listdir(path):
    if image[-2:]=="py":
        print("leaving out:",image)
    else:   
	    img=cv2.imread(path+image)
	    images.append(img)

pickle.dump(images,open("data.pkl","wb"))