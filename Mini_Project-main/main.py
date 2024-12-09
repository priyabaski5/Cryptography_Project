import Sender
import Receiver
import copy
import numpy as np
import cv2
import math
import random as r
import matplotlib.pyplot as plt
pic="peppers.png"
imgfile = "/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/peppers.jpg"

key,start,random,encrypted_image,orig_img,red,green,blue,ered,egreen,eblue=Sender.Encryption(pic,imgfile)
img="/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Encrypted_Image/"+pic
cv2.imwrite(img,np.uint8(np.array(encrypted_image)))

cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/"+pic,np.uint8(np.array(orig_img)))
cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/encrypted_"+pic,np.uint8(np.array(encrypted_image)))

decrypted_image=Receiver.Decryption(pic,img,key,random,start)

# Comment on
# Small change in initial value, gives completely different output
# start[0]=start[0]+1
# decrypted_image_diff=Receiver.Decryption("diff_"+pic,img,key,random,start)
plt.hist(np.uint8(np.array(red)).ravel(),256,[0,256],color="red")
plt.ylim(0,2500)
plt.show()
plt.hist(np.uint8(np.array(green)).ravel(),256,[0,256],color="green")
plt.ylim(0,2500)
plt.show()
plt.hist(np.uint8(np.array(blue)).ravel(),256,[0,256],color="blue")
plt.ylim(0,2500)
plt.show()
plt.hist(np.uint8(np.array(ered)).ravel(),256,[0,256],color="red")
plt.ylim(0,2500)
plt.show()
plt.hist(np.uint8(np.array(egreen)).ravel(),256,[0,256],color="green")
plt.ylim(0,2500)
plt.show()
plt.hist(np.uint8(np.array(eblue)).ravel(),256,[0,256],color="blue")
plt.ylim(0,2500)
plt.show()


# Comment off
def correlationCoefficient(X, Y):
    n = X.size
    sum_X = X.sum()
    sum_Y = Y.sum()
    sum_XY = (X*Y).sum()
    squareSum_X = (X*X).sum()
    squareSum_Y = (Y*Y).sum()
    corr = (n * sum_XY - sum_X * sum_Y)/(np.sqrt((n * squareSum_X - sum_X * sum_X)* (n * squareSum_Y - sum_Y * sum_Y))) 
    return corr
im1 = np.array(red)/255
im2 = np.array(ered)/255
print ('{0:.6f}'.format(correlationCoefficient(im1, im2))) 
im1 = np.array(green)/255
im2 = np.array(egreen)/255
print ('{0:.6f}'.format(correlationCoefficient(im1, im2))) 
im1 = np.array(blue)/255
im2 = np.array(eblue)/255
print ('{0:.6f}'.format(correlationCoefficient(im1, im2))) 
im1 = np.array(orig_img)/255
im2 = np.array(encrypted_image)/255
print ('{0:.6f}'.format(correlationCoefficient(im1, im2))) 

def NCPR(orig,encrypt):
    num=0
    w=len(orig)
    x=len(orig[0])
    for i in range(w):
        for j in range(x):
            if(orig[i][j]!=encrypt[i][j]):
                num+=1
    return num*100/(w*x)

def UACI(orig,encrypt):
    num=0
    w=len(orig)
    x=len(orig[0])
    for i in range(w):
        for j in range(x):
            num+=(abs(orig[i][j]-encrypt[i][j]))/255
    return num*100/(w*x)
def entropy(img):
    count=[0 for i in range(256)]
    w=len(img)
    h=len(img[0])
    for i in range(len(img)):
        for j in range(len(img[0])):
            count[img[i][j]]=count[img[i][j]]+1
    Hm=0
    for i in range(256):
        pi=count[i]/(w*h)
        if(pi!=0):
            Hm+=pi*math.log(1/pi,2)
    return Hm
print("NCPR of red component: ",NCPR(red,ered))
print("NCPR of green component: ",NCPR(green,egreen))
print("NCPR of blue component: ",NCPR(blue,eblue))
print("UACI of red component: ",UACI(red,ered))
print("UACI of green component: ",UACI(green,egreen))
print("UACI of blue component: ",UACI(blue,eblue))

print("Entropy of red component", entropy(red))
print("Entropy of green component", entropy(green))
print("Entropy of blue component", entropy(blue))
print("Entropy of Encrypted red component", entropy(ered))
print("Entropy of Encrypted green component", entropy(egreen))
print("Entropy of Encrypted blue component", entropy(eblue))

#adding noise:   
def add_salt_and_pepper_noise(image, noise_ratio = 0.2):
    noisy_image = copy.deepcopy(original_image.tolist())
    h=300
    w=300
    noisy_pixels = int(h * w * noise_ratio)
 
    for _ in range(noisy_pixels):
        row, col = r.randint(0, h-1), r.randint(0, w-1)
        if r.random() <= 0.5:
            noisy_image[row][col] = [0, 0, 0] 
        else:
            noisy_image[row][col] = [255, 255, 255]
 
    return noisy_image
 
original_image = cv2.imread("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/encrypted_"+pic)
 
if original_image is None:
    raise Exception("Image not loaded properly. Check the file path.")
 
noisy_image = add_salt_and_pepper_noise(original_image)
 
cv2.imshow("Original Image", np.uint8(np.array(original_image)))
cv2.imshow("Noisy Image (Salt and Pepper)", np.uint8(np.array(noisy_image)))
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/noisy_"+pic,np.uint8(np.array(noisy_image)))
decrypted_image=Receiver.Decryption(pic,"/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/noisy_"+pic,key,random,start)
cv2.imwrite("/Users/gnanapriya/Desktop/Work/Mini_Project-main/Images/Noise_Attack/decrypted_noisy_"+pic,np.uint8(np.array(decrypted_image)))
cv2.imshow("Original Image", np.uint8(np.array(original_image)))
cv2.imshow("Noisy Image (Salt and Pepper)", np.uint8(np.array(noisy_image)))
cv2.imshow("Decrypted Image", np.uint8(np.array(decrypted_image)))
cv2.waitKey(0)
cv2.destroyAllWindows()