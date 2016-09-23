import numpy as np
import pandas
import matplotlib.pyplot as plt
import math
import data_process_method
class logitReg():
    
    def __init__(self,train_set_x,train_set_y,n_in):
        #n_in=number of features
        
        self.train_set_x = train_set_x
        self.train_set_y = train_set_y

        self.W = np.asarray(np.random.uniform(0,1e-3,size = (n_in,1)))
        
    def sig(self,x,W):
        
        return 1.0/(1.0 + np.exp(-np.dot(x,W)))
    
    
    def loss(self,x,y):# calculate loss function
        p_y_given_x = self.sig(x,self.W)
        
        loss = -np.mean(np.sum(self.loss_helper(y,p_y_given_x)))
        return loss
    
    def loss_helper(self,y,p_y):
        
        sum=[]
        for ys in y:
            if ys==1:
                sum.append(map(self.log_sum_zero,p_y))
            else:
                sum.append(map(self.log_sum_zero,-p_y))
        sum=np.asarray(sum)
        print y.shape
        print sum.shape
        return y.T.dot(sum)
    
    def log_sum_zero(self,p):
        #a helper function for loss_helper to calculate -log(exp(a)+exp(b) where a is 0 in logistic reg
        return -math.log(math.exp(0)+math.exp(p))
        
        
    def g(self,x,y): # calculate some help functions for later logistic descent gradient
        
        return np.dot(x.T, (self.sig(x,self.W).T - y).T)
    
            
    def train(self,train_set_x,train_set_y,tol):
        #tol = 1e-6   # the convergence condition is tol = 1%
        error = 0.9
        loss = []
        err = []
        alpha = 1e-5
        old_loss = 1e20
        beta = 1e-20
#         import matplotlib.pyplot as plt
        max_loop = 3000
        n = 0
        while n<max_loop:
            
            n+=1
            grad = self.g(train_set_x,train_set_y)
            self.W -= alpha * grad
            print self.W
            alpha*=0.99

#         
#         plt.plot(loss,'r-') 
#         plt.show()  
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
    