'''
the model is: treat the linear relation between switching/repetition and RT
use all the samples from all the subjects
use linear regression for switchOrNot, just one variable which is categorical
after that, get the residual for each turn of subjects
and redo the analysis of the RT analysis on the previous matlab code to find results
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 
import sklearn.linear_model as lm
import statsmodels.api as sm


pop = scipy.io.loadmat('population.mat')
pop = pop['population']
#parameter setting
num_turn = 20
num_trial = 30
num_subj = pop.shape[0]/(num_turn*num_trial)

##pop is a numpy.array
##col1: id, col2: trial_num, col3:turn_num, col4:ExEx, col5: switchOrNot
##col6: timestamp, col7: RT

#all the first turn of each trial is 1, for switchOrNot, and remove them when doing linear regression 
#since they are not accurate
#should create dummy V? Yes
#NOTE: the exex, switch will both refer to the action of the same turn in 'pop', so is the card value
#it means that at the turn 6,e.g., the action is explore, it is switching/or-not compare to the 5th turn
#and the value you got is 70, and the RT is about 10ms for this exploration/this switching, all the info are written in the same row

#prepare the data

pop = pop[:,0:7]
#remove the every first data-point
#print pop.shape
data = np.delete(pop, range(0,pop.shape[0], 20), axis = 0)
print data.shape

#rt is 6, as y
y = data[:,6].copy()[:,np.newaxis]
x = data[:,4].copy()
#create dummy x
#for switch, 1 means switch
x_switch = x.copy()[:,np.newaxis]
#for not switch, 1 means not switch
x_not_switch = 1 - x[:,np.newaxis]
x_final = np.concatenate((x_not_switch,x_switch), axis = 1)
print x_final.shape

##use sklearn lm to fit the data
# lmfit = lm.LinearRegression(fit_intercept=True, normalize=False, copy_X=True)
# lmfit.fit(x_final, y)
# lmfit.coef_
# lmfit.intercept_
# lmfit.fit(x_switch,y)
# lmfit.coef_
# lmfit.intercept_

##note that: in the switch case, since it is only binary option, so there is no need to create addtional
##dummy variables; otherwise, the model will have multicollinearity, which leads to get very strange coeffient
##and the sklearn package and statsmodel package will generate different coeffients
##this is because the computer cannot solve it accurately because of the matrix is singluar
##use only x_switch to fit the model
# x_final_tmp = sm.add_constant(x_final)
# model0 = sm.OLS(y, x_final_tmp)
# result0 = model0.fit()

## add constant to the linear model
x_switch_tmp = sm.add_constant(x_switch)
model1 = sm.OLS(y, x_switch_tmp)
result1 = model1.fit()
print(result1.summary())

#get the residual of the linear model for the RT
resid = result1.resid

##now, using this resid array to redo the RT analysis



















