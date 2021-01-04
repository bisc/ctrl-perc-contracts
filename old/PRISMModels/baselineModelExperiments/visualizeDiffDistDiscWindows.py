import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt


##############################
## N5 H5
##############################
N=5
H=
L=3
distDiscsArray = []
crashProbsArray = []
runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsH' + str(H) + 'L' + str(L) + 'Temp.csv')
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
    plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
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
resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDs\\resultsTemp.csv')
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
    plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
plt.show()

# ##############################
# ## N5 H3
# ##############################

# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscs\\diffDistDiscresultsN5H3.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='red')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# #plt.gca().invert_xaxis()
# axes = plt.gca()
# axes.set_ylim([0,1])
# plt.xlabel('Runtime (s)')
# plt.ylabel('P(crash)')
# plt.title('N=5,H=3: PRISM Result Different Model Discretizations')
# # plt.show()




# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N5H3\\diffDeltaDs\\results.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='blue')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# plt.show()

# #########################################
# ## N=3,H3
# #########################################


# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscs\\diffDistDiscresultsN3H3.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='red')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# #plt.gca().invert_xaxis()
# axes = plt.gca()
# axes.set_ylim([0,1])
# plt.xlabel('Runtime (s)')
# plt.ylabel('P(crash)')
# plt.title('N=3,H=2: PRISM Result Different Model Discretizations')
# # plt.show()


# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N3\\diffDeltaDs\\results.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='blue')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# plt.show()



# #########################################
# ## N=3,H2
# #########################################

# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscs\\diffDistDiscresultsN3H2.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='red')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# #plt.gca().invert_xaxis()
# axes = plt.gca()
# axes.set_ylim([0,1])
# plt.xlabel('Runtime (s)')
# plt.ylabel('P(crash)')
# plt.title('N=3,H=2: PRISM Result Different Model Discretizations')
# # plt.show()


# distDiscsArray = []
# crashProbsArray = []
# runTimesArray = []

# resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N3H2\\diffDeltaDs\\results.csv')
# csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
# firstIterFlag=True
# for row in csv_reader_probs_array:
#     if(firstIterFlag):
#         firstIterFlag=False
#         continue
#     distDiscsArray.append(float(row[0]))
#     crashProbsArray.append(float(row[1]))
#     runTimesArray.append(float(row[2])/1000000000)


# print(distDiscsArray)
# print(crashProbsArray)
# print(runTimesArray)

# plt.scatter(runTimesArray,crashProbsArray,color='blue')

# for i in range(len(runTimesArray)):
#     label = str(distDiscsArray[i])
#     plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
# plt.show()



