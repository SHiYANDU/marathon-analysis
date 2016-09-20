import numpy as np
import pandas
import matplotlib.pyplot as plt

class logitReg():
    
    def __init__(self,train_set_x,train_set_y,n_in,n_out):
        
        self.train_set_x = train_set_x
        self.train_set_y = train_set_y

        self.W = np.asarray(np.random.uniform(0,1e-3,size = (n_in,n_out)))
        
    def sig(self,x,W):
        return 1.0/(1.0 + np.exp(-np.dot(x,W)))
    
    
    def loss(self,x,y):# calculate loss function
        p_y_given_x = self.sig(x,self.W)
        loss = -np.mean(np.sum(y*np.log(p_y_given_x) + (1-y)*np.log(1-p_y_given_x),axis = 1))
        return loss
    
    def g(self,x,y): # calculate some help functions for later logistic descent gradient
        return np.dot(x.T, self.sig(x,self.W) - y)
    
            
    def train(self,train_set_x,train_set_y,tol):
        #tol = 1e-6   # the convergence condition is tol = 1%
        error = 0.9
        loss = []
        err = []
        alpha = 1e-3
        old_loss = 1e20
        beta = 1e-20
#         import matplotlib.pyplot as plt
        max_loop = 1e5
        n = 0
        while n<max_loop:
            
            n+=1
            grad = self.g(train_set_x,train_set_y)
            self.W -= alpha * grad
            new_loss = self.loss(train_set_x,train_set_y)
            print "new loss", new_loss
            error = (np.abs(new_loss - old_loss)+beta)/(old_loss+beta)
#             print('err',error)
            if new_loss > old_loss:alpha *= 0.8
            err.append(error)
            loss.append(new_loss)
            old_loss = new_loss
        
        plt.plot(loss,'r-') 
        plt.show()  
#         while error>tol:  
#                   
#             grad = self.g(train_set_x,train_set_y)
#             self.W -= alpha * grad
#             new_loss = self.loss(train_set_x,train_set_y)
#             print "new loss", new_loss
#             error = (np.abs(new_loss - old_loss)+beta)/(old_loss+beta)
#             print('err',error)
#             if new_loss > old_loss:alpha *= 0.8
#             err.append(error)
#             loss.append(new_loss)
#             old_loss = new_loss
    def predict(self,test_set_x,test_set_y):
        
        p = np.array(self.sig(test_set_x,self.W))
        ind = [i for i in range(len(p)) if p[i]>0.5]
        result = np.zeros(np.shape(test_set_x)[0])
        testY = list(test_set_y.flat)
        result[ind] = 1
        #a = [[i for i,j in zip(testY,result) if i == j]]
        accuracy = 1.0*len([i for i,j in zip(testY,result) if i == j])/len(result)
        return result,testY,accuracy
        #return self.sig(self.w,inX)
    