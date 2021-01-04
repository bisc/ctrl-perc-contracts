import numpy as np
import csv
import math

# distDiscs = [0.05,0.1,0.5,1,1.5,2]
distDiscs = [0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]
# distDiscs = [1]
H = 3
L=3
for distDisc in distDiscs:
    speedDisc = 0.1
    B1=int(4/speedDisc)
    B2=int(8/speedDisc)

    modelFile = open("windowed/diffDistDiscsNewInflated/lecBaselineMajVoteFilterH" + str(H) + "L" + str(L) + "DistDisc" + str(distDisc) + ".prism",'w')

    modelFile.write("mdp\n\n")
    modelFile.write("const int B1=" + str(B1) + ";\n")
    modelFile.write("const int B2=" + str(B2) + ";\n")
    modelFile.write("const int TTCThresh = 6;\n")
    modelFile.write("const int xwarning = 1;\n")
    modelFile.write("const int freq = 10;\n")
    modelFile.write("const int fmu=1;\n")
    modelFile.write("const int Thd=2;\n")

    modelFile.write("const int initPos;\n")
    modelFile.write("const int initSpeed;\n")

    modelFile.write("const int initBrakingFlag;\n")
    modelFile.write("const int initBraking;\n \n")

    modelFile.write("const int carPosThresh;\n\n")

    modelFile.write("module LECMarkovChain\n\n")

    modelFile.write("    s : [0..1] init 1;  // 0 is detect, 1 is misdetect\n")
    modelFile.write("	s2 : [0..1] init 1;\n")
    if(H==3):
        modelFile.write("	s3 : [0..1] init 1;\n\n")
    if(H==4):
        modelFile.write("	s3 : [0..1] init 1;\n\n")
        modelFile.write("	s4 : [0..1] init 1;\n\n")
    if(H==5):
        modelFile.write("	s3 : [0..1] init 1;\n\n")
        modelFile.write("	s4 : [0..1] init 1;\n\n")
        modelFile.write("	s5 : [0..1] init 1;\n\n")
    if(H==6):
        modelFile.write("	s3 : [0..1] init 1;\n\n")
        modelFile.write("	s4 : [0..1] init 1;\n\n")
        modelFile.write("	s5 : [0..1] init 1;\n\n")
        modelFile.write("	s6 : [0..1] init 1;\n\n")
    if(H==7):
        modelFile.write("	s3 : [0..1] init 1;\n\n")
        modelFile.write("	s4 : [0..1] init 1;\n\n")
        modelFile.write("	s5 : [0..1] init 1;\n\n")
        modelFile.write("	s6 : [0..1] init 1;\n\n")
        modelFile.write("	s7 : [0..1] init 1;\n\n")

    modelFile.write("    carSpeed : [0 .. initSpeed] init initSpeed;\n")
    modelFile.write("    carPos : [0..initPos] init initPos;\n\n")

    modelFile.write("    seqflag : [0..2] init initBrakingFlag;\n")  
    modelFile.write("    contRegion : [0..2] init 0;\n\n")

    modelFile.write("    //TTC = carPos/carSpeed;")
    modelFile.write("    //xwarning = (carPos-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)\n")
    modelFile.write("    // compute controller region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))>TTCThresh&((" + str(distDisc/speedDisc) + ")*(carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->   (seqflag'=1)&(contRegion'=0); // safe region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))>TTCThresh&((" + str(distDisc/speedDisc) + ")*(carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning ->  (seqflag'=1)&(contRegion'=1); // braking region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))<=TTCThresh&((" + str(distDisc/speedDisc) + ")*(carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->  (seqflag'=1)&(contRegion'=1); // braking region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))<=TTCThresh&((" + str(distDisc/speedDisc) + ")*(carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning -> (seqflag'=1)&(contRegion'=2); // collision mitigation region\n\n")

    probs = []
    with open('lecStatefulAverages.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        print(csv_reader)
        for row in csv_reader:
            row = [float(row_) for row_ in row]
            print(row)
            probs.append(row)
    print(probs)




    maxDist = 200/distDisc
    minDist = 0/distDisc
    LECInvervalLen = 10/distDisc


    index = 0
    for prob in probs:

        numHist = math.log(len(prob),2)
        distLower = int((index*LECInvervalLen))
        distUpper = int(((index+1)*LECInvervalLen))

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

            #modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(seqflag'=2);\n"
            if(numHist==3):
                if(H==2):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(seqflag'=2);\n"
                if(H==3):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
                if(H==4):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2);\n"
                if(H==5):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2);\n"
                if(H==6):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2);\n"
                if(H==7):
                    modelLine = "    [] seqflag=1&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2);\n"
            elif(numHist==2):
                if(H==2):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(seqflag'=2);\n"
                if(H==3):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
                if(H==4):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2);\n"
                if(H==5):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2);\n"
                if(H==6):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2);\n"
                if(H==7):
                    modelLine = "    [] seqflag=1&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2);\n"
            elif(numHist==1):
                if(H==2):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(seqflag'=2);\n"
                if(H==3):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
                if(H==4):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2);\n"
                if(H==5):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2);\n"
                if(H==6):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2);\n"
                if(H==7):
                    modelLine = "    [] seqflag=1&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2);\n"
            else:
                if(H==2):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(seqflag'=2);\n"
                if(H==3):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(seqflag'=2);\n"
                if(H==4):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(seqflag'=2);\n"
                if(H==5):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(seqflag'=2);\n"
                if(H==6):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(seqflag'=2);\n"
                if(H==7):
                    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(seqflag'=2);\n"

            #print(modelLine)
            modelFile.write(modelLine)
            det_index+=1
        index+=1

    roundingCombinations = (['floor','floor'],['floor','ceil'],['ceil','floor'],['ceil','ceil'])

    for rounding in roundingCombinations:
        posRounding = rounding[0]
        speedRounding = rounding[1]
        if(H==2):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2<=0)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2<=0)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2<=0)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2>0)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2>0)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2>0)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")
        

        if(H==3):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3<=1)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3<=1)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3<=1)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3>1)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3>1)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3>1)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")
        
        if(H==4):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4<=1)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4<=1)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4<=1)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4>1)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4>1)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4>1)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")

        if(H==5):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5<=2)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5<=2)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5<=2)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5>2)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5>2)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5>2)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")
        if(H==6):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6>3)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6>3)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6>3)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")

        if(H==7):
            modelFile.write("    // compute carPos, carSpeed\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B1/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0," + speedRounding + "(carSpeed-(B2/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n")
            modelFile.write("    [] seqflag=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0," + posRounding + "(carPos-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(seqflag'=0);\n\n")

    modelFile.write("endmodule")
    modelFile.close()



