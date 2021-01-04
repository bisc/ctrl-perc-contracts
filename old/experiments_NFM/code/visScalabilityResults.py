import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


##############################
## N5 H5
##############################
N=3
H=3
L=3

showOlegBaseline=True
showOlegBaselineWithRounding=True
showExactBaseline=True
showBaselineWithRounding=True
showLattice=True
showRamneetKN=True

useLogScale=True

dists = [100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200]
speeds = [10,14,18,22,26]
X,Y = np.meshgrid(speeds,dists)


distsSmall = [120,125,130,135,140]
speedsSmall = [10,14,18,22,26]
XSmall,YSmall = np.meshgrid(speedsSmall,distsSmall)



if(showOlegBaseline):
    crashProbsArrayOlegBaseline = []
    runTimesArrayOlegBaseline = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\crashOlegBaselineNoRounding.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\runTimesOlegBaselineNoRounding.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayOlegBaseline.append(tempCrashProbsArray)
    crashProbsArrayOlegBaselineFlat = [item for sublist in crashProbsArrayOlegBaseline for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayOlegBaseline.append(tempRunTimesArray)
    runTimesArrayOlegBaselineFlat = [item for sublist in runTimesArrayOlegBaseline for item in sublist]



if(showOlegBaselineWithRounding):
    crashProbsArrayOlegBaselineWithRounding = []
    runTimesArrayOlegBaselineWithRounding = []

    resultsFileCrashProbsWithRounding = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\crashOlegBaselineWithRounding.csv')
    resultsFileRunTimesWithRounding = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\runTimesOlegBaselineWithRounding.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbsWithRounding, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArrayWithRounding = []
        for col in row:
            tempCrashProbsArrayWithRounding.append(float(col))
        crashProbsArrayOlegBaselineWithRounding.append(tempCrashProbsArrayWithRounding)
    crashProbsArrayOlegBaselineWithRoundingFlat = [item for sublist in crashProbsArrayOlegBaselineWithRounding for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimesWithRounding, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArrayWithRounding = []
        for col in row:
            tempRunTimesArrayWithRounding.append(float(col)/1000000000)
        runTimesArrayOlegBaselineWithRounding.append(tempRunTimesArrayWithRounding)
    runTimesArrayOlegBaselineWithRoundingFlat = [item for sublist in runTimesArrayOlegBaselineWithRounding for item in sublist]



if(showBaselineWithRounding):
    crashProbsArrayBaselineWithRounding = []
    runTimesArrayBaselineWithRounding = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\crashProbsBaseline.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\runTimesBaseline.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayBaselineWithRounding.append(tempCrashProbsArray)
    crashProbsArrayBaselineWithRoundingFlat = [item for sublist in crashProbsArrayBaselineWithRounding for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayBaselineWithRounding.append(tempRunTimesArray)
    runTimesArrayBaselineWithRoundingFlat = [item for sublist in runTimesArrayBaselineWithRounding for item in sublist]



if(showExactBaseline):
    crashProbsArrayExactBaseline = []
    runTimesArrayExactBaseline = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\crashProbsExactBaseline.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\runTimesExactBaseline.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayExactBaseline.append(tempCrashProbsArray)
    crashProbsArrayExactBaselineFlat = [item for sublist in crashProbsArrayExactBaseline for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayExactBaseline.append(tempRunTimesArray)
    runTimesArrayExactBaselineFlat = [item for sublist in runTimesArrayExactBaseline for item in sublist]


if(showLattice):
    crashProbsArrayLattice = []
    runTimesArrayLattice = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\crashProbsLatticeN3H3L3d15.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\runTimesLatticeN3H3L3d15.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayLattice.append(tempCrashProbsArray)
    crashProbsArrayLatticeFlat = [item for sublist in crashProbsArrayLattice for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayLattice.append(tempRunTimesArray)
    runTimesArrayLatticeFlat = [item for sublist in runTimesArrayLattice for item in sublist]


if(showRamneetKN):
    crashProbsArrayRamneetKandN = []
    runTimesArrayRamneetKandN = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\temp\\crashProbsRamneetKandNm3.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\scalabilityAnalysis\\data\\temp\\runTimesRamneetKandNm3.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayRamneetKandN.append(tempCrashProbsArray)
    crashProbsArrayRamneetKandNFlat = [item for sublist in crashProbsArrayRamneetKandN for item in sublist]

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayRamneetKandN.append(tempRunTimesArray)
    runTimesArrayRamneetKandNFlat = [item for sublist in runTimesArrayRamneetKandN for item in sublist]


ax = plt.axes(projection='3d')
if(showOlegBaseline):
    ax.scatter3D(YSmall, XSmall, crashProbsArrayOlegBaseline, color='purple')
if(showOlegBaselineWithRounding):
    ax.scatter3D(Y, X, crashProbsArrayOlegBaselineWithRounding, color='cyan')
if(showExactBaseline):
    ax.scatter3D(Y, X, crashProbsArrayExactBaseline, color='black')
if(showBaselineWithRounding):
    ax.scatter3D(Y, X, crashProbsArrayBaselineWithRounding, color='green')
if(showLattice):
    ax.scatter3D(Y, X, crashProbsArrayLattice, color='red')
if(showRamneetKN):
    ax.scatter3D(Y, X, crashProbsArrayRamneetKandN, color='blue')

plt.xlabel('Initial Distance (m)',fontsize=12)
plt.ylabel('Initial Speed (m/s)',fontsize=12)
ax.set_zlabel('Crash Chance',fontsize=12)
# plt.zlabel('Crash Chance')
# plt.title('Computed Crash Probabilities')
plt.show()

print(min(min(runTimesArrayOlegBaseline)))
print(min(min(runTimesArrayOlegBaselineWithRounding)))
print(min(min(runTimesArrayExactBaseline)))
print(min(min(runTimesArrayBaselineWithRounding)))
print(min(min(runTimesArrayLattice)))
print(min(min(runTimesArrayRamneetKandN)))

ax2 = plt.axes(projection='3d')
if(showOlegBaseline):
    ax2.scatter3D(YSmall, XSmall, np.log10(runTimesArrayOlegBaseline), color='purple')
if(showOlegBaselineWithRounding):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayOlegBaselineWithRounding), color='cyan')
if(showExactBaseline):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayExactBaseline), color='black')
if(showBaselineWithRounding):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayBaselineWithRounding), color='green')
if(showLattice):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayLattice), color='red')
if(showRamneetKN):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayRamneetKandN), color='blue')
# ax2.set_zlim(0.001,5000)
# if(useLogScale):
#     ax2.zaxis.set_scale('log')
plt.xlabel('Initial Distance (m)',fontsize=12)
plt.ylabel('Initial Speed (m/s)',fontsize=12)
ax2.set_zlabel('Runtime (log(s))',fontsize=12)
# plt.zlabel('Crash Chance')
# plt.title('Model Checking Runtimes')
plt.show()