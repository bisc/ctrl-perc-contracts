import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


##############################
## N5 H5
##############################

showOlegBaseline=True
showOlegBaselineWithRounding=True
showBundledLEC=True


showBaseline=True
showOlegBaselineStateTrimming=True
showBundledLEC=True

if(showBaseline):
    crashProbsArrayOlegBaseline = []
    runTimesArrayOlegBaseline = []

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_EMSOFT\\data\\crashProbsTwoTankOlegBaseline.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_EMSOFT\\data\\runTimesTwoTankOlegBaseline.csv')

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

print(crashProbsArrayOlegBaseline)

# x = np.arange(0, 25, 1)
# y = np.arange(0, 25, 1)
# x, y = np.meshgrid(x, y)
# z = x + y

# print(z)
## Plot the percent drop in crash chance
waterLevels = [10,20,30,40,50,60,70,80,90]
X,Y = np.meshgrid(waterLevels,waterLevels)


ax = plt.axes(projection='3d')
if(showBaseline):
    ax.scatter3D(Y, X, crashProbsArrayOlegBaseline, color='black')
    # ax.plot_surface(Y,X,crashProbsArrayOlegBaseline)

plt.xlabel('Tank 1 Initial Water Level',fontsize=12)
plt.ylabel('Tank 2 Initial Water Level',fontsize=12)
ax.set_zlabel('Crash Chance',fontsize=12)
# plt.zlabel('Crash Chance')
# plt.title('Computed Crash Probabilities')
plt.show()


ax2 = plt.axes(projection='3d')
if(showBaseline):
    ax2.scatter3D(Y, X, np.log10(runTimesArrayOlegBaseline), color='black')

# ax2.set_zlim(0.001,5000)
# if(useLogScale):
#     ax2.zaxis.set_scale('log')
plt.xlabel('Tank 1 Initial Water Level',fontsize=12)
plt.ylabel('Tank 2 Initial Water Level',fontsize=12)
ax2.set_zlabel('Runtime (log(s))',fontsize=12)
# plt.zlabel('Crash Chance')
# plt.title('Model Checking Runtimes')
plt.show()