import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d







resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\results\\exp2\\exp2CrashProbsAllAllPoints.csv')

crashProbs = []

csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
for row in csv_reader_probs_array:
    tempCrashProbsArray = []
    for col in row:
        crashProbs.append(float(col))


initDistLower = 20
initDistUpper = 130
distanceDisc = 0.5
numPoints = round((initDistUpper-initDistLower)/distanceDisc+1)

indLower = round((initDistLower-0.5)/distanceDisc+1)
indUpper = indLower+numPoints
dists = np.linspace(initDistLower,initDistUpper,numPoints,endpoint=True)

plt.plot(dists,crashProbs[indLower:indUpper],color='black')
plt.xlabel('Initial Distance (m)',fontsize=20)
plt.ylabel('Crash Probability',fontsize=20)
# plt.title('Crash Probability for Initial Speed=20m/s')
plt.show()