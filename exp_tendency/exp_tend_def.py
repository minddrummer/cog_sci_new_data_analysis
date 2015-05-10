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
import pylab
pylab.ion()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 

#reading data section
data0 = scipy.io.loadmat('IncreaseDecreaseTendency.mat')
data1 = scipy.io.loadmat('InDeConTendency.mat')
report_thres = scipy.io.loadmat('summarydatacollect.mat')['summarysrchncollect']
report_thres = report_thres[:, ([0]+range(2,8))]



##assigning variables:
subj_id = data1['subjectID']
constant = data0['constant']
increase = data0['increase']
decrease = data0['decrease']




##decide which class for each subj is in for the reported threshold
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
			print 'well, it has both increase and decrease, so it is a mix'
			return 'mix'
	elif sum(row == 0 ) == 0:
		return 'mix'


#classifying each subj into the four reported threshold classes
df = np.concatenate((subj_id, constant,increase,decrease), axis = 1)
df = pd.DataFrame(df)
df.columns = ['subj_id', 'constant', 'increase','decrease']
df.set_index('subj_id', inplace =True)
df.loc[:, 'class'] = df.apply(match, axis = 1)
#class_df = df.groupby('class').agg('count')
#class_df.to_csv('class_df.csv', index = True)


##combine with the reported threshold of each subj,
report_thres = pd.DataFrame(report_thres)
report_thres.columns = ['subj_id','repo_thres1','repo_thres2','repo_thres3','repo_thres4','repo_thres5','repo_thres6']
report_thres.set_index('subj_id', inplace = True)
df = pd.concat([df, report_thres],axis = 1)

##1)get the reported threshold for each category
df_class = df.loc[:,['class','repo_thres1','repo_thres2','repo_thres3','repo_thres4','repo_thres5','repo_thres6']].groupby('class').apply(np.mean).reset_index(inplace=False)
df_class = pd.melt(df_class, id_vars=['class'], value_vars=['repo_thres1','repo_thres2','repo_thres3','repo_thres4','repo_thres5','repo_thres6']).pivot(index = 'variable', columns = 'class',values='value')
df_class.index.name = 'thres'
df_class.columns.name = None
df_class.loc[:,'turns'] = [2, 5, 9, 13, 17, 20]
df_class.plot(x ='turns', y =['constant','increase','decrease','mix'])
plt.ylabel('Card Values')
plt.xlabel('Turn')
plt.axis([1,20,0,100])
plt.title('Reported thresholds for each of 4 groups')



##??5)(Maybe you can also show all of the individual threshold lines for each subject in each of the four categories, too, so we can see how well the mean captures all the individual thresholds....) 

