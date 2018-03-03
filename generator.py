# encoding:utf-8

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import *
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool

# マルチプロセスの許可
# pool or full or not が選べる
multiprocess_mode = "pool"

# 作成する画像数
numOfImages=5

# 消失点の表示
showVanishingPoints = True

# https://i.imgur.com/KguoTZ9.jpg
image = Image.open('KguoTZ9.jpg')
image = image.resize((int(image.size[0]/image.size[1]*400), 400))

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

def getCrossPoint(pixel,hoge,huge,to):
    vector_To2Pixel=pixel.minus(to)

    tmpx=huge.x-hoge.x
    tmpy=huge.y-hoge.y
    if((tmpy*vector_To2Pixel.x - tmpx*vector_To2Pixel.y)!=0):
        r=((tmpx*to.y - tmpy*to.x) - (tmpx*hoge.y - tmpy*hoge.x))/(tmpy*vector_To2Pixel.x - tmpx*vector_To2Pixel.y)
    else:
        r=((tmpx*to.y - tmpy*to.x) - (tmpx*hoge.y - tmpy*hoge.x))/(0.00001)
    return to.add(vector_To2Pixel.mul(r)),r


def generate(i):
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

    for x in range(image.size[1]):
        for y in range(image.size[0]):
            pixel=Point(x,y)
            cross1,r1=getCrossPoint(pixel,p1,p4,to)
            cross2,r2=getCrossPoint(pixel,p2,p1,to)
            cross3,r3=getCrossPoint(pixel,p3,p2,to)
            cross4,r4=getCrossPoint(pixel,p4,p3,to)
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
            if(showVanishingPoints):
                mat[int(cross.x)][int(cross.y)]=(255,255,255)
    if(showVanishingPoints): # show vanishing points
        def setcolor(pixel,color):
            for j in [(0,0),(0,1),(1,0),(1,1)]:
                mat[int(pixel.x)+j[0]][int(pixel.y)+j[1]]=color
        # set color RED
        setcolor(fr, (255,0,0))
        # set color BLUE
        setcolor(to, (0,255,255))

    mat2img(mat,i1)
    i1.save(str(i).zfill(3) + ".png")

if multiprocess_mode == "pool":
    # プロセス数の最大値
    pool = Pool(max(1, multiprocessing.cpu_count() - 1))
    pool.map(generate, range(numOfImages))
    pool.close
else:
    for i in range(numOfImages):
        if multiprocess_mode == "full":
            # pool非使用時はこちら
            p = Process(target=generate,args=(i,))
            p.start()
        else:
            # シリアルに実行する
            generate(i)
