import numpy as np
import csv
import math
import random

N = 1
M = 3
L = 3

# latticeDistDiscs = (0.75, 1, 1.25, 1.5,1.75)
latticeDistDiscs = [0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.65, 1.7, 1.75, 1.8, 1.9, 2]
# latticeDistDiscs = [1.8,1.9]
# latticeDistDiscs = [1.25]
# latticeDistDiscs = [1.45, 1.55, 1.6, 1.65]

for latticeDistDisc in latticeDistDiscs:

    probsArray = []
    probsFile = open('N' + str(N) + '/avgProbPerBinPerLen.csv')
    csv_reader_probs_array = csv.reader(probsFile, delimiter=',')
    for row in csv_reader_probs_array:
        tempProbArray = []
        for prob in row:
            tempProbArray.append(float(prob))
        probsArray.append(tempProbArray)


    probsHists = []
    probsHistLenFile = open('N' + str(N) + '/historyLengthByBin.csv')
    csv_reader_hist_lens = csv.reader(probsHistLenFile, delimiter=',')
    for row in csv_reader_hist_lens:
        probsHists.append(float(row[0]))

    # print(probsHists)
    # print(probsArray)

    probsArrayInd = 0


    # outfile = open('N' + str(N) + '/miscTesting.txt', 'w')
    modelfile = open('latticeWindowedModels/windowedBoBLatticeMajVoteFilter-N' + str(N) + 'M' + str(M) + 'L' + str(L) + '-deltaD' + str(latticeDistDisc) + '.prism', 'w')
    # distIndUpper = 43
    # distIndLower = 43
    LECModelDistDisc = 10
    Nmax = max(N,M) #Use LEC step size of 10

    for binInd in range(len(probsHists)):
        distLower = (binInd)*LECModelDistDisc
        distUpper = (binInd+1)*(LECModelDistDisc)
        distIndLower = math.floor(distLower/latticeDistDisc)+1
        distIndUpper = math.floor(distUpper/latticeDistDisc)+1

        currHistLen = int(probsHists[binInd])
        lookBackLen = max(M-1,currHistLen)
        print(currHistLen)
        for prevSIter in range(0,2**lookBackLen):
            s1 = 1-(prevSIter % 2)
            s2 = 1-(math.floor((prevSIter/2)) % 2)
            s3 = 1-(math.floor((prevSIter/4)) % 2)
            s4 = 1-(math.floor((prevSIter/8)) % 2)
            s5 = 1-(math.floor((prevSIter/16)) % 2)
            s6 = 1-(math.floor((prevSIter/32)) % 2)

            if(lookBackLen==7):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + "&s4=" + str(s4) + "&s5=" + str(s5) + "&s6=" + str(s6) + "&s7=" + str(s7) + " -> "
            if(lookBackLen==6):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + "&s4=" + str(s4) + "&s5=" + str(s5) + "&s6=" + str(s6) + " -> "
            if(lookBackLen==3):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + " -> "
            if(lookBackLen==5):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + "&s4=" + str(s4) + "&s5=" + str(s5) + " -> "
            if(lookBackLen==4):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + "&s4=" + str(s4) + " -> "
            if(lookBackLen==2):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + " -> "

            modelfile.write(modelLine)
            if(currHistLen==0):
                p = probsArray[probsArrayInd][0]
                provsVars = ("p111","p110","p101","p100","p011","p010","p001","p000")
                probs = [p,p,p,p,p,p,p,p]
            elif(currHistLen==1):
                p0 = probsArray[probsArrayInd+1][0]
                p1 = probsArray[probsArrayInd+1][1]
                probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000")
                probs = (p1,p0,p1,p0,p1,p0,p1,p0)
            elif(currHistLen==2):
                p00 = probsArray[probsArrayInd+2][0]
                p01 = probsArray[probsArrayInd+2][1]
                p10 = probsArray[probsArrayInd+2][2]
                p11 = probsArray[probsArrayInd+2][3]
                probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000")
                probs = (p11,p10,p01,p00,p11,p10,p01,p00)
            elif(currHistLen==3):
                p000 = probsArray[probsArrayInd+3][0]
                p001 = probsArray[probsArrayInd+3][1]
                p010 = probsArray[probsArrayInd+3][2]
                p011 = probsArray[probsArrayInd+3][3]
                p100 = probsArray[probsArrayInd+3][4]
                p101 = probsArray[probsArrayInd+3][5]
                p110 = probsArray[probsArrayInd+3][6]
                p111 = probsArray[probsArrayInd+3][7]
                probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000")
                probs = (p111,p110,p101,p100,p011,p010,p001,p000)
            else:
                raise ValueError('This code only handles histories up to length 3')
            
            if(lookBackLen==7):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s7) + str(1-s6) + str(1-s5) + str(1-s4) + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'
            if(lookBackLen==6):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s6) + str(1-s5) + str(1-s4) + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'
            if(lookBackLen==5):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s5) + str(1-s4) + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'
            if(lookBackLen==3):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'
            if(lookBackLen==4):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s4) + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'
            if(lookBackLen==2):
                fileName = 'windowed/k-l-m-bob2-maj/N' + str(N) + 'M' + str(M) + '/probsBoB-N' + str(N) + '-M' + str(M) + '-L' + str(3) + '-init' + str(1-s3) + str(1-s2) + str(1-s1) + '.csv'

            outProbSum=0
            with open(fileName) as eqns_csv_file:
                csv_reader = csv.reader(eqns_csv_file, delimiter=',')
                rowiter = 0
                firstWrite = True
                for row in csv_reader:
                    coliter = 0
                    colIterMax = len(row)-1
                    for col in row:
                        s1Next = 1-(coliter % 2)
                        s2Next = 1-(math.floor((coliter/2)) % 2)
                        s3Next = 1-(math.floor((coliter/4)) % 2)
                        s4Next = 1-(math.floor((coliter/8)) % 2)
                        s5Next = 1-(math.floor((coliter/16)) % 2)
                        s6Next = 1-(math.floor((coliter/32)) % 2)

                        for i in range(len(probs)):
                            strToReplace = probsVars[i]
                            strToReplaceVal = probs[i]
                            col = col.replace(strToReplace,str(strToReplaceVal))

                        col = col.replace("^","**")
                        outProbSum+=eval(col)

                        detProb = eval(col)
                        if(rowiter==math.floor(Nmax/2) and coliter==colIterMax):
                            if(not detProb==0):
                                if(lookBackLen==5):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ");\n"
                                if(lookBackLen==7):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ")&(s7'=" + str(s7Next) + ");\n"
                                if(lookBackLen==6):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ");\n"
                                if(lookBackLen==3):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ");\n"
                                if(lookBackLen==4):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ");\n"
                                if(lookBackLen==2):
                                    modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ");\n"

                            else:
                                modelLine = ';\n'
                        else:
                            if(not detProb==0):
                                if(firstWrite):
                                    if(lookBackLen==5):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")"
                                    if(lookBackLen==7):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ")&(s7'=" + str(s7Next) + ")"
                                    if(lookBackLen==6):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ")"
                                    if(lookBackLen==3):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")"
                                    if(lookBackLen==4):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")"
                                    if(lookBackLen==2):
                                        modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")"

                                    firstWrite = False
                                else:
                                    if(lookBackLen==5):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")"
                                    if(lookBackLen==7):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ")&(s7'=" + str(s7Next) + ")"
                                    if(lookBackLen==6):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")&(s5'=" + str(s5Next) + ")&(s6'=" + str(s6Next) + ")"
                                    if(lookBackLen==3):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")"
                                    if(lookBackLen==4):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")&(s4'=" + str(s4Next) + ")"
                                    if(lookBackLen==2):
                                        modelLine = "+" + str(detProb) + ":(currN'=1)&(currK'=" + str(2*rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")"

                            else:
                                modelLine=""
                        modelfile.write(modelLine)
                        coliter+=1

                    rowiter+=1
            print(outProbSum)
        
        probsArrayInd+=int(currHistLen)+1
        # print(probsArrayInd)
    modelfile.close()
