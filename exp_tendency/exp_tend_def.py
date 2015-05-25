'''
#to-do-list:
1)get the reported threshold for each category
5)(Maybe you can also show all of the individual threshold lines for each subject in each of the four categories, too, so we can see how well the mean captures all the individual thresholds....) 
2)get modelB threshold for each category:mean/median
3)get the # of subjects best fitting for each type of model
4)get the # of subjects besting fitting in each of the 4 category for each type of model
6)compare the 4 reported threshold with other fitting modeled threshold:try jumpturn model
7)taking out jumpturn7 model, and add the name of the epsilon-greedy and successive_non_candidate model name into the table
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
modelb = pd.DataFrame(scipy.io.loadmat('Parameter7_ModelB_ModelingResult_Bounded_191Subjects.mat')['data'])
modelb.columns = ['subj_id', 'LL_total', 'thres1','thres2','thres3','thres4','thres5','thres6','scaling']
#transfer to BIC value, modelB has 7 paras
modelb.loc[:, 'modelB'] = modelb.loc[:,'LL_total'] + np.log(570)*7
epi_greedy = pd.DataFrame(scipy.io.loadmat('epsilon_greedy_model_results.mat')['LL_total'], columns = ['epi_greedy'])
#epi_greedy has 1 para
epi_greedy = epi_greedy + np.log(570)*1
fix = pd.DataFrame(scipy.io.loadmat('fixed_thresh_model_results.mat')['LL_Total'], columns = ['fix'])
#fix has 2 paras
fix = fix + np.log(570)*2
jump_7 = pd.DataFrame(scipy.io.loadmat('jumpturn_7_two_thres_model_bounded_fitting_result.mat')['minLL'], columns = ['jump_7'])
#jump_7 has 3 paras
jump_7 = jump_7 + np.log(570)*3
jump = pd.DataFrame(scipy.io.loadmat('jumpturn_two_thres_model_bounded_fitting_result.mat')['minLL'], columns = ['jump'])
#jump has 4 paras
jump = jump + np.log(570)*4
##add parameter estimating values for the jumpturn model
best_thresh1 = pd.DataFrame(scipy.io.loadmat('jumpturn_two_thres_model_bounded_fitting_result.mat')['best_thresh1'], columns = ['jump_best_thresh1'])
best_thresh2 = pd.DataFrame(scipy.io.loadmat('jumpturn_two_thres_model_bounded_fitting_result.mat')['best_thresh2'], columns = ['jump_best_thresh2'])
best_scale = pd.DataFrame(scipy.io.loadmat('jumpturn_two_thres_model_bounded_fitting_result.mat')['best_scale'], columns = ['jump_best_scale'])
best_jumpturn = pd.DataFrame(scipy.io.loadmat('jumpturn_two_thres_model_bounded_fitting_result.mat')['best_jumpturn'], columns = ['jump_best_jumpturn'])
jumpturn_modeling_res  = pd.concat((jump, best_thresh1, best_thresh2, best_scale, best_jumpturn), axis = 1)
jump = jumpturn_modeling_res

k_step = pd.DataFrame(scipy.io.loadmat('k_step_model_results.mat')['minLL'], columns = ['k_step'])
#k_step has 2 paras
k_step = k_step + np.log(570)*2
random_k = pd.DataFrame(scipy.io.loadmat('random_k_step_model_results.mat')['LL_total'], columns = ['random_k'])
#random_k has 1 para
random_k = random_k + np.log(570)*1
secretary = pd.DataFrame(scipy.io.loadmat('secretary_search_model_results.mat')['minLL'], columns = ['secretary'])
#secretary has 2 paras
secretary = secretary + np.log(570)*2
successive = pd.DataFrame(scipy.io.loadmat('successive_non_candidate_count_model_results.mat')['minLL'], columns = ['successive'])
#successive has 2 paras
successive = successive + np.log(570)*2

#concatenate all the model results into one df named 'model'
model = pd.concat([modelb, epi_greedy,fix,jump_7,jump,k_step,random_k,secretary,successive],axis=1)


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

##5)(Maybe you can also show all of the individual threshold lines for each subject in each of the four categories, too, so we can see how well the mean captures all the individual thresholds....) 
df_thres_groupby = df.loc[:,['class','repo_thres1','repo_thres2','repo_thres3','repo_thres4','repo_thres5','repo_thres6']].groupby('class')
type_lst = ['constant','increase','decrease','mix']

for class_name in type_lst:
	#class_name = 'constant'
	tempt_df = pd.melt(df_thres_groupby.get_group(class_name).reset_index(inplace=False), id_vars = 'subj_id',\
	value_vars=['repo_thres1','repo_thres2','repo_thres3','repo_thres4','repo_thres5','repo_thres6']).\
	pivot(index = 'variable', columns = 'subj_id',values='value')
	tempt_df.loc[:,'turns'] = [2, 5, 9, 13, 17, 20]
	ax = tempt_df.plot(x='turns', y = tempt_df.columns[0:-1], legend = False)
	title = 'Plot the mean of reported threshold for ' + class_name + ' group and also the invididual thresholds'
	df_class.plot(x ='turns', y =class_name, ax = ax, title = title,xlim=[1,20],ylim=[0,100],  ls='-', lw =4.0, marker = 'o', color='k',legend = False)
	# L=plt.legend()
	# L.get_texts()[0].set_text(None)
plt.close()
plt.close()
plt.close()
plt.close()
plt.close()
plt.close()


##2)get modelB threshold for each category:mean/median

#combine df and model
df.reset_index(inplace =True)
final = pd.merge(df,model, on = 'subj_id', how = 'left')

final_modelb = final.loc[:,['class', u'thres1', u'thres2', u'thres3', u'thres4', u'thres5', u'thres6']].copy()
final_modelb_groupby = pd.melt(final_modelb.groupby('class').apply(np.mean).reset_index(inplace=False),\
 id_vars=['class'], value_vars=['thres1','thres2','thres3','thres4','thres5','thres6']).\
pivot(index = 'variable', columns = 'class',values='value')
final_modelb_groupby.index.name = 'Threshold'
final_modelb_groupby.columns.name = None
final_modelb_groupby.loc[:,'turns'] = [2, 5, 9, 13, 17, 20]
	
##plot on each figure the thresold of ModelB and reported
for class_name in type_lst:
	title = 'Comparison of Reported and Model B for the ' + class_name.upper() + ' group'
	ax = df_class.plot('turns', class_name, ls ='-.', lw=3.0)
	final_modelb_groupby.plot('turns', class_name, ax = ax, xlim = [1,20], ylim=[0,100], ls='-', lw = 3.0,title = title)
	L=plt.legend()
	L.get_texts()[0].set_text('Reported')
	L.get_texts()[1].set_text('Model B')
plt.close()
plt.close()
plt.close()
plt.close()



##3)get the # of subjects best fitting for each type of model
final_model = final.loc[:,['subj_id', 'modelB', \
u'epi_greedy', u'fix', u'jump_7', u'jump', u'k_step', u'random_k', u'secretary', u'successive']].copy()
final_model.set_index('subj_id', inplace = True)
final_model.loc[:,'best_model'] = final_model.apply(np.argmin, axis = 1)
final_model.loc[:,'best_BIC'] = final_model.apply(np.min, axis = 1)
print final_model.loc[:,'best_model'].value_counts()
final_model.loc[:,'best_model'].value_counts().to_csv('total_best_model_each_subj.csv')

##4)get the # of subjects besting fitting in each of the 4 category for each type of model
###----the difference between final_model and final_model_class is that the later has 'class' for grouping and analyzing on each group level
final_model_class = final.loc[:,['subj_id', 'class', 'modelB', \
u'epi_greedy', u'fix', u'jump_7', u'jump', u'k_step', u'random_k', u'secretary', u'successive']].copy()
final_model_class.set_index('subj_id', inplace = True)
final_model_class_gp = dict(list(final_model_class.groupby('class')))

for each_class in final_model_class_gp:
	print each_class.upper()
	print final_model_class_gp[each_class].set_index('class',inplace=False).apply(np.argmin, axis=1).value_counts()
	file_name = each_class+'.csv'
	final_model_class_gp[each_class].set_index('class',inplace=False).apply(np.argmin, axis=1).value_counts().to_csv(file_name,index=True)



#^^^^^^^6)compare the 4 reported threshold with other fitting modeled threshold:try jumpturn model

final_jump = final.loc[:,['class', 'jump_best_thresh1', 'jump_best_thresh2', 'jump_best_scale', 'jump_best_jumpturn']].copy()
final_jump_groupby = pd.melt(final_jump.groupby('class').apply(np.mean).reset_index(inplace=False),\
 id_vars=['class'], value_vars=['jump_best_thresh1','jump_best_thresh2','jump_best_scale']).\
pivot(index = 'variable', columns = 'class',values='value')
final_jump_groupby.columns.name = None
final_jump_groupby_median = pd.melt(final_jump.groupby('class').agg(np.median).reset_index(inplace=False),\
 id_vars=['class'], value_vars=['jump_best_jumpturn']).\
pivot(index = 'variable', columns = 'class',values='value')
final_jump_groupby_median.columns.name = None
final_jump_groupby = pd.concat((final_jump_groupby, final_jump_groupby_median),axis = 0)
	
##plot on each figure the thresold of ModelB and reported
for class_name in type_lst:
	title = 'Comparison of Reported and JumpTurn Model for the ' + class_name.upper() + ' group'
	#first plot the reported threshold
	#open a new figure every time for the same class: it will add all the information into the same graph
	plt.figure()
	reported_thres, = plt.plot(df_class.loc[:,'turns'], df_class.loc[:, class_name], ls ='-.', lw=3.0, color = 'b', label = 'Reported Threshold')
	#second plot the modeling result
	tmp_turns0 = range(2, int(final_jump_groupby.loc['jump_best_jumpturn', class_name]+1))
	tmp_thres0 = final_jump_groupby.loc['jump_best_thresh1', class_name]
	line_jumpturn, = plt.plot(tmp_turns0, len(tmp_turns0)*[tmp_thres0], color = 'g', ls='-', lw = 3.0, label = 'JumpTurn Model')
	plt.legend(handles = [reported_thres, line_jumpturn])
	tmp_turns = range(int(final_jump_groupby.loc['jump_best_jumpturn', class_name]+1), 21)
	tmp_thres = final_jump_groupby.loc['jump_best_thresh2', class_name]
	plt.plot(tmp_turns, len(tmp_turns)*[tmp_thres], color = 'g', ls='-', lw = 3.0)
	#add connecting line to jumpturn_thres1 and jumpturn_thres2
	plt.plot([tmp_turns0[-1], tmp_turns[0]],[tmp_thres0, tmp_thres], color='g', ls = '--', lw =3.0)
	plt.axis([1,20, 0,100])
	plt.title(title)
	plt.xlabel('Turn')
	plt.ylabel('Card Value')
	
plt.close()
plt.close()
plt.close()
plt.close()


#7)taking out jumpturn7 model, and add the name of the epsilon-greedy and successive_non_candidate model name into the table






