import socket
import numpy as np
from random import randint
from time import time
import cv2
import keyboard
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras import Model
import numpy as np
import socket
import pickle
import cv2

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

model=load_model("autoencoder2.h5")
decoder=tf.keras.models.Sequential(model.layers[9:])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        if keyboard.is_pressed("w"):
            s.sendall(b"w")
        else:
            s.sendall(b"s")
        data=s.recv(512*800)
        data=np.fromstring(data,dtype=np.float32)
        data=data.reshape(1,10,20,512)
        data=decoder.predict(data)
        data=data.reshape(40,80,3)
        cv2.imshow("Result",data)
        cv2.waitKey(60)
