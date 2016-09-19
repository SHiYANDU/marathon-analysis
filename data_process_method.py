def zeromean(column):
    #center the data at 0 mean
    avg = np.average(column)
    return column-avg

def divbystd(column):
    
    std = np.std(column)
    return column/std


def onehot(data,colInd):
    #one-hot coding to treat categorical data
    option=countdiff(data,colInd)
    numcat=len(countdiff(data,colInd))
    
    res=np.zeros((data.shape[0],data.shape[1]+numcat-1))
    for var in range(0,colInd):
        for x in range(0,data.shape[0]):
            res[x,var]=data[x,var]
    for count in range(0,numcat):
        for x in range(0,data.shape[0]):
            if data[x,colInd]==option.values()[count]:
                res[x,colInd+count]=1
    for var in range(colInd,data.shape[1]):
        for x in range(0,data.shape[0]):
            res[x,var+numcat-1]=data[x,var]
    return res    
def countdiff(X,colInd):
#     store different value of the variable for binary split attempt
    result={}
    for row in range(0,X.shape[0]):
        r=X[row,colInd]
        if r not in result:result[r]=0
    return result