def HPS_verti(dist,x,y,n):
    if(dist>0):               #Upwards movement
        if(y+dist<=n):        #Checking within chessboard
            y1=y+dist
        else:
            y1=y+dist-n
    elif(dist<0):             #Downwards movement
        if(y+dist>=1):        #Checking within chessboard
            y1=y+dist
        else:
            y1=y+dist+n
    else:
        y1=y
    return x,y1

def HPS_hori(dist,x,y,n):
    if(dist>0):               #move Left
        if(x-dist>=1):        #Checking within chessboard
            x1=x-dist
        else:
            x1=x-dist+n
    elif(dist<0):             #move Right
        if(x-dist<=n):        #Checking within chessboard
            x1=x-dist
        else:
            x1=x-dist-n
    else:
        x1=x
    return x1,y

def HPS_diago(dist,x,y,n):
    if(dist>0):
        if(x<=y):
            lpd = n - y + x
            realdist = dist%lpd
            if(x-realdist >=1):
                x1=x-realdist
                y1=y-realdist
            else:
                x1=x+lpd-realdist
                y1=y+lpd-realdist
        else:
            lpd=n - x + y
            realdist = dist%lpd
            if(y-realdist >=1):
                x1=x-realdist
                y1=y-realdist
            else:
                x1=x+lpd-realdist
                y1=y+lpd-realdist
    elif(dist<0):
        if(x<=y):
            lpd = n - y + x
            realdist = (-dist)%lpd
            if(y+realdist <=n):
                x1=x+realdist
                y1=y+realdist
            else:
                x1=x-lpd+realdist
                y1=y-lpd+realdist
        else:
            lpd=n - x + y
            realdist = (-dist)%lpd
            if(x+realdist <=n):
                x1=x+realdist
                y1=y+realdist
            else:
                x1=x-lpd+realdist
                y1=y-lpd+realdist
    else:
        x1=x
        y1=y
    return x1,y1

def HPS_adiago(dist,x,y,n):
    if(dist>0):
        if(x+y <= n+1):
            lpd = x + y - 1
            realdist = dist%lpd
            if(x-realdist >=1):
                x1=x-realdist
                y1=y+realdist
            else:
                x1=x+lpd-realdist
                y1=y-lpd+realdist
        else:
            lpd = (2*n) - x - y + 1
            realdist = dist%lpd
            if(y+realdist <= n):
                x1=x-realdist
                y1=y+realdist
            else:
                x1=x+lpd-realdist
                y1=y-lpd+realdist
    elif(dist<0):
        if(x+y <= n+1):
            lpd = x + y - 1
            realdist = (-dist)%lpd
            if(y-realdist >= 1):
                x1=x+realdist
                y1=y-realdist
            else:
                x1=x-lpd+realdist
                y1=y+lpd-realdist
        else:
            lpd = (2*n) - x - y + 1
            realdist = (-dist)%lpd
            if(x+realdist <=n):
                x1=x+realdist
                y1=y-realdist
            else:
                x1=x-lpd+realdist
                y1=y+lpd-realdist
    else:
        x1=x
        y1=y
    return x1,y1

def HPS(dist,dire,n,x,y,p):
    dim1 = []
    D=[]
    for i in range(n):
        L=[]
        for j in range(n):
            L.append(-1)
            dim1.append(p[i][j])
        D.append(L)

    k=0
    unscr_pix=[]
    while(k<(n**2)):
        if(dire[k]==1):
            x1,y1=HPS_diago(dist[k],x,y,n)
        elif(dire[k]==2):
            x1,y1=HPS_adiago(dist[k],x,y,n)
        elif(dire[k]==3):
            x1,y1=HPS_hori(dist[k],x,y,n)
        elif(dire[k]==4):
            x1,y1=HPS_verti(dist[k],x,y,n)
        if(D[x1-1][y1-1]==-1):
            D[x1-1][y1-1]=dim1[k]
            x=x1
            y=y1
        else:
            unscr_pix.append(dim1[k])
        k=k+1
    k=0
    for i in range(n):
        for j in range(n):
            if(D[i][j]==-1):
                D[i][j]=unscr_pix[k]
                k=k+1
    return D

def deHPS(dist,dire,n,x,y,p):
    c=p
    D=[]
    k=0
    while(k<(n**2)):
        if(dire[k]==1):
            x1,y1=HPS_diago(dist[k],x,y,n)
        elif(dire[k]==2):
            x1,y1=HPS_adiago(dist[k],x,y,n)
        elif(dire[k]==3):
            x1,y1=HPS_hori(dist[k],x,y,n)
        elif(dire[k]==4):
            x1,y1=HPS_verti(dist[k],x,y,n)
        if(c[x1-1][y1-1]!=-1):
            D.append(c[x1-1][y1-1])
            c[x1-1][y1-1]=-1
            x=x1
            y=y1
        else:
            D.append(-1)
        k=k+1
    for i in range(n):
        for j in range(n):
            if(c[i][j]!=-1):
                if(-1 in D):
                    index=D.index(-1)
                else:
                    index=len(D)
                D=D[:index]+[c[i][j]]+D[index+1:]
    new_D=[]
    for i in range(0,n*n,n):
        new_D.append(D[i:(i+n)])
    return new_D