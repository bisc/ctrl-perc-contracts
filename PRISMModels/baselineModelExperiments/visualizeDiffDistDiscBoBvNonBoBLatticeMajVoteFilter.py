import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from pylab import *



##############################
## N5 H5
##############################
N=3
H=3
L=3

useLogScale = True

showBoBLattice=False
showNonBoBlattice=True
showBaseline=True
showRamneetKandN=True
showInflatedBaseline=False
showNoRoundingBaseline=True
showOlegBaseline=True
showOlegBaselineWithRounding=True
showCarlaBounds=True

initCond2=False


carlaLowerBound = 4/100
carlaUpperBound = 10/100


if(showNonBoBlattice):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDsBoBLattice\\resultsTemp.csv')
    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDs\\resultsTrimmed.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDsInitCond2\\results.csv')

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

    plt.scatter(runTimesArray,crashProbsArray,color='red',marker='D')

    for i in range(len(runTimesArray)):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
    #plt.gca().invert_xaxis()
    axes = plt.gca()
    axes.set_ylim([0,1])
    # plt.xlabel('Runtime (s)')
    # plt.ylabel('P(crash)')
    # plt.title('N=' + str(N) + ',H=' + str(H) + ': Majority Voting Window')
    # plt.show()


if(showBoBLattice):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDsBoBLattice\\resultsTemp.csv')
    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDsBoBLattice\\resultsTemp.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\matlabCode\\simpleExample\\PRISMModels\\ForPaper\\windows\\N' + str(N) + 'H' + str(H) + 'L' + str(L) + '\\diffDeltaDsBoBLatticeInitCond2\\resultsTemp.csv')

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

    plt.scatter(runTimesArray,crashProbsArray,color='yellow')

    for i in range(len(runTimesArray)):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
    #plt.gca().invert_xaxis()
    axes = plt.gca()
    axes.set_ylim([0,1])
    # plt.xlabel('Runtime (s)')
    # plt.ylabel('P(crash)')
    # plt.title('N=' + str(N) + ',H=' + str(H) + ': Majority Voting Window')
    # plt.show()


if(showBaseline):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'Temp.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'TempInitCond2.csv')
    
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

    plt.scatter(runTimesArray,crashProbsArray,color='green',marker='s')

    for i in range(len(runTimesArray)):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
    #plt.gca().invert_xaxis()
    # axes = plt.gca()
    # axes.set_ylim([0,1])
    # plt.xlabel('Runtime (s)')
    # plt.ylabel('P(crash)')
    # plt.title('N=' + str(N) + ',H=' + str(H) + ': Majority Voting Window')



if(showRamneetKandN):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    if(not initCond2):
        resultsFile = open('C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\ramneetKandNExperiments\\\\pos1600.0_v200.0_m' + str(H) +  '\\\\resultsRamneetKandN.csv')
    else:
        resultsFile = open('C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\ramneetKandNExperiments\\\\pos900.0_v100.0_m' + str(H) +  '\\\\resultsRamneetKandN.csv')
    
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

    plt.scatter(runTimesArray,crashProbsArray,color='blue',marker='*',s=130)




if(showInflatedBaseline):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewInflated\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'Temp.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewInflated\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'TempInitCond2.csv')
    
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

    plt.scatter(runTimesArray,crashProbsArray,color='yellow')

    for i in range(len(runTimesArray)):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
    #plt.gca().invert_xaxis()
    # axes = plt.gca()
    # axes.set_ylim([0,1])
    # plt.xlabel('Runtime (s)')
    # plt.ylabel('P(crash)')
    # plt.title('N=' + str(N) + ',H=' + str(H) + ': Majority Voting Window')



if(showNoRoundingBaseline):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    # resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\diffDistDiscresultsN' + str(N) + 'H' + str(H) + 'Temp.csv')
    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewNoRounding\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'Temp.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewNoRounding\\diffDistDiscresultsMajVoteFilterH' + str(H) + 'L' + str(L) + 'TempInitCond2.csv')
    
    csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
    firstIterFlag=True
    for row in csv_reader_probs_array:
        if(firstIterFlag):
            firstIterFlag=False
            continue
        distDiscsArray.append(float(row[0]))
        crashProbsArray.append(float(row[1]))
        runTimesArray.append(float(row[2])/1000000000)

    crashProb = crashProbsArray[0]
    plt.hlines(y=crashProb,xmin=0,xmax=60000,color='black',linestyle="dashed")

    print(distDiscsArray)
    print(crashProbsArray)
    print(runTimesArray)

    # plt.scatter(runTimesArray,crashProbsArray,color='black')

    # for i in range(len(runTimesArray)):
    #     label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')
    #plt.gca().invert_xaxis()
    # axes = plt.gca()
    # axes.set_ylim([0,1])
    # plt.xlabel('Runtime (s)')
    # plt.ylabel('P(crash)')
    # plt.title('N=' + str(N) + ',H=' + str(H) + ': Majority Voting Window')


if(showOlegBaseline):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSNoRoundingResultsInitCond1.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSNoRoundingResultsInitCond2.csv')
    
    csv_reader_probs_array = csv.reader(resultsFile, delimiter=',')
    firstIterFlag=True
    secondIterFlag=True
    thirdIterFlag=True
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

    plt.scatter(runTimesArray[:-2],crashProbsArray[:-2],color='purple',marker='X')

    for i in range(len(runTimesArray[:-2])):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')

if(showOlegBaselineWithRounding):
    distDiscsArray = []
    crashProbsArray = []
    runTimesArray = []

    if(not initCond2):
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSWithRoundingResultsInitCond1.csv')
    else:
        resultsFile = open('C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\olegBaselineAEBSWithRoundingResultsInitCond2.csv')
    
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

    plt.scatter(runTimesArray[:-2],crashProbsArray[:-2],color='cyan',marker='.',s=150)

    for i in range(len(runTimesArray[:-2])):
        label = str(distDiscsArray[i])
        # plt.annotate(label,(runTimesArray[i],crashProbsArray[i]),textcoords="offset points", xytext=(5,5), ha='left')

ax = plt.gca()
xs = np.arange(0.05,6500,1)
if(showCarlaBounds):

    plt.hlines(y=carlaLowerBound,xmin=0,xmax=60000,color='orange',linestyle="dotted")
    plt.hlines(y=carlaUpperBound,xmin=0,xmax=60000,color='orange',linestyle="dotted")

    ax.fill_between(xs,carlaLowerBound,carlaUpperBound,color='orange',alpha=0.2)
    print(xs)




ax.set_xlim(0.05,6500)
if(useLogScale):
    ax.set_xscale('log')
plt.xlabel('Run time (s)',fontsize=20)
plt.ylabel('Crash Chance',fontsize=20)
# plt.title('Abstraction Accuracy v. Runtime Tradeoff')
plt.show()