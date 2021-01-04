import numpy as np
import matplotlib.pyplot as pp

import csv
import math

# func for getting K and N
def calKN(p_s, p_t, v, no_safe, no_non_safe):
    j = 0 # to keep the count of final safe modes in the interval -> it would reduce for accomodating non-safe modes in the interval. final 
    # no of same modes in the interval = no_safe - j

    while True:
        i = 0
        p = p_s
        while(p > p_t and i < no_safe-j):
            p = p - v * (1/r)
            i += 1
        
        i = 0
        v_new = v
        while(p > p_t and i < no_non_safe):
            p = p - v_new * (1/r)
            v_new = v_new - b1*(1/r)
            i += 1

        # print("i: ", i)
        if ((i == no_non_safe and p >= p_t) or no_safe-j==0):
            break
        else:
            j += 1

    return no_non_safe, no_non_safe+no_safe-j

def genDetProb(pos):
    pos = pos/10

    # load data
    dists = np.load('vehicleDists.npy')
    confs = np.load('LECconfidences.npy')

    if(len(confs) != len(dists)):
        raise Exception('Array lengths not equal. CODE BETTER!')

    # for confThresh in confThreshs:
    confThresh = 0.6
    detectionsByDist = np.zeros(len(pos)-1)
    misdetectionsByDist = np.zeros(len(pos)-1)

    for i in range(len(confs)):
        conf = confs[i]
        dist = dists[i]
        distArrayIndex = 0

        for j in range(len(pos)-1):
            init_pos = pos[j]
            end_pos = pos[j+1]
            if end_pos <= dist <= init_pos:
                distArrayIndex = j

        if(conf >= confThresh):
            # Detection
            detectionsByDist[distArrayIndex] += 1
        else:
            misdetectionsByDist[distArrayIndex] += 1

    finalDetectionProbs = np.zeros(len(detectionsByDist))

    for index in range(len(detectionsByDist)):
        if detectionsByDist[index]+misdetectionsByDist[index] != 0:
            finalDetectionProbs[index] = detectionsByDist[index]/(detectionsByDist[index]+misdetectionsByDist[index])
        else:
            finalDetectionProbs[index] = finalDetectionProbs[index-1]
        if finalDetectionProbs[index] == 0:
            non_zero_det_index = index - 1
            while(finalDetectionProbs[non_zero_det_index] == 0): # assuming that at least the first det prob is not zero 
                non_zero_det_index -= 1
            finalDetectionProbs[index] = finalDetectionProbs[non_zero_det_index]

    # print(finalDetectionProbs)
    return finalDetectionProbs

# hyperparameters
fmu = 1
thd = 2
ttc_th = 6
x_th = 1
init_pos = 1600
r = 10
b1 = 40
b2 = 80
init_v = 200
amax = b2
crash_pos = 50
BD_b1 = (init_v*init_v)/(2*b1)
BD_b2 = (init_v*init_v)/(2*b2)

def get_pos_int(p, v):

    # local variables
    dis = []
    color = []
    p1 = [p] # p1 should start with the starting position
    k = [] # no of safe modes in the interval
    v_prevSM = []
    braking_actions_count = []
    br_cnt = 0
    # flag for non-safe mode
    flag_NSM = 0 # set to 1 if its a NSM
    flag_SM = 0 # set to 1 if there is a transition from NSM to SM
    flag_start = 0 # to indicate the start of the trace with the safe mode
    init_k = 0 # the no of safe modes in the first interval
    count = 0 # number of safe modes in an interval

    # position, p starts from intial distance between the car and the obstacle and then goes on decreasing towards 0
    while p >= crash_pos and v > 0:
        # not considering v_s - v_long term as v_s = v_long = v_0 (v) in our simulation
        # p_long = p
        dbr = (v * thd) + (fmu * ((v * v)/(2*amax)))
        dw = dbr + v * thd
        p_temp = p - crash_pos
        dis.append(p)
        x = (p_temp - dbr)/(dw - dbr)
        ttc = p_temp/v
        if (x > x_th and ttc > ttc_th): 
            # SAFE MODE
            if(p == init_pos):
                flag_start = 1
                init_k += 1
            if (flag_NSM == 1):
                if flag_start == 1:
                    k.append(init_k-1)
                    braking_actions_count.append(0)
                    v_prevSM.append(init_v)
                    flag_start = 0
                flag_NSM = 0
                flag_SM = 1
                count = 0
                braking_actions_count.append(br_cnt)
            if (flag_SM == 1):
                count = count + 1
            # for plotting purpose
            color.append('g')
        elif (x <= x_th and ttc <= ttc_th): 
            # COLLISION MITIGATION MODE
            if(flag_NSM == 1):
                br_cnt = br_cnt+1
            if (flag_NSM == 0):
                if p!= init_pos:
                    p1.append(p+v*(1/r))
                v_prevSM.append(v)
                flag_NSM = 1
                br_cnt = 1
            if(flag_SM == 1):
                flag_SM = 0
                k.append(count)
            v = v - b2*(1/r)
            # for plotting purpose
            color.append('r')
        else:
            # BRAKING MODE
            if(flag_NSM == 1):
                br_cnt = br_cnt+1
            if (flag_NSM == 0):
                if p!= init_pos:
                    p1.append(p+v*(1/r))
                v_prevSM.append(v)
                flag_NSM = 1
                br_cnt = 1 
            if (flag_SM == 1):
                flag_SM = 0
                k.append(count)
            v = v - b1*(1/r)
            # for plotting purpose
            color.append('b')
        if(v<0):
            v=0   
        p = p - v * (1/r)

    # check if the last mode was a non-safe mode, if yes add br_cnt to braking_actions_count and count to k. This is beacuse br_cnt and count were added to SM after
    # NSM but if the trace ends at NSM, then we will miss the last br_cnt and k
    if (flag_NSM == 1):
        braking_actions_count.append(br_cnt)

    if (flag_SM==1 or flag_NSM==1):
        k.append(count)

    # if all the modes in the last interal are safe mode then the no. of braking actions = 0
    # if(flag_SM == 1):
    #    braking_actions_count.append(0) 

    p1.append(p)

    # plotting the control modes in a original safe trace with all detections with control modes- green = SM, blue = BM and red = CMM
    _,ax = pp.subplots()
    # for distance starting from p1[0] till crash_pos on x-axis 
    ax.set_xlim(p1[0], crash_pos)
    ax.scatter(dis, [1 for _ in dis],color=color)
    pp.show(block=False)

    return p1, v_prevSM, k, braking_actions_count  

def get_inputs_for_KN_cal(int_pos, start_bm_p, v):

    # local variables
    dis = []
    color = []
    k = [] # no of safe modes in the interval
    prev_v = [v]
    braking_actions_count = [] # no. of braking action modes in the interval
    safe_mode_flag = 1 # cont with SM actions

    # iterate over each interval to get the no. of safe modes, non-safe modes and starting velocity for the intervals
    for i in range(len(int_pos)-1):
        start_pos = int_pos[i]
        end_pos = int_pos[i+1]
        if start_pos >= start_bm_p and start_bm_p >=end_pos: # this is the interval from which we can start applying brakes or start going into braking modes
            safe_mode_flag = 0
        p = start_pos
        count = 0 # for counting the no. of safe modes in the interval
        br_cnt = 0 # for counting the no. of braking modes in the interval
        while p >= end_pos and v > 0:
            dbr = (v * thd) + (fmu * ((v * v)/(2*amax)))
            dw = dbr + v * thd
            p_temp = p - crash_pos
            dis.append(p)
            x = (p_temp - dbr)/(dw - dbr)
            ttc = p_temp/v
            if (x > x_th and ttc > ttc_th) or (safe_mode_flag == 1):
                # SAFE MODE
                count += 1
                # for plotting purpose
                color.append('g')
            elif (x <= x_th and ttc <= ttc_th): 
                # COLLISION MITIGATION MODE
                br_cnt += 1
                v = v - b2*(1/r)
                # for plotting purpose
                color.append('r')
            else:
                # BRAKING MODE
                br_cnt += 1
                v = v - b2*(1/r)
                # for plotting purpose
                color.append('b')
            if(v<0):
                v=0   
            p = p - v * (1/r)
        braking_actions_count.append(br_cnt)
        k.append(count)
        if i != len(int_pos)-2:
            prev_v.append(v)
    
    print("Final vel: ", v)
    # plotting the control modes in a original safe trace with all detections with control modes- green = SM, blue = BM and red = CMM
    _,ax = pp.subplots()
    # for distance starting from p1[0] till crash_pos on x-axis 
    ax.set_xlim(int_pos[0], crash_pos)
    ax.scatter(dis, [1 for _ in dis],color=color)
    pp.show(block=False)

    return prev_v, k, braking_actions_count


##############################################################################################
# int_pos contains the interval positions and det_prob containts pr of det for these intervals
##############################################################################################

# get intervals for init_pos = 1600
int_pos = get_pos_int(p=init_pos, v=init_v)[0]
print("int pos: ", int_pos)
# THIS WILL BE SAME AS THE INTERVALS ARE SAME
det_prob = genDetProb(np.asarray(int_pos))
# print("det prob: ", det_prob)

############################################################
# trace_init_points contain starting points for diff traces
############################################################

no_traces = 10
trace_init_points = []
temp_init_pos = init_pos
div_int = (temp_init_pos-BD_b2)/(no_traces+1)
for i in range(no_traces):
    start_pos = temp_init_pos-div_int
    trace_init_points.append(start_pos)
    temp_init_pos = start_pos

print("trace init points: ", trace_init_points)
# trace_init_points[0] = 300

for trace_no in range(no_traces):
    prev_v, k, braking_actions_count = get_inputs_for_KN_cal(int_pos, start_bm_p=trace_init_points[trace_no], v=init_v)

    out_k = []
    out_n = []
    orig_n = []

    i = 0
    while (i<len(int_pos)-1):
        new_k, new_n = calKN(int_pos[i], int_pos[i+1], prev_v[i], k[i], braking_actions_count[i])
        out_k.append(new_k)
        out_n.append(new_n)
        orig_n.append(k[i]+braking_actions_count[i])
        i = i+1
    
    print("N- ", out_n)
    print("K- ", out_k)

    orig_k = out_k.copy()

    beg_int_no = int(len(int_pos)/2)
    last_int_no = int(len(int_pos)/4)
    middle_int_no = len(int_pos)-beg_int_no-last_int_no
    print("beg_int_no, middle_int_no, last_int_no")
    print(beg_int_no, middle_int_no, last_int_no)

    ######################################################################
    # making beg_int braking counts to 0 by shifting them to middle_int
    #####################################################################
    i = 0
    count_shift_br_modes = 0

    while i<beg_int_no:
        if orig_k[i] != 0 and i+beg_int_no<beg_int_no+middle_int_no-1: # and i+... to make sure that we remain in the mid-interval
            out_k[i+beg_int_no] += orig_k[i]
            out_k[i] = 0
        i += 1
    
    i = 0
    while i<beg_int_no:
        if out_k[i] != 0:
            count_shift_br_modes += out_k[i]
            out_k[i] = 0
        i += 1
    
    # print("No of braking modes to be shifted right from the beg_inter", count_shift_br_modes)

    ##################################################################
    # adjusting mid_int braking counts such that k <= half of n there
    ##################################################################
    j = 0
    while j < middle_int_no:
        while 2*out_k[i] > out_n[i]:
            count_shift_br_modes += 1
            out_k[i] -= 1
        i += 1
        j += 1

    i = len(int_pos)-3
    while count_shift_br_modes > 0 and i > len(int_pos)-last_int_no-3: # cond on i to make sure that we are in the last interval  
        # print("Orig out_n[i]: {}, out_k[i]: {}".format(out_n[i], out_k[i]))
        while (out_n[i]>(2*out_k[i])):
            out_k[i] += 1
            count_shift_br_modes -= 1
            # print("i: {}, out_k[i]: {}, count_shift_br_modes: {}".format(i, out_k[i], count_shift_br_modes))
            if (count_shift_br_modes == 0):
                break
        i -= 1
    
    # i = 0
    # while i < beg_int_no:
    #     out_k[i] = 0
    #     i += 1

    no_org_br_modes = 0
    i = 0
    while i<len(orig_k):
        no_org_br_modes += orig_k[i]
        i += 1

    print("No of br modes in orig_k - ", no_org_br_modes)

    no_new_br_modes = 0
    i = 0
    while i<len(out_k):
        no_new_br_modes += out_k[i]
        i += 1

    print("No of br modes in new_k - ", no_new_br_modes)

    print("Orig K ", orig_k)
    print("Final k ", out_k)



    if trace_no == 0:
        file_open_perm = 'w'
    else:
        file_open_perm = 'a'

    with open('PRISMInput.csv', file_open_perm, newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(out_n)):
            csvwriter.writerow([out_n[i]])
        csvwriter.writerow(['K_'+str(trace_no+1)])
        for i in range(len(out_k)):
            csvwriter.writerow([out_k[i]])
        csvwriter.writerow(['det_tth_'+str(trace_no+1)])
        csvwriter.writerow([np.max(out_n)])


with open('PRISMInput.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csvwriter.writerow(['pos'])
    for i in range(len(int_pos)):
        csvwriter.writerow([int(int_pos[i])])

    csvwriter.writerow(['det_prob'])
    for i in range(len(det_prob)):
        csvwriter.writerow([det_prob[i]])

y = [0.3605542716422943,0.3605542716422943,0.3605542716422943,0.3605542716422943,0.3605542716422943,0.35581527828281323,0.3526069808849782,0.3532383421518331,0.34186204585230123,0.3768965320861802,
0.4698452101449819, 0.4461854950505571,0.39390,0.33379494402599713]
x = [1600,1500,1400,1300,1200,1100,1000,900,800,700,600,500,400,300]

fig, ax = pp.subplots()
ax.scatter(x, y)

ax.set(ylabel='pr of failure', xlabel='start positions',
       title='Inc in acc with dec in conservatism?')
pp.show(block=False)
    

