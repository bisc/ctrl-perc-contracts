import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt


##############################
## N5 H5
##############################

showOlegBaseline=True
showOlegBaselineWithPartialOrdering=True

if(showOlegBaseline):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSNoRoundingResultsInitCond1.csv')
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
    # axes.set_ylim([0,1])
    plt.xlabel('Runtime (s)')
    plt.ylabel('P(crash)')
    plt.title('Accuracy v. Runtime for Different Models')
    # plt.show()


if(showOlegBaselineWithPartialOrdering):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSWithRoundingResultsInitCond1.csv')

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