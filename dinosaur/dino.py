import numpy as np
from random import randint
from time import time
import cv2
from PIL import Image
import keyboard

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

while run:
    if keyboard.is_pressed("w"):
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
            if i==dino:
                print("GAME OVER!!!")
                run=False
        #img=Image.fromarray(data)
        #img.save(f'{ii}.png')
        ii+=1
        data=cv2.cvtColor(data,cv2.COLOR_BGR2RGB)
        cv2.imshow("Game",data)
        cv2.waitKey(1)
        lastFrame=time()