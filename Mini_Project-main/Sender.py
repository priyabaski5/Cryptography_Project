from KeyGeneration import bin2dec,xor,add,hex2bin,getImageLists,dec2bin
import Scrambler as scramble
import cv2
import numpy as np
import copy
import Diffusion
import random
import hashlib
import math
def Key_Generation_Encryption(imgfile,n,red,blue,green):
    #SHA256
    with open(imgfile,'rb') as f:
        b=f.read()
        sha_hex_key=hashlib.sha256(b).hexdigest()
    sha_bin=''
    for i in sha_hex_key:
        sha_bin += hex2bin[i]
    
    #generating 32 keys from SHA256
    key=[]
    for i in range(0,256,8):
        key.append(sha_bin[i:i+8])
    
    #Secret Keys: x1,x2,x3,x4,x5,x6,y1,y2,y3,y4,y5,y6
    x=[]
    y=[]
    for i in range(6):
        x.append(random.randint(0,n-1))
        y.append(random.randint(0,n-1))
    
    #starting position of Queen
    start_rx = (red[x[0]][y[0]])%n
    start_ry = (red[x[1]][y[1]])%n
    start_gx = (green[x[2]][y[2]])%n
    start_gy = (green[x[3]][y[3]])%n
    start_bx = (blue[x[4]][y[4]])%n
    start_by = (blue[x[5]][y[5]])%n
    
    #Generating random values (Initialisation Vector)
    x0_b = random.random()
    y0_b = random.random()
    z0_b = random.random()
    mu_b = random.uniform(0,3.999)
    k1_b = random.uniform(33.6,100)
    k2_b = random.uniform(38,100)
    k3_b = random.uniform(35.8,100)
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
        
    return dist,dire,mask,[start_rx,start_ry,start_gx,start_gy,start_bx,start_by],sha_bin,[x0_b,y0_b,z0_b,mu_b,k1_b,k2_b,k3_b]

def Encryption(pic,imgfile):
    img,red,green,blue = getImageLists(imgfile)
    n = len(red)
    dist,dire,mask,start_pos,sha_key,random=Key_Generation_Encryption(imgfile,n,red,green,blue)

    srx=start_pos[0]
    sry=start_pos[1]
    sgx=start_pos[2]
    sgy=start_pos[3]
    sbx=start_pos[4]
    sby=start_pos[5]

    scrambled_red = scramble.HPS(dist[:n*n],dire[:n*n],n,srx,sry,red)
    encrypted_red = Diffusion.diffuse(scrambled_red,mask[:n*n])

    scrambled_green = scramble.HPS(dist[n*n:2*n*n],dire[n*n:2*n*n],n,sgx,sgy,green)
    encrypted_green = Diffusion.diffuse(scrambled_green,mask[n*n:2*n*n])

    scrambled_blue = scramble.HPS(dist[2*n*n:3*n*n],dire[2*n*n:3*n*n],n,sbx,sby,blue)
    encrypted_blue = Diffusion.diffuse(scrambled_blue,mask[2*n*n:3*n*n])

    scrambled_image = []
    for i in range(n):
        L=[]
        for j in range(n):
            L.append([scrambled_red[i][j],scrambled_green[i][j],scrambled_blue[i][j]])
        scrambled_image.append(L)
        
    encrypted_image = []
    for i in range(n):
        L=[]
        for j in range(n):
            L.append([encrypted_red[i][j],encrypted_green[i][j],encrypted_blue[i][j]])
        encrypted_image.append(L)
    
    cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Original_Image/"+pic,img)
    cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Scrambled_Image/"+pic,np.uint8(np.array(scrambled_image))) 
    cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Encrypted_Image/"+pic,np.uint8(np.array(encrypted_image)))

    cv2.imshow("Original Image",img)
    cv2.imshow("Scrambled Image",np.uint8(np.array(scrambled_image)))
    cv2.imshow("Encrypted Image",np.uint8(np.array(encrypted_image)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(random)
    return sha_key,start_pos,random,encrypted_image,img,red,green,blue,encrypted_red,encrypted_green,encrypted_blue