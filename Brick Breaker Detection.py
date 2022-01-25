#!/usr/bin/env python
# coding: utf-8

# In[14]:


import os
import cv2
import math
import numpy as np
from itertools import islice
from glob import glob
from sklearn.metrics import mean_absolute_error as MAE


# In[15]:


def get_res_from_txt(file):
    f = open(file, "r")
    hits = []
    flag = False
    for line in f.readlines():
        if flag: 
            tokens = line.strip().split(",")
            hits.append(int(tokens[1]))
        flag = True # Preskacemo prvi red txt
    return hits


# In[16]:


def create_dir(path):
    # Pravljenje fajla za cuvanje frejmova
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name {path}")


# In[17]:


def save_frame(video_path, save_dir, gap=1):
    name = video_path.split("/")[-1].split(".")[0]
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)
    cap = cv2.VideoCapture(video_path)
    idx = 0
    while True:
        ret, frame = cap.read()

        if ret == False:
            cap.release()
            break
        # Pravimo frejmove iz snimka po indeksu
        cv2.imwrite(f"{save_path}/{idx}.png", frame)
        idx += 1


# In[18]:


def get_frames():
# Pomocna metoda da pozove seckanje snimka
    video_paths = glob("Videos/*")
    save_dir = "Save"
    for path in video_paths:
        save_frame(path, save_dir, gap=10)


# In[19]:


def lr_edge(frame):
    # Canny edge radimo
    canny_frame = cv2.Canny(frame, 100, 200)
    # Vrednosti za ivice koje ce biti sigurno pretabane
    l = [math.inf, math.inf, math.inf, math.inf]
    r = [-math.inf, -math.inf, -math.inf, -math.inf]
    # Svi parametri koje Hough Lines zahteva
    # HL se koristi da dobijemo linije od ivica
    rres = 1
    thetares = 1*np.pi/180
    threshold = 1
    min_line_length = 1
    max_line_gap = 100
    lines = cv2.HoughLinesP(canny_frame, rres, thetares, threshold, min_line_length,
                            max_line_gap)
    i = 0
    for i in range(len(lines)):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]    
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]  
        # Gledamo x od linija da nadjemo levu i desnu stranu
        # Najmanji x je leva ivica dok je najveci desna ivica
        if x1 == x2: # Da li je vertikalna linija u pitanju?
            if x1 < l[0]: # Sada ovu vert. liniju uzimamo za levu stranu
                l = [x1, y1, x2, y2] 
            if x1 > r[0]: # Sada ovu vert. liniju uzimamo za desnu stranu
                r = [x1, y1, x2, y2]
    return l, r            


# In[20]:


def get_ball_coordinates(frame):
    # Vadimo binarnu sliku sa thresholdom
    xyz, t_image = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    # Vadimo objekte
    fc, vwz = cv2.findContours(t_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    balls = [] # Lista svih loptica sa slike
    for c in fc:
        # X i Y su centar loptice
        (x, y), r = cv2.minEnclosingCircle(c)
        if r < 5 and r > 4: # Gledamo da li je loptica iz liste kontura
            balls.append((x, y)) # Cuvamo koordinate za kasniju proveru udarca
    return balls


# In[21]:


def get_edges():
# Pomocna metoda koja se pozove jednom da inicijalizujemo ivice igre
    i = 1
    l = []
    r = []
    for i in range(11):
        path = r'Save\Videos\video' + str(i) + '\*.png'
        img_names = glob(path)
        for frame in img_names:
            img = cv2.imread(frame, 0)
            l, r = lr_edge(img) # Metoda nam vrati ivice i imamo za dalji rad
            return l, r


# In[22]:


def calculate_hits():
# Za svaki frame iz snimaka koji uzimamo iz foldera,
# gledamo da li je loptica izvucena sa framea u zoni
# pixela ivica. Ako jeste dodajemo hit
    result = {}
    i = 1
    flag = True
    l, r = get_edges()
    for i in range(11):
        hits = 0
        path = r'Save\Videos\video' + str(i) + '\*.png'
        img_names = glob(path)
        for frame in img_names:
            img = cv2.imread(frame, 0)
            balls = get_ball_coordinates(img) # Dobijamo loptice
            # X coordinate ivica za poredjenje
            lx = l[0] 
            rx = r[0]
            for b in balls:
                # Uzimamo x loptice za poredjenje
                bx = b[0]
                # Ako je u zoni manjoj od 20 dodaj hit
                # Flag klazula je dodata zbog bug-a na prvoj iteraciji
                if flag:
                    if bx - lx < 20:
                        hits += 1
                    if rx - bx < 20:
                        hits += 1
                else:
                    if bx - lx < 23:
                        hits += 1
                        # next(islice(balls, 3, 3), None)
                    if rx - bx < 23:
                        hits += 1
                        # next(islice(balls, 3, 3), None)
        if hits != 0:
            flag = False
        #print(hits)
        # U recnik pisemo ime snimka i broj udaraca vezan za snimak
        result['video' + str(i)] = hits 
    return result # Vracamo recnik sa svim snimcima i njihovim udarcima


# In[23]:


if __name__ == "__main__":
    # Init programa i pozivanje metoda
    #get_frames() # Pozivamo metodu secenja snimaka u frejmove
    result = calculate_hits()
    my_result = result.values()
    data = []
    flag = True
    for mr in my_result: # Prebacujemo vrednosti recnika u listu
        if not flag:
            data.append(mr)
        else:
            flag = False
    print(data)
    # Uzmi tacne rezultate
    data_result = get_res_from_txt(r'Videos\res.txt')
    print(data_result)
    # Racunaj Mean Absolute Error
    print('MAE: ', MAE(data_result, data))


# In[ ]:





# In[ ]:





# In[ ]:




