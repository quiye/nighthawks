# encoding:utf-8

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import *

class Point:
    def dist(self,target):
        return sqrt((self.x-target.x)**2+(self.y-target.y)**2)
    def minus(self,target):
        return Point(self.x-target.x,self.y-target.y)
    def add(self,target):
        return Point(self.x+target.x,self.y+target.y)
    def mul(self,r):
        return Point(self.x*r,self.y*r)
    def __init__(self, x,y):
        self.x=x
        self.y=y

def img2mat(bf, k):
    px = bf.getdata()
    pxx = list(px)
    ppp = np.array(pxx)
    mat1 = ppp.reshape(bf.size[1], bf.size[0], k)
    return mat1

def mat2img(mat, bf):
    px = bf.getdata()
    pxx = list(px)
    m = mat.shape[0]
    n = mat.shape[1]
    for x in range(0, m):
        for y in range(0, n):
            tmp=mat[x][y]
            pxx[y + n * x] = int(tmp[0]), int(tmp[1]), int(tmp[2])
    bf.putdata(pxx)
    return

# https://i.imgur.com/KguoTZ9.jpg
image = Image.open('KguoTZ9.jpg')
image = image.resize((int(image.size[0]/image.size[1]*400), 400))
numOfImages=50
for i in range(numOfImages):
    i1 = Image.new("RGB", (image.size[0], image.size[1]), (120, 150, 200))

    mat = img2mat(image,3)
    cpymat=img2mat(image,3)
    # mat[10][11]=(255,255,255) # 10は縦軸下方向、11は横軸右方向

    p1=Point(96,270)
    p2=Point(99,68)
    p3=Point(267,67)
    p4=Point(266,269)
    fr = Point(165,127)
    to = Point(165+15*sin(i/numOfImages*2*pi),127+15*cos(i/numOfImages*2*pi))

    def getCrossPoint(pixel,hoge,huge):
        vector_To2Pixel=pixel.minus(to)

        tmpx=huge.x-hoge.x
        tmpy=huge.y-hoge.y
        if((tmpy*vector_To2Pixel.x - tmpx*vector_To2Pixel.y)!=0):
            r=((tmpx*to.y - tmpy*to.x) - (tmpx*hoge.y - tmpy*hoge.x))/(tmpy*vector_To2Pixel.x - tmpx*vector_To2Pixel.y)
        else:
            r=((tmpx*to.y - tmpy*to.x) - (tmpx*hoge.y - tmpy*hoge.x))/(0.00001)
        return to.add(vector_To2Pixel.mul(r)),r

    for x in range(image.size[1]):
        for y in range(image.size[0]):
            pixel=Point(x,y)
            cross1,r1=getCrossPoint(pixel,p1,p4)
            cross2,r2=getCrossPoint(pixel,p2,p1)
            cross3,r3=getCrossPoint(pixel,p3,p2)
            cross4,r4=getCrossPoint(pixel,p4,p3)
            dist=1000000000000000
            crosses=[cross1,cross2,cross3,cross4]
            ratios=[r1,r2,r3,r4]
            for j in range(len(crosses)):
                if to.dist(crosses[j]) < dist and ratios[j]>0:
                    cross=crosses[j]
                    dist=to.dist(crosses[j])
                    r=ratios[j]

            targetPixel=fr.add((cross.minus(fr)).mul(1/r))
            if(r<1):
                try:
                    mat[int(pixel.x)][int(pixel.y)]=cpymat[int(targetPixel.x)%image.size[1]][int(targetPixel.y)%image.size[0]]
                except:
                    print('err')
            # mat[int(cross.x)][int(cross.y)]=(255,255,255)
    if(1): # teach
        mat[p1.x][p1.y]=(255,255,255)
        mat[p2.x][p2.y]=(255,255,255)
        mat[p3.x][p3.y]=(255,255,255)
        mat[p4.x][p4.y]=(255,255,255)
        mat[int(fr.x)][int(fr.y)]=(255,0,0) #red
        mat[int(fr.x+1)][int(fr.y)]=(255,0,0) #red
        mat[int(fr.x)][int(fr.y+1)]=(255,0,0) #red
        mat[int(fr.x+1)][int(fr.y+1)]=(255,0,0) #red
        mat[int(to.x)][int(to.y)]=(0,0,255) #blue
        mat[int(to.x+1)][int(to.y)]=(0,0,255) #blue
        mat[int(to.x)][int(to.y+1)]=(0,0,255) #blue
        mat[int(to.x+1)][int(to.y+1)]=(0,0,255) #blue

    mat2img(mat,i1)
    # i1.show()
    i1.save(str(i).zfill(3) + ".png")
