import numpy as np
import matplotlib.pyplot as pp

# FUNCTION for calculating K for the worst-case for all but last sub-interval
# p1 is the position of the first non-safe mode in the sub-interval, p2 is the position of the last safe mode in the sub-interval, v is the velocity at the safe mode before the start of sub-interval
def calK(p1, p2, k, v):
	i = 0
	j = 0
	p_t = p2+1
	while(p_t > p2 and (k-j > 0)):
		p = p1
		i = 0
		while (i < k-j):
			p = p - v * (1/r)
			i = i+1
		p_t = p
		j = j+1

	return k-j
    
# hyperparameters
fmu = 1
thd = 1
amax = 20
ttc_th = 10
x_th = 2
p = 100
r = 10
b1 = 10
b2 = 20
v = 13.4
dis = []
color = []
p1 = []
p2 = []
k = []
v_prevSM = []
braking_actions_count = []
br_cnt = 0
# flag for non-safe mode
flag_NSM = 0
flag_SM = 0
count = 0

# position, p starts from intial distance between the car and the obstacle and then goes on decreasing towards 0
while p >= 0 and v > 0:
    dis.append(p)
    # not considering v_s - v_long term as v_s = v_long = v_0 (v) in our simulation
    # p_long = p
    dbr = (v * thd) + (fmu * ((v * v)/(2*amax)))
    dw = dbr + v * thd
    x = (p - dbr)/(dw - dbr)
    ttc = p/v
    if (x>=x_th and ttc <= ttc_th):
        # SAFE MODE
        if (flag_NSM == 1):
            flag_NSM = 0
            flag_SM = 1
            count = 0
            braking_actions_count.append(br_cnt)
        if (flag_SM == 1):
            count = count + 1
        # for plotting purpose
        color.append('g')
    elif (x < x_th and ttc > ttc_th):
        # COLLISION MITIGATION MODE
        if(flag_NSM == 1):
            br_cnt = br_cnt+1
        if (flag_NSM == 0):
            p1.append(p)
            v_prevSM.append(v)
            flag_NSM = 1
            br_ac = []
            br_ac.append(b1)
        if(flag_SM == 1):
            flag_SM = 0
            k.append(count)
            p2.append(p + (v*(1/r)))
        v = v - b2*(1/r)
        # for plotting purpose
        color.append('r')
    else:
        # BRAKING MODE
        if(flag_NSM == 1):
            br_cnt = br_cnt+1
        if (flag_NSM == 0):
            p1.append(p)
            v_prevSM.append(v)
            flag_NSM = 1
            br_cnt = 1
        if (flag_SM == 1):
            flag_SM = 0
            k.append(count)
            p2.append(p + (v*(1/r)))
        v = v - b1*(1/r)
        # for plotting purpose
        color.append('b')
    if(v<0):
        v=0   
    p = p - v * (1/r)

# plotting the control modes in a original safe trace with all detections with control modes- green = SM, blue = BM and red = CMM
fig,ax = pp.subplots()
# for distance starting from 100 till 0 on x-axis 
ax.set_xlim(100, 0)
ax.scatter(dis, [1 for _ in dis],color=color)
pp.show()

i = 0
out_k = []
out_n = []

while (i<len(p2)):
    new_k = calK(p1[i], p2[i], k[i], v_prevSM[i])
    out_k.append(new_k)
    out_n.append(new_k + braking_actions_count[i])
    i = i+1

# out_k contains the worst-case K numbers for all but the last sub-interval
print("Worst-case K")
print(out_k)
# out_n contains the worst-case N numbers for all but the last sub-interval. For a sub-interval i, it is calculated as worst-case Ki + number of braking actions in the i sub-interval of original trace
print("Worst-case N= worst-case K + number of braking actions in the sub-interval") 
print(out_n)

# For last sub-interval, K and N would be calcualted manually based on current position and speed of the car at the beginning of this sub-interval


