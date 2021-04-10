import numpy as np
import csv
import math

modelName = 'modelTestTestTestSimData.prism'

f1 = open(modelName,"w")

maxWl = 100
wls = range(1,maxWl+1)
numTanks = 2

for wl in wls:
    ts = 101
    inf = 13
    of = 4
    ut = 80
    ew = 4

    LECModelStrings = ['p[min]','p[max]','p[-10]','p[-9]','p[-8]','p[-7]','p[-6]','p[-5]','p[-4]','p[-3]','p[-2]','p[-1]','p[0]','p[1]','p[2]','p[3]','p[4]','p[5]','p[6]','p[7]','p[8]','p[9]','p[10]']
    LECModel = [0.3801,0.3743,0,0,0,0,0.0184,0.0198,0.0181,0.0190,0.0179,0.0215,0.0176,0.0219,0.0174,0.0200,0.0193,0.0162,0.0185,0,0,0,0]
    # print(sum(LECModel))


    fileName = 'tankstepprobs_ts' + str(ts) + '_isos' + str(inf) + str(of) + '_ew' + str(ew) + '/stepdistr_wl' + str(wl) + '_ts' + str(ts) + '_isos' + str(inf) + str(of) + '_ut' + str(ut) + '_ew' + str(ew) + '.txt'
    print(fileName)

    tempProbs = []
    with open(fileName,'r') as f:
        Lines = f.readlines()
        for line in Lines:
            # print(line)
            # print('a')
            tempLine = line
            for i in range(len(LECModel)):
                strToRep = LECModelStrings[i]
                tempProb = LECModel[i]
                tempLine = tempLine.replace(strToRep,str(tempProb))
            tempLine= tempLine.replace("^","**")
            tempLine = tempLine.strip('\n')
            # print(tempLine)
            # print(eval(tempLine))
            tempProbs.append(eval(tempLine))
    print(sum(tempProbs))
    for i in range(1,numTanks+1):
        # print('    [] currN=0&tankFlag=' + str(i) + '&wl' + str(i) + '=' + str(wl) + ' -> ')
        f1.write('    [] currN=1&contAction' + str(i) + '=1&wl' + str(i) + '=' + str(wl) + '&sink=0 -> ')

        for j in range(0,len(tempProbs)):
            prob = tempProbs[j]
            if j==0:
                if prob==0:
                    probScalar=1
                else:
                    probScalar=1/(1-prob)
                print(prob)
                print(probScalar)
                continue
            steps = max(1,j)
            if(j==0):
                contAction=0
            else:
                contAction=1
            if(i==numTanks):
                dagera=1
                if(j==len(tempProbs)-1):
                    # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1);")
                    # f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1);\n")
                    f1.write(str(prob*probScalar) + ":(sink'=1);\n")
                else:
                    # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1) + ")
                    f1.write(str(prob*probScalar) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps1'=" + str(steps) + ")&(numSteps2'=" + str(steps) + ")&(tankFlag'=1)&(currN'=2) + ")
            else:
                if(j==len(tempProbs)-1):
                    # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ");")
                    # f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ");\n")
                    f1.write(str(prob*probScalar) + ":(sink'=1);\n")
                else:
                    # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ") + ")
                    f1.write(str(prob*probScalar) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps1'=" + str(steps) + ")&(numSteps2'=" + str(steps) + ")&(tankFlag'=1)&(currN'=2) + ")
    # break
            # print('b')

            