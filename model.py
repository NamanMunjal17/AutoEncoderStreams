import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Input,UpSampling2D
from tensorflow.keras.optimizers import Adam
import cv2
from tensorflow.keras import Model
import pickle
images=pickle.load(open("data.pkl","rb"))
images=[cv2.resize(img,(80,48)) for img in images]
images=[cv2.cvtColor(img,cv2.COLOR_BGR2HSV) for img in images]
images=images[:700]
images=[img/255 for img in images]
images=np.array(images)
images=images.reshape(len(images),48,80,3)
input_img = Input(shape=(48,80, 3))
x = Conv2D(2048, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(1024, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)


en = Conv2D(512, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(1024, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(2048, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(3, (3, 3), activation='softmax', padding='same')(x)
autoenc=Model(input_img,decoded)
autoenc.compile(optimizer=Adam(learning_rate=0.0001),loss='mse')
autoenc.summary()
autoenc.fit(images,images,epochs=200,batch_size=2,verbose=1)
autoenc.save('autoencoder2.h5')