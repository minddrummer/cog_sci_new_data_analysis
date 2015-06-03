'''
#to-do-list:
1)plot the reported threshold with the standard error value/error bar
2)fit a linear model to the turn and threshold value, check the significancy of the linear model
'''
# find the tendency for each subj as the following policy:
# If the reported thresholds at those 6 turns remained the same, participants were classified as Constant;
# if the values increased at least once and never decreased, participants were classified as Increasing;
# if the values decreased at least once and never increased, participants were classified as Decreasing; 
# otherwise, they were labeled as Mixed.
# Among 188 participants (3 were excluded due to incomplete questionnaires), 
# 71 participants were Increasing, 
# 47 were Decreasing, 
# 19 were Constant, and 51 were Mixed. 
import pylab
pylab.ion()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 
import statsmodels.api as sm




#reading data section
data0 = scipy.io.loadmat('IncreaseDecreaseTendency.mat')
data1 = scipy.io.loadmat('InDeConTendency.mat')
report_thres = scipy.io.loadmat('summarydatacollect.mat')['summarysrchncollect']
report_thres = report_thres[:, ([0]+range(2,8))]

thres = report_thres[:,1:]
report_mean =  thres.mean(axis = 0)
##use standard error as bar height
error_bar = thres.std(axis = 0, ddof = 1)/np.sqrt(thres.shape[0])
turns = [2, 5, 9, 13, 17, 20]


#`````````ploting
plt.figure(1)
#plt.plot(turns, report_mean,color='g', lw=3.0, ls = '--')
plt.errorbar(turns, report_mean,color='g', lw=3.0, ls = '--', yerr = error_bar)
plt.axis([1,21,0,100])
plt.xlabel('Turns')
plt.ylabel('Card Values')
plt.title('Plot the reported threshold with standard error')
plt.close()

#run a simple linear regression on turns and reported threshold value
#transfer thres to 2 columns
np.array(turns)

for i in np.arange(thres.shape[1]):
	if i == 0:
		data = np.append(thres[:,i][:,np.newaxis],np.array([turns[i]]*thres.shape[0])[:,np.newaxis], axis = 1)
		#break
	else:
		data = np.append(data, np.append(thres[:,i][:,np.newaxis],np.array([turns[i]]*thres.shape[0])[:,np.newaxis], axis = 1), axis = 0)

data = sm.add_constant(data)
y = data[:,1]
X = data[:,[0,2]]
model = sm.OLS(y, X)
result = model.fit()
print result.summary()


#  OLS Regression Results--whether the model is significant or not(the p value)
# --is the result in terms of the coefficient of the x1, not refering to the const--
#
# ==============================================================================
# Dep. Variable:                      y   R-squared:                       0.003
# Model:                            OLS   Adj. R-squared:                  0.003
# Method:                 Least Squares   F-statistic:                     3.834
# Date:                Wed, 03 Jun 2015   Prob (F-statistic):             0.0505
# Time:                        16:37:09   Log-Likelihood:                -4981.2
# No. Observations:                1128   AIC:                             9966.
# Df Residuals:                    1126   BIC:                             9976.
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [95.0% Conf. Int.]
# ------------------------------------------------------------------------------
# const         72.6197      1.194     60.844      0.000        70.278    74.961
# x1             0.1840      0.094      1.958      0.050        -0.000     0.368
# ==============================================================================
# Omnibus:                      424.610   Durbin-Watson:                   1.963
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):             1333.166
# Skew:                          -1.909   Prob(JB):                    3.21e-290
# Kurtosis:                       6.714   Cond. No.                         25.5
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

