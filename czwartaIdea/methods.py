'''
Created on 04-11-2015

@author: tomek
'''
import numpy as np
import cv2
#import video
from methods import *
import Tkinter as tk
from Xlib import display
#from menu import *
from numpy import sqrt, real, math, double
from cmath import atan, cos, sin
from math import atan2
from EyeTracking import *


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


ramkaWidth = 25
ramkaHeight = 15
gruboscObszaruSterowaniaKursorem = 2;


def czyMoznaWPrawo(px, py, capWidth, capHeight):
    if px < capWidth-ramkaWidth / 2 - 5:
        return True
    return False

def czyMoznaWLewo(px, py, capWidth, capHeight):
    if px > ramkaWidth / 2 + 5:
        return True
    return False

def czyMoznaWGore(px, py, capWidth, capHeight):
    if py > ramkaHeight / 2 + 5:
        return True
    return False

def czyMoznaWDol(px, py, capWidth, capHeight):
    if py < capHeight - ramkaHeight / 2 - 5:
        return True
    return False


def black_field(thresh, (pupilX, pupilY)):
    rozmiar = 10
    cropped_thresh = thresh[pupilY-rozmiar/2:pupilY+rozmiar/2, pupilX-rozmiar/2:pupilX+rozmiar/2]
    #cv2.imshow('kropd', cropped_thresh)
    return 255-cv2.mean(cropped_thresh)[0]

  
def korektaPupil(thresh, (x0,y0), (pupilX, pupilY)):
    #screenHeight, screenWidth = np.shape(thresh)
    margines = gruboscObszaruSterowaniaKursorem #kazdy piksel to inny 'bieg'
    dXmax = ramkaWidth/2.0
    dYmax = ramkaHeight/2.0
    dXmin = dXmax - margines
    dYmin = dYmax - margines
    #jezeli zrenica jest w "obramowaniu" okienka to czytam to jako polecenie ruchu kursorem
    directionPosX = 0
    directionNegX = 0
    directionPosY = 0
    directionNegY = 0
    dX = pupilX-x0
    dY = pupilY-y0
    
    if abs(dX)>dXmin:
        if dX>0:
            #speedPosX = 3
            if dX>dXmin:
                directionPosX = 1
        else:
            #speedNegX = 3
            if dX<-dXmin:
                directionNegX = 1
    if abs(dY)>dYmin:
        if dY>0:
            #speedPosY = 3
            if dY>dYmin:
                directionPosY = 1
        else:
            #speedNegY = 3
            if dY<-dYmin:
                directionNegY = 1

                  
    kierunek = 0 #kierunek 0 brak, 1-gora 2-prawo 3-dol, 4-lewo   
    if directionPosX == 1:
        kierunek = 2
    elif directionNegX == 1:
        kierunek = 4
    elif directionPosY == 1:
        kierunek = 3
    elif directionNegY == 1:
        kierunek = 1
    else: 
        kierunek = 0
    return (pupilX, pupilY, x0, y0, kierunek)

def obliczPozycjeRamki(thresh, (x0,y0), (pupilX, pupilY)):
    dXmax = ramkaWidth/2.0
    dYmax = ramkaHeight/2.0
    #'uciekam okienkiem'
    if abs(pupilX-x0)>dXmax:
        if (pupilX-x0)>0:
            x0 += (pupilX-x0 - (dXmax))
        else:
            x0 += (pupilX-x0 + (dXmax))
    if abs(pupilY-y0)>dYmax:
        if (pupilY-y0)>0:
            y0 += (pupilY-y0 - (dYmax))
        else:
            y0 += (pupilY-y0 + (dYmax))
    return (x0,y0)

def pupil_position_meanshift(thresh, (x0, y0), (pupilX, pupilY), (capWidth, capHeight)):
    obecnie = black_field(thresh, (pupilX, pupilY))
    prawo = black_field(thresh, (pupilX+1, pupilY))
    lewo = black_field(thresh, (pupilX-1, pupilY))
    gora = black_field(thresh, (pupilX, pupilY-1))
    dol = black_field(thresh, (pupilX, pupilY+1))
    
    while (obecnie < max([prawo, lewo, gora, dol])): 
        if prawo > obecnie:
            if not czyMoznaWPrawo(pupilX, pupilY, capWidth, capHeight):
                break
            pupilX+=1
        elif lewo > obecnie:
            if not czyMoznaWLewo(pupilX, pupilY, capWidth, capHeight):
                break
            pupilX-=1
        elif gora > obecnie:
            if not czyMoznaWGore(pupilX, pupilY, capWidth, capHeight):
                break
            pupilY-=1
        elif dol > obecnie:
            if not czyMoznaWDol(pupilX, pupilY, capWidth, capHeight):
                break
            pupilY+=1   
        x0, y0 = obliczPozycjeRamki(thresh, (x0, y0), (pupilX, pupilY))
        obecnie = black_field(thresh, (pupilX, pupilY))
        prawo = black_field(thresh, (pupilX+1, pupilY))
        lewo = black_field(thresh, (pupilX-1, pupilY))
        gora = black_field(thresh, (pupilX, pupilY-1))
        dol = black_field(thresh, (pupilX, pupilY+1)) 
        #if pozaEkranem(pupilX, pupilY, capWidth, capHeight):
        #    break
    
    pupilX, pupilY , x0, y0, kierunek = korektaPupil(thresh, (x0,y0), (pupilX, pupilY))    
    return (pupilX, pupilY, x0, y0, kierunek)




