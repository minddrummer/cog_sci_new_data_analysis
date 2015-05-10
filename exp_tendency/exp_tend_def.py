'''
#to-do-list:
1)get the reported threshold for each category
??5)(Maybe you can also show all of the individual threshold lines for each subject in each of the four categories, too, so we can see how well the mean captures all the individual thresholds....) 
2)get modelB threshold for each category:mean/median
3)get the # of subjects best fitting for each type of model
4)get the # of subjects besting fitting in each of the 4 category for each type of model
6)compare the 4 reported threshold with other fitting modeled threshold, like the constant model?
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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 

data0 = scipy.io.loadmat('IncreaseDecreaseTendency.mat')
data1 = scipy.io.loadmat('InDeConTendency.mat')
subj_id = data1['subjectID']
constant = data0['constant']
increase = data0['increase']
decrease = data0['decrease']

df = np.concatenate((subj_id, constant,increase,decrease), axis = 1)

df = pd.DataFrame(df)
df.columns = ['subj_id', 'constant', 'increase','decrease']
df.set_index('subj_id', inplace =True)

def  match(row):
	if sum(row == 0) ==2:
		return row.loc[row != 0].index[0]
	elif sum(row == 0) == 1:
		intermediate_result =row.loc[row==0].index[0]
		if intermediate_result == 'increase':
			return 'decrease'
		elif intermediate_result == 'decrease':
			return 'increase'
		else:
			print 'welll'
			return 'mix'
	elif sum(row == 0 ) == 0:
		return 'mix'
df.loc[:, 'class'] = df.apply(match, axis = 1)

class_df = df.groupby('class').agg('count')
#class_df.to_csv('class_df.csv', index = True)







