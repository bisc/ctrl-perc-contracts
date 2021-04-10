import numpy as np
import csv
import math


probs = []
with open('lecStatefulConservativeBounds.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        probs.append(row)
print(probs)




maxDist = 2000
minDist = 0
distDisc = 100

f = open('PRISMLECModelConservative.txt', 'w')

index = 0
for prob in probs:

    numHist = math.log(len(prob),2)
    distLower = (index*distDisc)
    distUpper = ((index+1)*distDisc)

    det_index = 0
    for detProb in prob:
        detProb = abs(detProb)
        s1 = 1-(det_index % 2)
        s2 = 1-(math.floor((det_index/2)) % 2)
        s3 = 1-(math.floor((det_index/4)) % 2)

        #modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(seqflag'=2);\n"
        if(numHist==3):
            modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        elif(numHist==2):
            modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        elif(numHist==1):
            modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        else:
            modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"

        #print(modelLine)
        f.write(modelLine)
        det_index+=1
    index+=1
f.close()





probs = []
with open('lecStatefulAverages.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        probs.append(row)
print(probs)




maxDist = 2000
minDist = 0
distDisc = 100

f = open('PRISMLECModelAverages.txt', 'w')

index = 0
for prob in probs:

    numHist = math.log(len(prob),2)
    distLower = (index*distDisc)
    distUpper = ((index+1)*distDisc)

    det_index = 0
    for detProb in prob:
        detProb = abs(detProb)
        s1 = 1-(det_index % 2)
        s2 = 1-(math.floor((det_index/2)) % 2)
        s3 = 1-(math.floor((det_index/4)) % 2)

        #modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(seqflag'=2);\n"
        if(numHist==3):
            modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        elif(numHist==2):
            modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        elif(numHist==1):
            modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
        else:
            modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"

        #print(modelLine)
        f.write(modelLine)
        det_index+=1
    index+=1
f.close()




probs = []
with open('lecStatefulAverages.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        probs.append(row)
print(probs)




maxDist = 200
minDist = 0
distDisc = 10

latticeDistDisc = 1.5

f = open('PRISMLECModelForLatticeAverages.txt', 'w')

index = 0
for prob in probs:

    numHist = math.log(len(prob),2)
    distLower = (index*distDisc)
    distUpper = ((index+1)*distDisc)

    distIndLower = math.floor(distLower/latticeDistDisc)+1
    distIndUpper = math.floor(distUpper/latticeDistDisc)+1
    det_index = 0
    for detProb in prob:
        detProb = abs(detProb)
        s1 = 1-(det_index % 2)
        s2 = 1-(math.floor((det_index/2)) % 2)
        s3 = 1-(math.floor((det_index/4)) % 2)

        #modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(seqflag'=2);\n"
        if(numHist==3):
            modelLine = "    [] currN<Nmax&currK<Nmax&did>1&vid>1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=currN+1)&(currK'=currK+1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=currN+1);\n"
        elif(numHist==2):
            modelLine = "    [] currN<Nmax&currK<Nmax&did>1&vid>1&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=currN+1)&(currK'=currK+1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=currN+1);\n"
        elif(numHist==1):
            modelLine = "    [] currN<Nmax&currK<Nmax&did>1&vid>1&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=currN+1)&(currK'=currK+1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=currN+1);\n"
        else:
            modelLine = "    [] currN<Nmax&currK<Nmax&did>1&vid>1&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=currN+1)&(currK'=currK+1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=currN+1);\n"

        #print(modelLine)
        f.write(modelLine)
        det_index+=1
    index+=1
f.close()

