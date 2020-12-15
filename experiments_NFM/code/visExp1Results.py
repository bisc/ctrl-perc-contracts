import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d




dists = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200]
speeds = [10,14,18,22,26]
X,Y = np.meshgrid(speeds,dists)



resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\results\\exp1\\crashProbs.csv')
resultsFileCrashDeltaDProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\results\\exp1\\crashProbsDeltad.csv')

crashProbs = []
crashProbsDeltad = []

csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
for row in csv_reader_probs_array:
    tempCrashProbsArray = []
    for col in row:
        tempCrashProbsArray.append(float(col))
    crashProbs.append(tempCrashProbsArray)

csv_reader_probs_array = csv.reader(resultsFileCrashDeltaDProbs, delimiter=',')
for row in csv_reader_probs_array:
    tempCrashProbsArray = []
    for col in row:
        tempCrashProbsArray.append(float(col))
    crashProbsDeltad.append(tempCrashProbsArray)

diffsInCrashProb = []
XMosViolated = []
YMosViolated = []

XMosHolds = []
YMosHolds = []
numPointsWithDiff=0
sumPointsWithDiff=0
sumPointsNoDiff=0

diffsInCrashProbNotHolds = []
diffsInCrashProbHolds = []
maxDiffInProbs = 0
for i in range(len(crashProbs)):
    tempCrashProbs = crashProbs[i]
    tempCrashProbsDeltad = crashProbsDeltad[i]
    tempdiffsInCrashProb = []
    for j in range(len(tempCrashProbs)):
        crashProb = tempCrashProbs[j]
        crashProbDeltad = tempCrashProbsDeltad[j]
        tempDiffInProbs = crashProb-crashProbDeltad
        tempdiffsInCrashProb.append(tempDiffInProbs)
        if(abs(tempDiffInProbs)>maxDiffInProbs):
            maxDiffInProbs = abs(tempDiffInProbs)
        if(tempDiffInProbs<0):
            XMosViolated.append(dists[i])
            YMosViolated.append(speeds[j])
            diffsInCrashProbNotHolds.append(abs(tempDiffInProbs))
            numPointsWithDiff+=1
            sumPointsWithDiff+=abs(tempDiffInProbs)
        else:
            sumPointsNoDiff+=abs(tempDiffInProbs)
            XMosHolds.append(dists[i])
            YMosHolds.append(speeds[j])
            diffsInCrashProbHolds.append(abs(tempDiffInProbs))

    diffsInCrashProb.append(tempdiffsInCrashProb)
    print(tempdiffsInCrashProb)


print(numPointsWithDiff)
print(sumPointsWithDiff)
print(sumPointsNoDiff)
rgba_colors_diff = np.zeros((len(diffsInCrashProbNotHolds),4))
rgba_colors_diff[:,0] = 1.0
alphas = np.asarray(diffsInCrashProbNotHolds)/maxDiffInProbs
rgba_colors_diff[:,3] = alphas
plt.scatter(XMosViolated,YMosViolated,marker="X",color=rgba_colors_diff)

rgba_colors_nodiff = np.zeros((len(diffsInCrashProbHolds),4))
rgba_colors_nodiff[:,2] = 1.0
alphas_nodiff = np.asarray(diffsInCrashProbHolds)/maxDiffInProbs
rgba_colors_nodiff[:,3] = alphas_nodiff

plt.scatter(XMosHolds,YMosHolds,marker="*",color=rgba_colors_nodiff)


TTCThresh = 6
distVals = np.arange(0,210,0.5)
TTCVals = distVals/6
plt.plot(distVals,TTCVals,'--',color='green',alpha=0.5)

xThresh=1
amax=8
thd=2

speedVals = np.arange(0,30,0.5)
# XwarningVals = (xThresh-speedVals/(2*amax))*thd*speedVals
XwarningVals = thd*speedVals + (speedVals*speedVals)/(2*amax)
plt.plot(XwarningVals,speedVals,'--',color='black',alpha=0.5)




plt.xlabel('Distance to Obstacle',fontsize=20)
plt.ylabel('Speed of Car',fontsize=20)
plt.ylim((8,28))
plt.xlim((0,210))

# plt.title('MoS for Varied Initial Distances and Speeds')
plt.show()





