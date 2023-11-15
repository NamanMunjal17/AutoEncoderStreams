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

game=[[" "]*8]*4
dino=[1,1] #x y
jump=False
jump_init=time()
obstacle_init=time()
jump_duration=1
obstacles=[]
lastFrame=time()
fps=5
ii=0

run=True

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

model=load_model("autoencoder2.h5")
encoder=tf.keras.models.Sequential(model.layers[:9])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while run:
            key=conn.recv(32).decode("utf-8")
            if key=='w':
                if not jump:
                    jump_init=time()
                    jump=True
                    dino[1]=0
            
            if time()-jump_init>=jump_duration:
                jump=False
                dino[1]=1
            
            if time()-obstacle_init>=randint(3,8):
                obstacles.append([7,1])
                obstacle_init=time()
            else:
                pass


            if time()-lastFrame>=1/fps:
            #last operations
                w,h=160,40
                data=np.zeros((h,w,3),dtype=np.uint8)
                data[dino[1]*20:(dino[1]*20)+20,dino[0]*20:(dino[0]*20)+20]=[255,255,255] #dino width 20 height 20
                for i in obstacles:
                    data[i[1]*20:(i[1]*20)+20,i[0]*20:(i[0]*20)+20]=[0,0,255]
                    i[0]-=1
                #img=Image.fromarray(data)
                #img.save(f'{ii}.png')
                ii+=1
                data=cv2.resize(data,(80,40))
                cv2.imshow("Result",data)
                cv2.waitKey(60)
                data=cv2.cvtColor(data,cv2.COLOR_BGR2HSV)
                data=data/255
                data=encoder.predict(data.reshape(1,40,80,3))
                data=data.tostring()
                conn.sendall(data)
                lastFrame=time()