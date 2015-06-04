'''
checking the feedback results
to-do-list:

2)figure out when the results is better/>= optimal
3)find all the behavioral metrics:
a)score
b)num explore
c)starting_place 
d)# switching
etc

##done:
1)find all the related results mat file
'''
import pylab
pylab.ion()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 
import statsmodels.api as sm



pop = scipy.io.loadmat('population.mat')
pop = pop['population']
#parameter setting
num_turn = 20
num_trial = 30
num_subj = pop.shape[0]/(num_turn*num_trial)
header = ['subjectid','trial','turn','exploit','switch_exploit','timeofclick','timesincelastclick','numberofcards','cardvalue','maxvalueontable','totalpoint',
         'optimalthreshold','totaloptimalpoints','optimalcardnumber','maxvalonoptimaltable','isoptimalexploiting','optimalcardvalue']
    
data0 = pd.DataFrame(pop, columns = header)

#create a new df with only 5700 rows, as each standing for each trial
idx_lst = range(num_turn-1,num_trial*num_turn*num_subj,num_turn)
data = data0.loc[idx_lst,['subjectid','trial','totalpoint','totaloptimalpoints']]

#compute the final score for each trial both for subjects and also for optimal
#define subject out performs optimal as 1, and not equal or better than optimal as 0
data.loc[:, 'outperform'] = data.apply(lambda x: x['totalpoint']>= x['totaloptimalpoints'], axis = 1)
#check the outperform distribution over trials
tmp = data.groupby('trial').outperform.apply(np.sum).apply(lambda x: x/float(num_subj)).reset_index()
plt.plot(tmp.trial,tmp.outperform, color ='g', lw= 3.0)
plt.axis([0,30,0,1])
plt.xlabel('Trials')
plt.ylabel('optimal percent across subjects')
plt.title('the percentage of optimal performance across all subjects on every trial')
plt.close()


##compute the metrics of score, nun_explore, starting_place for each trial of each subj
#score is just the score on every trial
# num of explore
# num of switching---you have to -1 after summing across one trial b/c the first turn is always 1
data.set_index(['subjectid','trial'], inplace = True)
num_ex = num_turn - data0.groupby(['subjectid','trial']).exploit.agg(np.sum) 
num_ex.name = 'num_explore'
num_switch = data0.groupby(['subjectid','trial']).switch_exploit.agg(np.sum) - 1 
num_switch.name = 'num_switch'
data = pd.concat([data, num_ex, num_switch], axis = 1, join ='outer')

#first consecutive exploit(FCE)
#first add the value of exexe the turn and the turn-next, and then add 2 to the 20turns
#then find the first 2, that is where the first consecutive exploit happening
def find_1st_consecu_exploit_turn(x):
	'''
	x here is exex of one trial. with a length of 20 
	first add the value of exexe the turn and the turn-next, and then add 2 to the 20turns
	then find the first 2, that is where the first consecutive exploit happening
	'''
	#first x is a pd.Series object, transfer to a list
	x = x.values.tolist()
	num_turns = len(x)
	tmp = []
	for i in range(num_turns-1):
		tmp.append(x[i]+x[i+1])
	#for the 20th turn	
	tmp.append(2)
	#return the first 2 and +1 for the turn-place
	return tmp.index(2)+1


first_consec_exploit_turn = data0.groupby(['subjectid','trial']).exploit.apply(find_1st_consecu_exploit_turn)
first_consec_exploit_turn.name = 'first_con_exploit_turn'
data = pd.concat([data, first_consec_exploit_turn],axis = 1, join = 'outer')

##combine them and only compare the 19 trials for each subj
#for outperform, we want every 1-29 trials value--this is the previous trial results
#for score, #ex #sw FS-turn, we want 2-30 trial value
#for subjectid and trial part, we also use 2-30 trials
data.reset_index(inplace = True)
data.shape[0] 

tmp_outperform = data.outperform[~(data.trial == 30)]
tmp_other = data.loc[~(data.trial == 1), :].copy()
tmp_other.loc[:, 'outperform'] = tmp_outperform.values






