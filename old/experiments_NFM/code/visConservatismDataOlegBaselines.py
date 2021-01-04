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


if(showOlegBaseline):
    crashProbsArrayOlegBaseline = []
    runTimesArrayOlegBaseline = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\crashOlegBaselineNoRounding.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\runTimesOlegBaselineNoRounding.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayOlegBaseline.append(tempCrashProbsArray)

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayOlegBaseline.append(tempRunTimesArray)


if(showOlegBaselineWithRounding):
    crashProbsArrayOlegBaselineWithRounding = []
    runTimesArrayOlegBaselineWithRounding = []

    resultsFileCrashProbsWithRounding = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\crashOlegBaselineWithRounding.csv')
    resultsFileRunTimesWithRounding = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\runTimesOlegBaselineWithRounding.csv')

    csv_reader_probs_arrayWithRounding = csv.reader(resultsFileCrashProbsWithRounding, delimiter=',')
    for row in csv_reader_probs_arrayWithRounding:
        tempCrashProbsArrayWithRounding = []
        for col in row:
            tempCrashProbsArrayWithRounding.append(float(col))
        crashProbsArrayOlegBaselineWithRounding.append(tempCrashProbsArrayWithRounding)

    csv_reading_run_timesWithRounding = csv.reader(resultsFileRunTimesWithRounding, delimiter=',')
    for row in csv_reading_run_timesWithRounding:
        tempRunTimesArrayWithRounding = []
        for col in row:
            tempRunTimesArrayWithRounding.append(float(col)/1000000000)
        runTimesArrayOlegBaselineWithRounding.append(tempRunTimesArrayWithRounding)



if(showExactBaseline):
    crashProbsArrayExactBaseline = []
    runTimesArrayExactBaseline = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\crashProbsExactBaseline.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\data\\runTimesExactBaseline.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        tempCrashProbsArray = []
        for col in row:
            tempCrashProbsArray.append(float(col))
        crashProbsArrayExactBaseline.append(tempCrashProbsArray)

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        tempRunTimesArray = []
        for col in row:
            tempRunTimesArray.append(float(col)/1000000000)
        runTimesArrayExactBaseline.append(tempRunTimesArray)

print(crashProbsArrayOlegBaseline)
print(runTimesArrayOlegBaseline)



print(crashProbsArrayOlegBaselineWithRounding)
print(runTimesArrayOlegBaselineWithRounding)


percentLossInCrashChance = []
absoluteLossInCrashChance = []
relLossInCrashChance = []
for i,_ in enumerate(crashProbsArrayOlegBaselineWithRounding):
    temppercentLossInCrashChance = []
    tempabsoluteLossInCrashChange = []
    temprelLossInCrashChance = []
    for j,_ in enumerate(crashProbsArrayOlegBaselineWithRounding[i]):
        baselineCrashProb = crashProbsArrayOlegBaseline[i][j]
        withRoundingCrashProb = crashProbsArrayOlegBaselineWithRounding[i][j]
        exactBaselineCrashProb = crashProbsArrayExactBaseline[i][j]

        percentChange = (baselineCrashProb-withRoundingCrashProb)/(baselineCrashProb)
        temppercentLossInCrashChance.append(percentChange)

        absoluteChange = (baselineCrashProb-withRoundingCrashProb)
        tempabsoluteLossInCrashChange.append(absoluteChange)

        percentChangeRelToExact = (baselineCrashProb-withRoundingCrashProb)/(baselineCrashProb-exactBaselineCrashProb)
        temprelLossInCrashChance.append(percentChangeRelToExact)

    percentLossInCrashChance.append(temppercentLossInCrashChance)
    absoluteLossInCrashChance.append(tempabsoluteLossInCrashChange)
    relLossInCrashChance.append(temprelLossInCrashChance)


print(percentLossInCrashChance)

with open('../conservatismAnalysis/results/percentLossInCrashChanceOlegBaselines.csv', mode='w') as outfile:
    outfile_writer = csv.writer(outfile, delimiter=',')
    for row in percentLossInCrashChance:
        outfile_writer.writerow(row)

with open('../conservatismAnalysis/results/absoluteLossInCrashChanceOlegBaselines.csv', mode='w') as outfile:
    outfile_writer = csv.writer(outfile, delimiter=',')
    for row in absoluteLossInCrashChance:
        outfile_writer.writerow(row)

with open('../conservatismAnalysis/results/relativeLossInCrashChanceOlegBaselinesAndExact.csv', mode='w') as outfile:
    outfile_writer = csv.writer(outfile, delimiter=',')
    for row in relLossInCrashChance:
        outfile_writer.writerow(row)

## Plot the percent drop in crash chance
dists = [120,125,130,135,140]
speeds = [10,14,18,22,26]
X,Y = np.meshgrid(speeds,dists)

ax = plt.axes(projection='3d')
ax.scatter3D(Y, X, percentLossInCrashChance, color='black')
plt.xlabel('Initial Distance (m)')
plt.ylabel('Initial Speed (m/s)')
# plt.zlabel('Crash Chance')
plt.title('Percent Change in Crash Chance')
plt.show()


ax = plt.axes(projection='3d')
ax.scatter3D(Y, X, absoluteLossInCrashChance, color='black')
plt.xlabel('Initial Distance (m)')
plt.ylabel('Initial Speed (m/s)')
# plt.zlabel('Crash Chance')
plt.title('Absolute Change in Crash Chance')
plt.show()


ax = plt.axes(projection='3d')
ax.scatter3D(Y, X, relLossInCrashChance, color='black')
plt.xlabel('Initial Distance (m)')
plt.ylabel('Initial Speed (m/s)')
# plt.zlabel('Crash Chance')
plt.title('Relative Change in Crash Chance')
plt.show()
