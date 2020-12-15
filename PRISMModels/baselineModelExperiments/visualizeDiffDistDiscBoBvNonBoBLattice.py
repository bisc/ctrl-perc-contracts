import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt


##############################
## N5 H5
##############################
N=5
H=4
L=3
distDiscsArray = []
crashProbsArray = []
runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + 'AllVote\\diffDeltaDsBoBLattice\\resultsTemp.csv')
csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
firstIterFlag=True
for row in csv_reader_probs_array:
    if(firstIterFlag):
        firstIterFlag=False
        continue
    distDiscsArray.append(float(row[0]))
    crashProbsArray.append(float(row[1]))
    runTimesArray.append(float(row[2])/1000000000)


print(distDiscsArray)
print(crashProbsArray)
print(runTimesArray)

plt.scatter(runTimesArray,crashProbsArray,color='red')

for i in range(len(runTimesArray)):
    label = str(distDiscsArray[i])
    # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
#plt.gca().invert_xaxis()
axes = plt.gca()
axes.set_ylim([0,1])
plt.xlabel('Runtime (s)')
plt.ylabel('P(crash)')
plt.title('N=' + str(N) + ',H=' + str(H) + ': PRISM Result Different Model Discretizations')
# plt.show()


distDiscsArray = []
crashProbsArray = []
runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + '\\diffDeltaDs\\results.csv')
resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + 'AllVote\\diffDeltaDs\\resultsTemp.csv')
csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
firstIterFlag=True
for row in csv_reader_probs_array:
    if(firstIterFlag):
        firstIterFlag=False
        continue
    distDiscsArray.append(float(row[0]))
    crashProbsArray.append(float(row[1]))
    runTimesArray.append(float(row[2])/1000000000)


print(distDiscsArray)
print(crashProbsArray)
print(runTimesArray)

plt.scatter(runTimesArray,crashProbsArray,color='blue')

for i in range(len(runTimesArray)):
    label = str(distDiscsArray[i])
    # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# plt.show()



distDiscsArray = []
crashProbsArray = []
runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsAllVoteFilterH' + str(H) + 'L' + str(L) + 'Temp.csv')
csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
firstIterFlag=True
for row in csv_reader_probs_array:
    if(firstIterFlag):
        firstIterFlag=False
        continue
    distDiscsArray.append(float(row[0]))
    crashProbsArray.append(float(row[1]))
    runTimesArray.append(float(row[2])/1000000000)


print(distDiscsArray)
print(crashProbsArray)
print(runTimesArray)

plt.scatter(runTimesArray,crashProbsArray,color='green')

for i in range(len(runTimesArray)):
    label = str(distDiscsArray[i])
    # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
#plt.gca().invert_xaxis()
axes = plt.gca()
axes.set_ylim([0,1])
plt.xlabel('Runtime (s)')
plt.ylabel('P(crash)')
plt.title('N=' + str(N) + ',H=' + str(H) + ': PRISM Result Different Model Discretizations')
plt.show()