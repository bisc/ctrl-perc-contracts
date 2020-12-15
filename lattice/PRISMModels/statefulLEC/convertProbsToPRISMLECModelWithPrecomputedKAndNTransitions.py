import numpy as np
import csv
import math
import random

# outfile = open('miscTesting.txt', 'w')
# modelfile = open('miscModelTesting.txt', 'w')
# distIndUpper = 43
# distIndLower = 43
# modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> "
# modelfile.write(modelLine)


# probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000","p11","p10","p01","p00","p1","p0","p")
# #probs = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
# probs = (0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5)
# #probs = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
# Nmax = 10
# print(probs)
# outProbSum=0
# with open('probsH3-N10.csv') as eqns_csv_file:
#     csv_reader = csv.reader(eqns_csv_file, delimiter=',')
#     iter = 0
#     for row in csv_reader:
#         outfile.write(str(iter))
#         outfile.write("\n")
#         row=row[0]
#         outfile.write(row)
#         outfile.write("\n")


#         for i in range(len(probs)):
#             strToReplace = probsVars[i]
#             strToReplaceVal = probs[i]
#             row = row.replace(strToReplace,str(strToReplaceVal))


#         row = row.replace("^","**")
#         outfile.write(row)
#         outfile.write("\n")
#         outfile.write(str(eval(row)))
#         outProbSum+=eval(row)
#         outfile.write("\n")
#         #break
#         outfile.write("\n")
#         outfile.write("\n")
#         outfile.write("\n")

#         detProb = eval(row)
#         if(iter==Nmax):
#             modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(iter) + ");\n"
#         else:
#             modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(iter) + ") + "
#         modelfile.write(modelLine)

#         iter+=1

# print(outProbSum)
# outfile.close()
# modelfile.close()




probsArray = []
probsFile = open('avgProbPerBinPerLen.csv')
csv_reader_probs_array = csv.reader(probsFile, delimiter=',')
for row in csv_reader_probs_array:
    tempProbArray = []
    for prob in row:
        tempProbArray.append(float(prob))
    probsArray.append(tempProbArray)


probsHists = []
probsHistLenFile = open('historyLengthByBin.csv')
csv_reader_hist_lens = csv.reader(probsHistLenFile, delimiter=',')
for row in csv_reader_hist_lens:
    probsHists.append(float(row[0]))

print(probsHists)
print(probsArray)

probsArrayInd = 0


outfile = open('miscTesting.txt', 'w')
modelfile = open('miscModelTestingH3N10.txt', 'w')
distIndUpper = 43
distIndLower = 43
latticeDistDisc = 1.5
LECModelDistDisc = 10
Nmax = 10 #Use LEC step size of 10
for binInd in range(len(probsHists)):
    distLower = (binInd)*LECModelDistDisc
    distUpper = (binInd+1)*(LECModelDistDisc)
    distIndLower = math.floor(distLower/latticeDistDisc)+1
    distIndUpper = math.floor(distUpper/latticeDistDisc)+1
    modelLine = "    [] currN=0&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> "
    modelfile.write(modelLine)

    currHistLen = probsHists[binInd]
    probsVars = ("p111","p110","p101","p100","p011","p010","p001","p000","p11","p10","p01","p00","p1","p0","p")

    ## set probs vals according to historyLen
    #probs = (0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5)
    if(currHistLen==0):
        p = probsArray[probsArrayInd][0]
        probs = (p,p,p,p,p,p,p,p,p,p,p,p,p,p,p)
        probsArrayInd+=1
    elif(currHistLen==1):
        p = probsArray[probsArrayInd][0]
        p0 = probsArray[probsArrayInd+1][0]
        p1 = probsArray[probsArrayInd+1][1]
        #probs = (p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p)
        probs = (p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p1,p0,p0)
        probsArrayInd+=2
    elif(currHistLen==2):

        p = probsArray[probsArrayInd][0]
        p0 = probsArray[probsArrayInd+1][0]
        p1 = probsArray[probsArrayInd+1][1]
        p00 = probsArray[probsArrayInd+2][0]
        p01 = probsArray[probsArrayInd+2][1]
        p10 = probsArray[probsArrayInd+2][2]
        p11 = probsArray[probsArrayInd+2][3]
        # if (not binInd==11):
        #     #probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p1,p0,p)
        #     # probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p1,p0,p0)
        #     # probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p10,p00,p00)
        # else:
        #     probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p01,p00,p00)
        probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p1,p0,p0)
        # probs = (p11,p10,p01,p00,p11,p10,p01,p00,p11,p10,p01,p00,p01,p00,p00)
        probsArrayInd+=3
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
        # probs = (p111,p110,p101,p100,p011,p010,p001,p000,p11,p10,p01,p00,p1,p0,p)
        probs = (p111,p110,p101,p100,p011,p010,p001,p000,p11,p10,p01,p00,p1,p0,p0)
        # probs = (p111,p110,p101,p100,p011,p010,p001,p000,p011,p010,p001,p000,p001,p000,p000)
        probsArrayInd+=4
    else:
        raise ValueError('This code only handles histories up to length 3')



    outProbSum=0
    with open('probsH3-N10.csv') as eqns_csv_file:
        csv_reader = csv.reader(eqns_csv_file, delimiter=',')
        iter = 0
        for row in csv_reader:
            row=row[0]
            for i in range(len(probs)):
                strToReplace = probsVars[i]
                strToReplaceVal = probs[i]
                row = row.replace(strToReplace,str(strToReplaceVal))

            row = row.replace("^","**")
            outfile.write(row)
            outfile.write("\n")
            outfile.write(str(eval(row)))
            outProbSum+=eval(row)
            outfile.write("\n")
            #break
            outfile.write("\n")
            outfile.write("\n")
            outfile.write("\n")

            detProb = eval(row)
            if(iter==Nmax):
                modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(iter) + ");\n"
            else:
                modelLine = str(detProb) + ":(currN'=1)&(currK'=" + str(iter) + ") + "
            modelfile.write(modelLine)

            iter+=1
    print(outProbSum)
