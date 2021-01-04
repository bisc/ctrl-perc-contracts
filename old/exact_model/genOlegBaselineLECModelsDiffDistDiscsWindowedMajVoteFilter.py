import numpy as np
import csv
import math

# distDiscs = [0.05,0.1,0.5,1,1.5,2]
# distDiscs = [0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]
# distDiscs = [0.1,0.5, 1, 2]
# distDiscs = [0.2, 0.25, 0.4]

distDiscs = [0.04]

H = 3
L=3
for distDisc in distDiscs:
    speedDisc = 0.1
    B1=int(4/speedDisc)
    B2=int(8/speedDisc)

    modelFile = open("olegBaseline/windowed/olegBaselineLECModelH" + str(H) + "L" + str(L) + "DistDisc" + str(distDisc) + ".prism",'w')

    probs = []
    with open('lecStatefulAverages.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print(csv_reader)
        for row in csv_reader:
            row = [float(row_) for row_ in row]
            # print(row)
            probs.append(row)
    # print(probs)




    maxDist = 200/distDisc
    minDist = 0/distDisc
    LECInvervalLen = 10


    index = 0
    for prob in probs:

        numHist = math.log(len(prob),2)
        distLower = int((index*LECInvervalLen))
        distUpper = int(((index+1)*LECInvervalLen))

        distIndLower = math.floor(distLower/distDisc)+1
        distIndUpper = math.floor(distUpper/distDisc)+1
        print(distUpper)
        print(distLower)
        print(distIndUpper)
        print(distIndLower)

        det_index = 0
        for detProb in prob:
            detProb = abs(detProb)
            s1 = 1-(det_index % 2)
            s2 = 1-(math.floor((det_index/2)) % 2)
            s3 = 1-(math.floor((det_index/4)) % 2)
            s4 = 1-(math.floor((det_index/8)) % 2)
            s5 = 1-(math.floor((det_index/16)) % 2)
            s6 = 1-(math.floor((det_index/32)) % 2)
            s7 = 1-(math.floor((det_index/64)) % 2)

            #modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower)+ " -> " + str(detProb) + ":(s'=0)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(currN'=1)&(currK'=0);\n"
            if(numHist==3):
                if(H==2):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)&(currK'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1)&(currK'=0);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=0);\n"
                if(H==4):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=0);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=0);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=0);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=0);\n"
            elif(numHist==2):
                if(H==2):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1)&(currK'=0);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=0);\n"
                if(H==4):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=0);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=0);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=0);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=0);\n"
            elif(numHist==1):
                if(H==2):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1)&(currK'=0);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=0);\n"
                if(H==4):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=0);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=0);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=0);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=0);\n"
            else:
                if(H==2):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1)&(currK'=0);\n"
                if(H==3):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=0);\n"
                if(H==4):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)&(currK'=0);\n"
                if(H==5):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)&(currK'=0);\n"
                if(H==6):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)&(currK'=0);\n"
                if(H==7):
                    modelLine = "    [] currN=0&did<" + str(distIndUpper) + "&did>=" + str(distIndLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)&(currK'=0);\n"

            #print(modelLine)
            modelFile.write(modelLine)
            det_index+=1
        index+=1


