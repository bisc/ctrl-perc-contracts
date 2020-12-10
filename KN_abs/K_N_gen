import numpy as np
import matplotlib.pyplot as pp

import csv
import math

import argparse

parser = argparse.ArgumentParser(description='Generate K/N pairs for abstraction')
parser.add_argument('--no_traces', default=1, help='number of traces for the starting point of non-braking mode')
parser.add_argument('--outf', default='PRISMInput_test.csv', help='output file from where PRISM model will be generated')
parser.add_argument('--fmu', default=1)
parser.add_argument('--thd', default=2)
parser.add_argument('--ttc_th', default=6)
parser.add_argument('--x_th', default=1)
parser.add_argument('--init_pos', default=1600)
parser.add_argument('--r', default=10)
parser.add_argument('--b1', default=40)
parser.add_argument('--b2', default=80)
parser.add_argument('--init_v', default=200)
parser.add_argument('--crash_pos', default=50)

args = parser.parse_args()

prism_input_file = args.outf
no_traces = int(args.no_traces)

#no_traces = 1

# hyperparameters
fmu = float(args.fmu)
thd = float(args.thd)
ttc_th = float(args.ttc_th)
x_th = float(args.x_th)
init_pos = float(args.init_pos)
r = float(args.r)
b1 = float(args.b1)
b2 = float(args.b2)
init_v = float(args.init_v)
crash_pos = float(args.crash_pos)


amax = b2
BD_b1 = (init_v*init_v)/(2*b1)
BD_b2 = (init_v*init_v)/(2*b2)

max_n = 10

def getNewInt(int_pos, n_pos, out_n):
    # print(len(int_pos))
    new_pos = int_pos.copy()
    j=0
    for i in range(len(out_n)):
        if out_n[i] > max_n:
            # print("i: ", i)
            num_elems = out_n[i]
            if (num_elems != len(n_pos[i])):
                print(num_elems,len(n_pos[i]))
                raise Exception("No. of N != sample position's len")
            counter = 1
            while True:
                idx = counter*max_n
                if idx>=num_elems:
                    break
                # print("sample_pos: ", n_pos[i])
                new_pos.insert(i+1+j,n_pos[i][idx-1])
                counter+=1
                # print("insert_pos: ", n_pos[i][idx-1])
                j += 1

    # print(len(new_pos))
    return new_pos


# func for getting K and N
def calKN(p_s, p_t, v, no_safe, no_non_safe, brake_level, int_no):
    if (len(brake_level[int_no]) != no_non_safe):
        raise Exception("No of non-safe modes != braking level counts for the interval: ", int_no+1)

    j = 0 # to keep the count of final safe modes in the interval -> it would reduce for accomodating non-safe modes in the interval. final 
    # no of same modes in the interval = no_safe - j

    # print("p_s: ", p_s)
    # print("p_t: ", p_t)
    sample_pos = []

    start_non_safe = 0

    while True:
        i = 0
        p = p_s
        sample_pos = [] # pos of each of the final N sample
        sample_pos.append(p_s)

        if no_safe != 0:
            p = p - v * (1/r)
            while(p > p_t and i < no_safe-j-1):
                sample_pos.append(p)
                p = p - v * (1/r)
                i += 1
        else:
            start_non_safe = 1
        
        # print("i: ", i)
        i = 0
        v_new = v

        while(p > p_t and i < no_non_safe):
            if start_non_safe != 1:
                sample_pos.append(p)
            else:
                start_non_safe = 0 # as p = p_s here, so no need to append
            v_new = v_new - brake_level[int_no][i]*(1/r)
            p = p - v_new * (1/r)
            i += 1

        if ((i == no_non_safe and p > p_t) or no_safe-j==0):
            # if (not(i == no_non_safe) or not(p >= p_t)) and (no_safe-j==0): # to handle the case when with no of non-safe modes, 
            #                                                         # braking b1 goes into next interval with non-safe mode actions- get min b2 braking modes
            #     no_cmm = 0
            #     print("total no of samples in this int: {}, len(sample_pos): {}, v_curr: {}, v_next: {}, p: {}, p_t: {}, i: {}, no_non_safe: {}".format(no_non_safe+no_safe-j, len(sample_pos), v_new, v_next, p, p_t, i, no_non_safe))
            #     while True:
            #         if (not(i == no_non_safe) or not(p >= p_t)):
            #             print("Here")
            #             if i <= no_non_safe and v_new <= v_next and p>=p_t:
            #                 no_non_safe = i
            #                 break
            #             print("i: {}, non_non_safe: {}".format(i, no_non_safe))
            #             if i==no_non_safe:
            #                 print("p_s: {}, p: {} and p_t: {}, i: {}, no_non_safe: {}, cmm: {}".format(p_s, p, p_t, i, no_non_safe, no_cmm))
            #                 break
            #             p = p_s
            #             sample_pos = [] 
            #             if first_int_flag == 1:
            #                 sample_pos.append(p_s)
            #             no_cmm += 1
            #             print("cmm: ", no_cmm)
            #             i = 0
            #             p=p_s
            #             v_new = v
            #             for _ in range(no_cmm):
            #                 p = p - v_new * (1/r)
            #                 sample_pos.append(p)
            #                 v_new = v_new - b2*(1/r)
            #                 i += 1
            #                 # print("i= {} for no_cmm= {} ".format(i, no_cmm))
            #             while i < no_non_safe and p>=p_t:
            #                 p = p - v_new * (1/r)
            #                 sample_pos.append(p)
            #                 v_new = v_new - b1*(1/r)
            #                 i += 1
            #                 print("i= {} for no_non_safe= {} and p: {}".format(i, no_non_safe, p))
                    # else:
                    #     break

            break
        else:
            j += 1

    # print("len of sample_pos: ", len(sample_pos))
    # if first_int_flag:
    # print("no of non_safe: ", no_non_safe)
    # print("no of safe: ", no_safe)
    # print("j: ", j)
    # print("total no of samples in this int: ", no_non_safe+no_safe-j)
    # if(no_non_safe+no_safe-j != len(sample_pos)):
    #     print("no_non_safe: ", no_non_safe)
    #     print("no_safe-j: ", no_safe-j)
    #     print("len(sample_pos): ", len(sample_pos))

    # print("Orig safe: {}, non_safe: {}".format(no_safe, no_non_safe))
    # print("new safe: {}, no_non_safe: {}, len(sample_pos): {} ".format(no_safe-j, no_non_safe, len(sample_pos)))

    return no_non_safe, no_non_safe+no_safe-j, sample_pos

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

    brake_level = [] # for the entire trace
    brake_level_cur_int = []

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
                    brake_level.append(brake_level_cur_int)
                    brake_level_cur_int = []
                v_prevSM.append(v)
                flag_NSM = 1
                br_cnt = 1
            if(flag_SM == 1):
                flag_SM = 0
                k.append(count)
            v = v - b2*(1/r)
            brake_level_cur_int.append(b2)
            # for plotting purpose
            color.append('r')
        else:
            # BRAKING MODE
            if(flag_NSM == 1):
                br_cnt = br_cnt+1
            if (flag_NSM == 0):
                if p!= init_pos:
                    p1.append(p+v*(1/r))
                    brake_level.append(brake_level_cur_int)
                    brake_level_cur_int = []
                v_prevSM.append(v)
                flag_NSM = 1
                br_cnt = 1 
            if (flag_SM == 1):
                flag_SM = 0
                k.append(count)
            v = v - b1*(1/r)
            brake_level_cur_int.append(b1)
            # for plotting purpose
            color.append('b')
        if(v<0):
            v=0   
        p = p - v * (1/r)

    if v != 0:
        raise Exception("In gen of intervals, this is not a safe trace as final v: {}".format(v))

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
    brake_level.append(brake_level_cur_int)

    if(len(braking_actions_count) != len(brake_level)):
        raise Exception("Len of braking actions count for the trace (len(N/K)) should be equal to the len of braking level (containing brake level for each interval)")

    for i in range(len(braking_actions_count)):
        if braking_actions_count[i] != len(brake_level[i]):
            # print("No of braking modes: {}, len of brake levels: {}".format(braking_actions_count[i], len(brake_level[i])))
            raise Exception("No of braking levels is not equal to the length of the braking actions count for the interval: ", i+1)

    # plotting the control modes in a original safe trace with all detections with control modes- green = SM, blue = BM and red = CMM
    # _,ax = pp.subplots()
    # # for distance starting from p1[0] till crash_pos on x-axis 
    # ax.set_xlim(p1[0], crash_pos)
    # ax.scatter(dis, [1 for _ in dis],color=color)
    # pp.show(block=False)

    return p1, v_prevSM, k, braking_actions_count  

def get_inputs_for_KN_cal(int_pos, start_bm_p, v):

    # local variables
    dis = []
    color = []
    k = [] # no of safe modes in the interval
    prev_v = [v]
    braking_actions_count = [] # no. of braking action modes in the interval
    safe_mode_flag = 1 # cont with SM actions

    brake_level = [] # for the entire trace

    # iterate over each interval to get the no. of safe modes, non-safe modes and starting velocity for the intervals
    for i in range(len(int_pos)-1):
        start_pos = int_pos[i]
        end_pos = int_pos[i+1]
        brake_level_cur_int = []
        if start_pos >= start_bm_p and start_bm_p > end_pos: # this is the interval from which we can start applying brakes or start going into braking modes
            safe_mode_flag = 0
        p = start_pos
        count = 0 # for counting the no. of safe modes in the interval
        br_cnt = 0 # for counting the no. of braking modes in the interval
        while p > end_pos and v > 0:
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
                brake_level_cur_int.append(b2)
                # for plotting purpose
                color.append('r')
            else:
                # BRAKING MODE
                br_cnt += 1
                v = v - b1*(1/r)
                brake_level_cur_int.append(b1)
                # for plotting purpose
                color.append('b')
            if(v<0):
                v=0   
            p = p - v * (1/r)
        braking_actions_count.append(br_cnt)
        k.append(count)
        brake_level.append(brake_level_cur_int)
        if i != len(int_pos)-2:
            prev_v.append(v)        

    if v != 0:
        br_intro_int = len(k)-2
        while(v>0):
            while(k[br_intro_int] == 0): # finding the first interval where we can add braking counts to make velocity = 0
                br_intro_int -= 1
                print("index: ", br_intro_int)
            # print(i)
            v = v - b1*(1/r)
            braking_actions_count[br_intro_int] += 1
            k[br_intro_int] -= 1
            brake_level[br_intro_int].append(b1)
    # print(k)
    # print(braking_actions_count)

    if v > 0:
        raise Exception("This is not a safe trace as final v: {}".format(v))
    # plotting the control modes in a original safe trace with all detections with control modes- green = SM, blue = BM and red = CMM
    # _,ax = pp.subplots()
    # # for distance starting from p1[0] till crash_pos on x-axis 
    # ax.set_xlim(int_pos[0], crash_pos)
    # ax.scatter(dis, [1 for _ in dis],color=color)
    # pp.show(block=False)


    if(len(braking_actions_count) != len(brake_level)):
        raise Exception("In get_inputs(), len of braking actions count for the trace (len(N/K)) should be equal to the len of braking level (containing brake level for each interval)")

    for i in range(len(braking_actions_count)):
        if braking_actions_count[i] != len(brake_level[i]):
            # print("No of braking modes: {}, len of brake levels: {}".format(braking_actions_count[i], len(brake_level[i])))
            raise Exception("In get_inputs(), no of braking levels is not equal to the length of the braking actions count for the interval: ", i+1)

    return prev_v, k, braking_actions_count, brake_level


##############################################################################################
# int_pos contains the interval positions and det_prob containts pr of det for these intervals
##############################################################################################

# get intervals for init_pos = 1600
int_pos = get_pos_int(p=init_pos, v=init_v)[0]
# print("int pos: ", int_pos)
# THIS WILL BE SAME AS THE INTERVALS ARE SAME
det_prob = genDetProb(np.asarray(int_pos))
# print("det prob: ", det_prob)

############################################################
# trace_init_points contain starting points for diff traces
############################################################

trace_init_points = []
temp_init_pos = init_pos
div_int = (temp_init_pos-BD_b2)/(no_traces+1)
for i in range(no_traces):
    start_pos = temp_init_pos-div_int
    trace_init_points.append(start_pos)
    temp_init_pos = start_pos

# trace_init_points[0] = 300
# trace_init_points[1] = 400
# trace_init_points[2] = 500
# trace_init_points[3] = 600
# trace_init_points[4] = 700
# trace_init_points[5] = 800
# trace_init_points[6] = 900
# trace_init_points[7] = 1000
# trace_init_points[8] = 1100
# trace_init_points[9] = 1200
# trace_init_points[10] = 1300
# trace_init_points[11] = 1400
# trace_init_points[12] = 1600
# trace_init_points[13] = 1500

# print(trace_init_points)
#################################################################################################
# SPILITING INTERVALS for allowing max_n, ASSUMPTION every int will have at most 2*max_n samples
#################################################################################################

init_int_pos_len = len(int_pos)
# print("Initially len of int_pos: ", init_int_pos_len)

while True:
    all_trace_satisfied = [False]*no_traces
    for trace_no in range(no_traces):
        prev_v, k, braking_actions_count, brake_level = get_inputs_for_KN_cal(int_pos, start_bm_p=trace_init_points[trace_no], v=init_v)
        # print(prev_v)

        out_k = []
        out_n = []
        orig_n = []
        n_pos = []

        i = 0
        while (i<len(int_pos)-1):
            new_k, new_n, sample_pos = calKN(int_pos[i], int_pos[i+1], prev_v[i], k[i], braking_actions_count[i], brake_level, i)
        
            # print(new_n, int_pos[i], int_pos[i+1], prev_v[i], k[i], sample_pos)
            n_pos.append(sample_pos)
            out_k.append(new_k)
            out_n.append(new_n)
            orig_n.append(k[i]+braking_actions_count[i])
            i = i+1

        # print("N: ", out_n)
        if max(out_n)<=max_n:
            all_trace_satisfied[trace_no]=True
        else:
            all_trace_satisfied[trace_no]=False
            # print("Not satisfied: ", max(out_n))
            # print("N: ", out_n)
            int_pos = getNewInt(int_pos, n_pos, out_n)
            # print("int_pos: ", int_pos)
            
    can_break = True 
    # print("now len of int_pos: ", len(int_pos))   
    for val in all_trace_satisfied:
        # if not val and len(int_pos)<2*init_int_pos_len:
        if not val:
            can_break = False
    
    if can_break:
        # print("final int_pos: ", int_pos)
        break



for trace_no in range(no_traces):
    prev_v, k, braking_actions_count, brake_level = get_inputs_for_KN_cal(int_pos, start_bm_p=trace_init_points[trace_no], v=init_v)
    # print(prev_v)

    out_k = []
    out_n = []
    orig_n = []

    i = 0
    while (i<len(int_pos)-1):
        new_k, new_n, sample_pos = calKN(int_pos[i], int_pos[i+1], prev_v[i], k[i], braking_actions_count[i], brake_level, i)

        
        # print(new_n, int_pos[i], int_pos[i+1], prev_v[i], k[i], sample_pos)
        out_k.append(new_k)
        out_n.append(new_n)
        orig_n.append(k[i]+braking_actions_count[i])
        i = i+1

    orig_k = out_k.copy()

    # print(out_n)
    beg_int_no = int(len(int_pos)/3)
    last_int_no = int(len(int_pos)/3)
    middle_int_no = len(int_pos)-beg_int_no-last_int_no
    # print("beg_int_no, middle_int_no, last_int_no")
    # print(beg_int_no, middle_int_no, last_int_no)

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
            if out_k[i] == 1 and out_n[i] == 1: # allowing n[i] = k[i] = 1
                break
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

    # print("No of br modes in orig_k - ", no_org_br_modes)

    no_new_br_modes = 0
    i = 0
    while i<len(out_k):
        no_new_br_modes += out_k[i]
        i += 1

    # print("No of br modes in new_k - ", no_new_br_modes)

    # print("Orig K ", orig_k)
    print("N ", out_n)
    # print("len of N- ", len(out_n))
    out_k = orig_k
    print("K ", out_k)



    if trace_no == 0:
        file_open_perm = 'w'
    else:
        file_open_perm = 'a'

    with open(prism_input_file, file_open_perm, newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(out_n)):
            csvwriter.writerow([out_n[i]])
        csvwriter.writerow(['K_'+str(trace_no+1)])
        for i in range(len(out_k)):
            csvwriter.writerow([out_k[i]])
        csvwriter.writerow(['det_tth_'+str(trace_no+1)])
        csvwriter.writerow([np.max(out_n)])


with open(prism_input_file, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csvwriter.writerow(['pos'])
    for i in range(len(int_pos)):
        csvwriter.writerow([int(int_pos[i])])

    csvwriter.writerow(['det_prob'])
    for i in range(len(det_prob)):
        csvwriter.writerow([det_prob[i]])

# y = [0.6385058893251953,0.6385058893251953,0.6385058893251953,0.6385058893251953,0.6385058893251953,0.6318003255782084,0.6204441158046315,0.6181597208628999,0.6182424354532788,0.6398099355363625,
# 0.5388508108673669,0.4784799808246903,0.4269491223737356,0.3707666173544963]
# x = [1600,1500,1400,1300,1200,1100,1000,900,800,700,600,500,400,300]

# fig, ax = pp.subplots()
# ax.scatter(x, y)

# ax.set(ylabel='pr of failure', xlabel='start positions',
#        title='Inc in acc with dec in conservatism?')
# pp.show(block=False)
   
