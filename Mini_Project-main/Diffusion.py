from KeyGeneration import xor,dec2bin,bin2dec
def diffuse(color,mask):
    D=[]
    for i in range(len(color)):
        L=[]
        for j in range(len(color[0])):
            L.append(0)
        D.append(L)
    
    k=0
    for i in range(len(color)):
        for j in range(len(color[0])):
            D[i][j]=bin2dec(xor(dec2bin(color[i][j]),dec2bin(mask[k])))
            k+=1
    return D