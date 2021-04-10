import numpy as np
import csv
import math
import random

latticeDistDiscs = (0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2)

for latticeDistDisc in latticeDistDiscs:
    N = 3

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

    print(probsHists)
    print(probsArray)

    probsArrayInd = 0


    modelfile = open('N' + str(N) + '/diffDistDiscs/miscModelTestingPrevDetsH3N' + str(N) + 'd' + str(latticeDistDisc) + '.txt', 'w')
    distIndUpper = 43
    distIndLower = 43
    LECModelDistDisc = 10
    Nmax = N #Use LEC step size of 10

    for binInd in range(len(probsHists)):
        distLower = (binInd)*LECModelDistDisc
        distUpper = (binInd+1)*(LECModelDistDisc)
        distIndLower = math.floor(distLower/latticeDistDisc)+1
        distIndUpper = math.floor(distUpper/latticeDistDisc)+1

        currHistLen = int(probsHists[binInd])
        print(currHistLen)
        for prevSIter in range(0,2**currHistLen):
            s1 = 1-(prevSIter % 2)
            s2 = 1-(math.floor((prevSIter/2)) % 2)
            s3 = 1-(math.floor((prevSIter/4)) % 2)

            if(currHistLen==0):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> "
            elif(currHistLen==1):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + " -> "
            elif(currHistLen==2):
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + " -> "
            else:
                modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + "&s=" + str(s1) + "&s2=" + str(s2) + "&s3=" + str(s3) + " -> "
            modelfile.write(modelLine)

            probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000","p11","p10","p01","p00","p1","p0","p")

            ## set probs vals according to historyLen
            #probs = (0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5)
            if(currHistLen==0):
                p = probsArray[probsArrayInd][0]
                probs = (p,p,p,p,p,p,p,p,p,p,p,p,p,p,p)
            elif(currHistLen==1):
                # p = probsArray[probsArrayInd][0]
                p0 = probsArray[probsArrayInd+1][0]
                p1 = probsArray[probsArrayInd+1][1]
                if(s1==1):
                    p=p0
                else:
                    p=p1
                probs = (p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p)
            elif(currHistLen==2):
                # p = probsArray[probsArrayInd][0]
                # p0 = probsArray[probsArrayInd+1][0]
                # p1 = probsArray[probsArrayInd+1][1]
                p00 = probsArray[probsArrayInd+2][0]
                p01 = probsArray[probsArrayInd+2][1]
                p10 = probsArray[probsArrayInd+2][2]
                p11 = probsArray[probsArrayInd+2][3]
                if(s2==1 and s1==1):
                    p=p00
                    p0=p00
                    p1=p01
                elif(s2==1 and s1==0):
                    p=p01
                    p0=p10
                    p1=p11
                elif(s2==0 and s1==1):
                    p=p10
                    p0=p00
                    p1=p01
                elif(s2==0 and s1==0):
                    p=p11
                    p0=p10
                    p1=p11
                probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p1,p0,p)
            elif(currHistLen==3):
                p = probsArray[probsArrayInd][0]
                p0 = probsArray[probsArrayInd+1][0]
                p1 = probsArray[probsArrayInd+1][1]
                p00 = probsArray[probsArrayInd+2][0]
                p01 = probsArray[probsArrayInd+2][1]
                p10 = probsArray[probsArrayInd+2][2]
                p11 = probsArray[probsArrayInd+2][3]
                p000 = probsArray[probsArrayInd+3][0]
                p001 = probsArray[probsArrayInd+3][1]
                p010 = probsArray[probsArrayInd+3][2]
                p011 = probsArray[probsArrayInd+3][3]
                p100 = probsArray[probsArrayInd+3][4]
                p101 = probsArray[probsArrayInd+3][5]
                p110 = probsArray[probsArrayInd+3][6]
                p111 = probsArray[probsArrayInd+3][7]
                if(s3==1 and s2==1 and s1==1):
                    p=p000
                    p0=p000
                    p1=p001
                    p00=p000
                    p01=p001
                    p10=p010
                    p11=p011
                elif(s3==1 and s2==1 and s1==0):
                    p=p001
                    p0=p010
                    p1=p011
                    p00=p100
                    p01=p101
                    p10=p110
                    p11=p111
                elif(s3==1 and s2==0 and s1==1):
                    p=p010
                    p0=p100
                    p1=p101
                    p00=p000
                    p01=p001
                    p10=p010
                    p11=p011
                elif(s3==1 and s2==0 and s1==0):
                    p=p011
                    p0=p110
                    p1=p111
                    p00=p100
                    p01=p101
                    p10=p110
                    p11=p111
                elif(s3==0 and s2==1 and s1==1):
                    p=p100
                    p0=p000
                    p1=p001
                    p00=p000
                    p01=p001
                    p10=p010
                    p11=p011
                elif(s3==0 and s2==1 and s1==0):
                    p=p101
                    p0=p010
                    p1=p011
                    p00=p100
                    p01=p101
                    p10=p110
                    p11=p111
                elif(s3==0 and s2==0 and s1==1):
                    p=p110
                    p0=p100
                    p1=p101
                    p00=p000
                    p01=p001
                    p10=p010
                    p11=p011
                elif(s3==0 and s2==0 and s1==0):
                    p=p111
                    p0=p110
                    p1=p111
                    p00=p100
                    p01=p110
                    p10=p110
                    p11=p111
                # probs = (p111,p110,p101,p100,p011,p010,p001,p000,p11,p10,p01,p00,p1,p0,p)
                probs = (p111,p110,p101,p100,p011,p010,p001,p000,p11,p10,p01,p00,p1,p0,p)
                # probs = (p111,p110,p101,p100,p011,p010,p001,p000,p011,p010,p001,p000,p001,p000,p000)
                #probsArrayInd+=4
            else:
                raise ValueError('This code only handles histories up to length 3')


            outProbSum=0
            with open('N' + str(N) + '/probsH3-N' + str(N) + '-L3.csv') as eqns_csv_file:
                csv_reader = csv.reader(eqns_csv_file, delimiter=',')
                rowiter = 0
                for row in csv_reader:
                    coliter = 0
                    colIterMax = len(row)-1
                    for col in row:
                        s1Next = 1-(coliter % 2)
                        s2Next = 1-(math.floor((coliter/2)) % 2)
                        s3Next = 1-(math.floor((coliter/4)) % 2)

                        for i in range(len(probs)):
                            strToReplace = probsVars[i]
                            strToReplaceVal = probs[i]
                            col = col.replace(strToReplace,str(strToReplaceVal))

                        col = col.replace("^","**")
                        outProbSum+=eval(col)

                        detProb = eval(col)
                        if(rowiter==Nmax and coliter==colIterMax):
                            modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ");\n"
                        else:
                            if(not detProb==0):
                                modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(rowiter) + ")&(s'=" + str(s1Next) + ")&(s2'=" + str(s2Next) + ")&(s3'=" + str(s3Next) + ")+"
                            else:
                                modelLine=""
                        modelfile.write(modelLine)
                        coliter+=1

                    rowiter+=1
            # print(outProbSum)
        
        probsArrayInd+=int(currHistLen)+1
        # print(probsArrayInd)
    modelfile.close()
