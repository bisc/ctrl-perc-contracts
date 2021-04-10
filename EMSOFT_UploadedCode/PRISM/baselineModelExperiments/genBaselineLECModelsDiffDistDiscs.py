import numpy as np
import csv
import math

distDiscs = [0.01,0.05,0.1,0.5,1,1.5,2]

for distDisc in distDiscs:
    speedDisc = 0.1
    B1=int(4/speedDisc)
    B2=int(8/speedDisc)

    modelFile = open("lecBaselineDistDisc" + str(distDisc) + ".prism",'w')

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
    modelFile.write("	s3 : [0..1] init 1;\n\n")

    modelFile.write("    carSpeed : [0 .. initSpeed] init initSpeed;\n")
    modelFile.write("    carPos : [0..initPos] init initPos;\n\n")

    modelFile.write("    seqflag : [0..2] init initBrakingFlag;\n")  
    modelFile.write("    contRegion : [0..2] init 0;\n\n")

    modelFile.write("    //TTC = carPos/carSpeed;")
    modelFile.write("    //xwarning = (carPos-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)\n")
    modelFile.write("    // compute controller region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/carSpeed)>TTCThresh&((carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->   (seqflag'=1)&(contRegion'=0); // safe region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/carSpeed)>TTCThresh&((carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning ->  (seqflag'=1)&(contRegion'=1); // braking region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/carSpeed)<=TTCThresh&((carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->  (seqflag'=1)&(contRegion'=1); // braking region\n")
    modelFile.write("    [] seqflag=0&((carPos-" + str(int(5/distDisc)) + ")/carSpeed)<=TTCThresh&((carPos-" + str(int(5/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning -> (seqflag'=1)&(contRegion'=2); // collision mitigation region\n\n")

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
            modelFile.write(modelLine)
            det_index+=1
        index+=1



    modelFile.write("    // compute carPos, carSpeed\n")
    modelFile.write("    [] seqflag=2&s=0&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(seqflag'=0);\n")
    modelFile.write("    [] seqflag=2&s=0&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(carSpeed'=max(0,carSpeed-floor(B1/freq)))&(seqflag'=0);\n")
    modelFile.write("    [] seqflag=2&s=0&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(carSpeed'=max(0,carSpeed-floor(B2/freq)))&(seqflag'=0);\n")
    modelFile.write("    [] seqflag=2&s=1&contRegion=0&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(seqflag'=0);\n")
    modelFile.write("    [] seqflag=2&s=1&contRegion=1&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(seqflag'=0);\n")
    modelFile.write("    [] seqflag=2&s=1&contRegion=2&carSpeed>0&carPos>0 -> (carPos'=max(0,floor(carPos-" + str(speedDisc/distDisc) + "*ceil(carSpeed/freq))))&(seqflag'=0);\n\n")



    modelFile.write("endmodule")
    modelFile.close()



