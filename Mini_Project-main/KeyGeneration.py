import random
import hashlib
import cv2
import math
#saving appropriate binary values as dictionary
hex2bin={
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'a':'1010',
    'b':'1011',
    'c':'1100',
    'd':'1101',
    'e':'1110',
    'f':'1111'
}

def getImageLists(imgfile):
    #reading the image file
    img=cv2.imread(imgfile)
    
    #resize to (300,300)
    img=cv2.resize(img,(300,300))
    
    #converting the image to 3D list
    img_list=img.tolist()
    
    #splitting up the red, green, blue components
    red=[]
    green=[]
    blue=[]
    for i in img_list:
        l1=[]
        l2=[]
        l3=[]
        for j in i:
            l1.append(j[0])
            l2.append(j[1])
            l3.append(j[2])
        red.append(l1)
        green.append(l2)
        blue.append(l3)
    
    #return the components of image
    return img,red,green,blue

def xor(*args):
    m=len(args[0])
    for i in args:
        s=len(i)
        if(s>m):
            m=s
    L=[]
    for i in args:
        if(len(i)<m):
            L.append('0'*(m-len(i))+i)
        else:
            L.append(i)
    s=''
    for i in range(m-1,-1,-1):
        c=0
        for j in L:
            if(j[i]=='1'):
                c+=1
        s=('0' if(c%2==0) else '1')+s
    return s

def add(*args):
    m=len(args[0])
    for i in args:
        s=len(i)
        if(s>m):
            m=s
    L=[]
    for i in args:
        if(len(i)<m):
            L.append('0'*(m-len(i))+i)
        else:
            L.append(i)
    s=''
    carry=0
    for i in range(m-1,-1,-1):
        c=carry
        for j in L:
            if(j[i]=='1'):
                c+=1
        if(c==0):
            s='0'+s
            carry=0
        elif(c==1):
            s='1'+s
            carry=0
        elif(c==2):
            s='0'+s
            carry=1
        elif(c==3):
            s='1'+s
            carry=1
        elif(c==4):
            s='0'+s
            carry=2
        elif(c==5):
            s='1'+s
            carry=2
        elif(c==6):
            s='0'+s
            carry=3
        elif(c==7):
            s='1'+s
            carry=3
        elif(c==8):
            s='0'+s
            carry=4
    if(carry==1):
        s='1'+s
    return s

def dec2bin(d):
    b = bin(d)[2:]
    l = len(b)
    if(l<8):
        b = '0'*(8-l) + b
    return b

def bin2dec(b):
    i=0
    d=0
    for bit in b[::-1]:
        d += (2**i)*int(bit)
        i+=1
    return d