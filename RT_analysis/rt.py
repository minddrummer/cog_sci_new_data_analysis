'''
the model is: treat the linear relation between switching/repetition and RT
use all the samples from all the subjects
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io 

pop = scipy.io.loadmat('population.mat')
pop = pop['population']

##pop is a numpy.array
##col1: id, col2: trial_num, col3:turn_num, col4:ExEx, col5: switchOrNot
##col6: timestamp, col7: RT

print pop[0,:]






