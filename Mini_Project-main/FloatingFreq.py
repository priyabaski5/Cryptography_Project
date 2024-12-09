import numpy as np
import matplotlib.pyplot as plt
def RFF(color,encrypt):
    Lo=[]
    Le=[]
    k=0
    while(k<256):
        tco=0
        tce=0
        for i in range(len(color)):
            for j in range(len(color[0])):
                if(color[i][j]==k):
                    tco+=1
                if(encrypt[i][j]==k):
                    tce+=1
        Lo.append(tco)
        Le.append(tce)
        k+=1
    x=[]
    for i in range(256):
        x.append(i)
    x=np.array(x)
    y_o=np.array(Lo)
    y_e=np.array(Le)
    plt.title("Original Image RFF")
    plt.plot(x,y_o,color="red")
    plt.show()
    
    plt.title("Encrypted Image RFF")
    plt.plot(x,y_e,color="blue")
    plt.show()
        
        