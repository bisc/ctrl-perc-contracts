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

    resultsFileCrashProbs = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_EMSOFT\\data\\singleTank\\crashProbsSingleTankBaseline.csv')
    resultsFileRunTimes = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_EMSOFT\\data\\singleTank\\runTimesSingleTankBaseline.csv')

    csv_reader_probs_array = csv.reader(resultsFileCrashProbs, delimiter=',')
    for row in csv_reader_probs_array:
        for col in row:
            crashProbsArrayOlegBaseline.append(float(col))

    csv_reading_run_times = csv.reader(resultsFileRunTimes, delimiter=',')
    for row in csv_reading_run_times:
        for col in row:
            runTimesArrayOlegBaseline.append(float(col)/1000000000)

print(crashProbsArrayOlegBaseline)


waterLevels = np.arange(1,101,1)

plt.plot(waterLevels,crashProbsArrayOlegBaseline[1:])
plt.xlabel('Initial Water Level',fontsize=12)
plt.ylabel('Crash Chance',fontsize=12)
plt.show()

