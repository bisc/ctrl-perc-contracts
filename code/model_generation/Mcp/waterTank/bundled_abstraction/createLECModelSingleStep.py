import numpy as np
import csv
import math
import subprocess
import os

modelName = 'modelTestTestSimData.prism'

f1 = open(modelName,"w")
f1.write("\n\n")

maxWl = 100
wls = range(1,maxWl+1)
numTanks = 2

ts = 101
inf = 13
of = 4
lt = 20
ut = 80
ew = 6

folderName = 'nextTankProbsNoDistCheck/watertank-next-precomp_ts' + str(ts) + '_isos' + str(inf) + str(of) + '_utlt' + str(ut) + str(lt) + '_ew' + str(ew)
fileName = 'watertank-next-precomp-nodistcheck_ts' + str(ts) + '_isos' + str(inf) + str(of) + '_utlt' + str(ut) + str(lt) + '_ew' + str(ew) + '.wls'
# fileName = 'watertank-next-precomp_ts101_isos134_utlt8020_ew4.wls'

LECModelStrings = ['p[min]','p[max]','p[-10]','p[-9]','p[-8]','p[-7]','p[-6]','p[-5]','p[-4]','p[-3]','p[-2]','p[-1]','p[0]','p[1]','p[2]','p[3]','p[4]','p[5]','p[6]','p[7]','p[8]','p[9]','p[10]']
# LECModel = [0.1,0.1,0,0,0,0,0,0,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0,0,0,0,0,0]
# LECModel = [0.3801,0.3743,0,0,0,0,0.0184,0.0198,0.0181,0.0190,0.0179,0.0215,0.0176,0.0219,0.0174,0.0200,0.0193,0.0162,0.0185,0,0,0,0]

LECModel = [0.143200000000000,0.143600000000000,0,0,0,0,0.020500000000000,   0.024900000000000,   0.036800000000000,   0.053500000000000,   0.076400000000000,   0.095200000000000,   0.102800000000000,   0.093200000000000,   0.073300000000000,   0.052700000000000,   0.040700000000000,   0.023000000000000,   0.020200000000000,0,0,0,0]


for wl1 in wls:
    for wl2 in wls:

        # run file with appropriate names
        # save to temp file
        # read temp file
        # convert to prism model
        # list_files = subprocess.run(["dir"], shell=True)
        # print("The exit code was: %d" % list_files.returncode)
        savedFile = folderName + '/numTanks2_wl1_' + str(wl1) + '_wl2_' + str(wl2) + '.txt'
        with open(savedFile,'r') as f:
            tempProbs = []
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
                print(tempLine)
                print(eval(tempLine))
                tempProbs.append(eval(tempLine))
        f1.write("    [] currN=0&sink=0&wl1=" + str(wl1) + "&wl2=" + str(wl2) + " -> ")
        for k in range(len(tempProbs)):
            prob = tempProbs[k]
            tankToFill = k
            if(tankToFill==0):
                f1.write(str(prob) + ":(currN'=2)&(numSteps1'=1)&(numSteps2'=1)&(contAction1'=0)&(contAction2'=0) + ")
            elif(tankToFill==1):
                f1.write(str(prob) + ":(currN'=1)&(contAction1'=1)&(contAction2'=0) + ")
            else:
                f1.write(str(prob) + ":(currN'=1)&(contAction1'=0)&(contAction2'=1);\n")
        print(sum(tempProbs))
        # break
    # break







    # LECModelStrings = ['p[min]','p[max]','p[-10]','p[-9]','p[-8]','p[-7]','p[-6]','p[-5]','p[-4]','p[-3]','p[-2]','p[-1]','p[0]','p[1]','p[2]','p[3]','p[4]','p[5]','p[6]','p[7]','p[8]','p[9]','p[10]']
    # LECModel = [0.1,0.1,0,0,0,0,0,0,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0.8*1/9,0,0,0,0,0,0]
    # # print(sum(LECModel))


    # fileName = 'watertank-next-precomp_ts' + str(ts) + '_isos' + str(inf) + str(of) + '_utlt_' + str(ut) + str(lt) + '_ew' + str(ew) + '.wls'
    # print(fileName)
    
    # tempProbs = []
    # with open(fileName,'r') as f:
    #     Lines = f.readlines()
    #     for line in Lines:
    #         # print(line)
    #         # print('a')
    #         tempLine = line
    #         for i in range(len(LECModel)):
    #             strToRep = LECModelStrings[i]
    #             tempProb = LECModel[i]
    #             tempLine = tempLine.replace(strToRep,str(tempProb))
    #         tempLine= tempLine.replace("^","**")
    #         tempLine = tempLine.strip('\n')
    #         # print(tempLine)
    #         # print(eval(tempLine))
    #         tempProbs.append(eval(tempLine))
    # print(sum(tempProbs))
    # for i in range(1,numTanks+1):
    #     # print('    [] currN=0&tankFlag=' + str(i) + '&wl' + str(i) + '=' + str(wl) + ' -> ')
    #     f1.write('    [] currN=0&tankFlag=' + str(i) + '&wl' + str(i) + '=' + str(wl) + '&sink=0 -> ')

    #     for j in range(0,len(tempProbs)):
    #         prob = tempProbs[j]
    #         steps = max(1,j)
    #         if(j==0):
    #             contAction=0
    #         else:
    #             contAction=1
    #         if(i==numTanks):
    #             dagera=1
    #             if(j==len(tempProbs)-1):
    #                 # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1);")
    #                 # f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1);\n")
    #                 f1.write(str(prob) + ":(sink'=1);\n")
    #             else:
    #                 # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=1)&(currN'=1) + ")
    #                 f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(wlPer" + str(i) + "'=wl" + str(i) + "+" + str(steps) + ")&(tankFlag'=1)&(currN'=1) + ")
    #         else:
    #             if(j==len(tempProbs)-1):
    #                 # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ");")
    #                 # f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ");\n")
    #                 f1.write(str(prob) + ":(sink'=1);\n")
    #             else:
    #                 # print(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(tankFlag'=" + str(i+1) + ") + ")
    #                 f1.write(str(prob) + ":(contAction" + str(i) + "'=" + str(contAction) + ")&(numSteps" + str(i) + "'=" + str(steps) + ")&(wlPer" + str(i) + "'=wl" + str(i) + "+" + str(steps) + ")&(tankFlag'=" + str(i+1) + ") + ")
    # # break
    #         # print('b')

            