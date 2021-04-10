import numpy as np
import matplotlib.pyplot as plt


import csv

folderName = 'singleTankEx/'
crashProbs = []
runTimes = []

# waterLevels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
waterLevels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
# waterLevels = [1,10,15,30,40,46,48]
# waterLevels = [1,3,5,10,15,20,25,30,35,40,45,47,49]
extraString = 'BadPerception_initCont1'


with open(folderName + 'crashProbs' + extraString + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        for prob in row:
            crashProbs.append(float(prob))

with open(folderName + 'runTimes' + extraString + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        for time in row:
            runTimes.append(float(time))

print(crashProbs)
plt.plot(waterLevels,crashProbs)
plt.title('Simple Water Tank Crash Probs')
plt.ylim((0,1))
plt.savefig(folderName + 'crashProbs' + extraString + '.png')
plt.clf()


plt.plot(waterLevels,runTimes)
plt.title('Simple Water Tank Run Times')
plt.savefig(folderName + 'runTimes' + extraString + '.png')
plt.clf()




# crashProbsOverflow = []
# runTimesOverflow = []

# with open('singleTankEx/crashProbsOverflow' + extraString + '.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         for prob in row:
#             crashProbsOverflow.append(float(prob))

# with open('singleTankEx/runTimesOverflow' + extraString + '.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         for time in row:
#             runTimesOverflow.append(float(time))

# print(crashProbsOverflow)
# plt.plot(waterLevels,crashProbsOverflow)
# plt.title('Simple Water Tank Crash Probs')
# # plt.ylim((0,1))
# plt.savefig('singleTankEx/crashProbsOverflow' + extraString + '.png')
# plt.clf()


# plt.plot(waterLevels,runTimesOverflow)
# plt.title('Simple Water Tank Run Times')
# plt.savefig('singleTankEx/runTimesOverflow' + extraString + '.png')
# plt.clf()



# crashProbsUnderflow = []
# runTimesUnderflow = []

# with open('singleTankEx/crashProbsUnderflow' + extraString + '.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         for prob in row:
#             crashProbsUnderflow.append(float(prob))

# with open('singleTankEx/runTimesUnderflow' + extraString + '.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         for time in row:
#             runTimesUnderflow.append(float(time))

# print(crashProbsUnderflow)
# plt.plot(waterLevels,crashProbsUnderflow)
# plt.title('Simple Water Tank Crash Probs')
# # plt.ylim((0,1))
# plt.savefig('singleTankEx/crashProbsUnderflow' + extraString + '.png')
# plt.clf()


# plt.plot(waterLevels,runTimesUnderflow)
# plt.title('Simple Water Tank Run Times')
# plt.savefig('singleTankEx/runTimesUnderflow' + extraString + '.png')
# plt.clf()
