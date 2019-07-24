# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:06:27 2018

Description: Get the average activity of source over duration(s) of observation.

@author: kalkm1
"""
import numpy as np
import datetime as dt

# decay law
def decay_law(a_o,t,s_T):
    # decay constant per hour
    l = np.log(2)/(s_T*24) 
    # time in hours
    t = t.days*24 + t.seconds/3600
    #activity after time
    a = a_o * np.exp(-l*t)
    
    return a

def avg_activity(a_o,t,s_T):
    # decay constant per hour
    l = np.log(2)/(s_T*24) 
    # integral of decay law
    a_t = (a_o/-l) * np.exp(-l*t)
    a_t0 = (a_o/-l)
    
    return (a_t - a_t0)/t
#------------------------------------------------------------------------------
# USER INPUT
# source reference info
s_info_a = 185 # MBq
s_info_dt = dt.datetime(2018,3,15)
s_T = 271.81  #days

# observation times (can put multiple start and end times)
obs_start = np.array([
                      dt.datetime(2018,9,14,7,58,51), # year,month,day,hour,minute,seconds
                      dt.datetime(2018,9,17,9,21,34)
                      ])
             
obs_end = np.array([
                    dt.datetime(2018,9,14,15,51,38),
                    dt.datetime(2018,9,17,15,50,42)
                    ])
#------------------------------------------------------------------------------
# DECAY CALCULATIONS
# get the duration of observations
obs_len = obs_end-obs_start

# get the start and end times from source activity date of observations
time2start = obs_start - s_info_dt
time2end = obs_end - s_info_dt

a_start = []
a_end = []
a_avg = []
t_obs = []
# get the average activity over each obs
for i in range(len(obs_len)):
    # obs length in hours
    t_obs.append(obs_len[i].days*24 + obs_len[i].seconds/3600)
    # acticity at start of observation
    a_start.append(decay_law(s_info_a, time2start[i], s_T))
    # activity at end of observation
    a_end.append(decay_law(s_info_a, time2end[i], s_T))
    # get average activity across observation
    a_avg.append(avg_activity(a_start[i],t_obs[i],s_T))
    
tot_t = sum(t_obs)
tot_avg_a = sum(a_avg)/len(a_avg)

# print results to file
with open('obs_time_activity.txt','w') as f:
    f.write('time(hours) avg_activity(MBq)\n')
    for i in range(len(obs_len)):
        f.write(format(t_obs[i],'.4f')+' '+format(a_avg[i],'.4f')+'\n')
    f.write(format(tot_t,'.4f')+' '+str(tot_avg_a))



