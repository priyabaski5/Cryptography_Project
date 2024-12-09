from KeyGeneration import bin2dec,xor,add,hex2bin,getImageLists,dec2bin
import Scrambler as scramble
import cv2
import numpy as np
import copy
import Diffusion
import random
import hashlib
import math
def Key_Generation_Decryption(n,sha_bin,start,random):
    key=[]
    for i in range(0,256,8):
        key.append(sha_bin[i:i+8])
    #starting position of Queen
    start_rx = start[0]
    start_ry = start[1]
    start_gx = start[2]
    start_gy = start[3]
    start_bx = start[4]
    start_by = start[5]
    
    #Generating random values (Initialisation Vector)
    x0_b = random[0]
    y0_b = random[1]
    z0_b = random[2]
    mu_b = random[3]
    k1_b = random[4]
    k2_b = random[5]
    k3_b = random[6]

    #Updating the initialisation vector values
    rho = (bin2dec(xor(key[0],key[1],key[2],key[3],key[4],key[5],key[6],key[7],key[8])))/(2**12)
    x0 = x0_b + (bin2dec(key[9])/256) - rho
    y0 = y0_b + (bin2dec(key[10])/256) - rho
    phi = (bin2dec(xor(dec2bin(start_rx),dec2bin(start_ry),dec2bin(start_bx),dec2bin(start_by),dec2bin(start_gx),dec2bin(start_gy))))/(2**12)
    z0 = z0_b + (bin2dec(xor(key[11],key[12]))%256)/(2**12) - phi
    mu = mu_b + (bin2dec(xor(key[13],add(key[14],key[15])))%256)/(2**12) - phi
    k1 = k1_b + (bin2dec(add(xor(key[16],key[17]),xor(key[18],key[19]))))/(2**12)
    k2 = k2_b + (bin2dec(add(xor(key[20],key[21]),xor(key[22],key[23]),xor(key[24],key[25]))))/(2**12)
    k3 = k3_b + (bin2dec(add(xor(key[26],key[27]),xor(key[28],key[29]),xor(key[30],key[31]))))/(2**12)

    #Chaotic sequences
    u=[x0]
    v=[y0]
    w=[z0]
    for i in range(1,n*n*3+1):
        u.append((mu*k1*v[i-1]*(1-u[i-1])+w[i-1])%1)
        v.append((mu*k2*v[i-1]+w[i-1]*(1/(1+(u[i]**2))))%1)
        w.append((mu*(u[i]+v[i]+k3)*math.sin(w[i-1]))%1)
    
    #Calculating distance, direction and mask sequences
    dist=[]
    dire=[]
    mask=[]
    for i in range(n*n*3):
        dist.append(int(((((abs(u[i])) - math.floor(abs(u[i])))*(10**14))%(2*n-1))-(n-1)))
        dire.append(int(((((abs(v[i])) - math.floor(abs(v[i])))*(10**14))%4)+1))
        mask.append(int((((abs(w[i]))-math.floor(abs(w[i])))*(10**14))%256))
        
    return dist,dire,mask,[start_rx,start_ry,start_gx,start_gy,start_bx,start_by]

def Decryption(pic,imgfile,sha_key,random,start):
    img,red,green,blue = getImageLists(imgfile)
    n = len(red)
    print(start)
    dist,dire,mask,start_pos=Key_Generation_Decryption(n,sha_key,start,random)

    srx=start_pos[0]
    sry=start_pos[1]
    sgx=start_pos[2]
    sgy=start_pos[3]
    sbx=start_pos[4]
    sby=start_pos[5]

    decrypted_red = Diffusion.diffuse(red,mask[:n*n])
    sr=copy.deepcopy(decrypted_red)
    descrambled_red = scramble.deHPS(dist[:n*n],dire[:n*n],n,srx,sry,sr)

    decrypted_green = Diffusion.diffuse(green,mask[n*n:2*n*n])
    sg=copy.deepcopy(decrypted_green)
    descrambled_green = scramble.deHPS(dist[n*n:2*n*n],dire[n*n:2*n*n],n,sgx,sgy,sg)

    decrypted_blue = Diffusion.diffuse(blue,mask[2*n*n:3*n*n])
    sb=copy.deepcopy(decrypted_blue)
    descrambled_blue = scramble.deHPS(dist[2*n*n:3*n*n],dire[2*n*n:3*n*n],n,sbx,sby,sb)

    decrypted_image = []
    for i in range(n):
        L=[]
        for j in range(n):
            L.append([decrypted_red[i][j],decrypted_green[i][j],decrypted_blue[i][j]])
        decrypted_image.append(L)
            
    descrambled_image = []
    for i in range(n):
        L=[]
        for j in range(n):
            L.append([descrambled_red[i][j],descrambled_green[i][j],descrambled_blue[i][j]])
        descrambled_image.append(L)
        
    
    cv2.imshow("Encrypted Image",np.uint8(np.array(img)))
    cv2.imshow("Decrypted Image",np.uint8(np.array(decrypted_image)))
    cv2.imshow("Descrambled Image",np.uint8(np.array(descrambled_image)))

        
    cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Decrypted_Image/"+pic,np.uint8(np.array(decrypted_image)))
    cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Descrambled_Image/"+pic,np.uint8(np.array(descrambled_image)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return descrambled_image
    