import numpy as np
import csv
import math


f = open('PRISMLECModel.prism', 'w')
f.write("mdp \n \n")
no_traces = 10

j = 0
inter = 0
curPos = 0
nextPos = 0

# for writing N, K and positions to the PRISM file
with open('PRISMInput.csv', newline='') as csvfile:
    while j < no_traces:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 1
        for row in csvreader:
            line = (', '.join(row)) 
            if line != 'K_'+str(j+1):      
                f.write("const int N"+str(j+1)+"_"+str(i)+" = " + line +";"+"\n")
                i += 1
            else:
                break
        
        f.write("\n")
        i = 1
        for row in csvreader:
            line = (', '.join(row)) 
            if line != 'det_tth_'+str(j+1):      
                f.write("const int K"+str(j+1)+"_"+str(i)+" = " + line +";"+"\n")
                i += 1
            else:
                break
        
        f.write("\n")

        for row in csvreader:
            line = (', '.join(row)) # for reading the det_tth value
            f.write("const int det_tth_"+str(j+1)+"=" + line +";"+"\n")
            break

        j +=1
        f.write("\n")

    i = 0
    for row in csvreader:
        if i == 0:
            i += 1
            continue # this will read the string 'pos'
        line = (', '.join(row)) 
        if line != 'det_prob':      
            f.write("const int d"+str(i)+" = " + line +";"+"\n")
            if i == 1:
                curPos = line
            if i == 2:
                nextPos = line
            i += 1
        else:
            inter = i-1
            break

    f.write("\n")
    f.write("module LECMarkovChain\n\n")
    j = 0

    print("Inter: ", inter)
    print("Cur pos: ", curPos)
    print("nextPos: ", nextPos)
    
    while j < no_traces:
        f.write("   detects_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        f.write("   trials_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        f.write("   fail_"+str(j+1)+" : [0..1] init 0;\n")
        f.write("   currN_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        f.write("   currK_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")

        f.write("\n")
        j += 1

    f.write("   pickKN : [0..1] init 1;\n")
    f.write("   inter : [1.."+str(inter)+"] init 1;\n")
    f.write("   currPos : [0.."+str(curPos)+"] init "+str(curPos)+";\n")
    f.write("   carPos : [0.."+str(curPos)+"] init "+str(curPos)+";\n")
    f.write("   nextPos : [0.."+str(nextPos)+"] init "+str(nextPos)+";\n")
    f.write("   s : [0..1] init 1;\n")
    f.write("   s1 : [0..1] init 1;\n")
    f.write("   s2 : [0..1] init 1;\n")
    f.write("   s3 : [0..1] init 1;\n")
    f.write("\n")


    i = 1
    while i<inter:
        f.write("   [] pickKN=1 & inter="+str(i)+"-> (carPos'=d"+str(i)+")&(currPos'=d"+str(i)+")&(nextPos'=d"+str(i+1)+")&(pickKN'=0)&(inter'=inter+1)")
        j = 0
        while j < no_traces:
            f.write("&(currN_"+str(j+1)+"'=N"+str(j+1)+"_"+str(i)+")&(currK_"+str(j+1)+"'=K"+str(j+1)+"_"+str(i)+")&(detects_"+str(j+1)+"'=0)&(trials_"+str(j+1)+"'=0)")
            j+=1
        f.write(";\n")
        i += 1

    f.write("\n")

    # i = 0
    # for row in csvreader:
    #     line = (', '.join(row))
    #     if i == 0:
    #         i += 1
    #         continue # this line is det_prob
    #     f.write("   [] pickKN=0 & (currPos=d"+str(i)+")&(nextPos=d"+str(i+1)+")")

    ############### ADD conditional LEC probabilities here ###############################
    probs = []
    with open('lecStatefulAverages.csv') as pr_csv_file:
        pr_csv_reader = csv.reader(pr_csv_file, delimiter=',')
        # print(pr_csv_reader)
        for pr_row in pr_csv_reader:
            pr_row = [float(row_) for row_ in pr_row]
            # print(pr_row)
            probs.append(pr_row)
    # print(probs)

    distDisc = 100

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

            f.write("   [] pickKN=0")
            j = 0
            while j < no_traces:
                f.write("& detects_"+str(j+1)+" <= det_tth_"+str(j+1))
                f.write("& detects_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
                f.write("& trials_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
                
                j += 1
            
            f.write("&")

            j = 0
            while j < no_traces:
                if no_traces == 1:
                    f.write("trials_"+str(j+1)+"<currN_"+str(j+1))
                elif j == no_traces - 1:
                    f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+")")
                elif j == 0:
                    f.write("(trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
                else:
                    f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
                j += 1

            if(numHist==3):
                f.write("&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)) 
                f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
                    j += 1
                f.write("+ "+str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
                    j += 1
                f.write(";\n")
            elif(numHist==2):
                f.write("&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
                f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
                    j += 1
                f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
                    j += 1
                f.write(";\n")
            elif(numHist==1):
                f.write("&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
                f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
                    j += 1
                f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
                    j += 1

                f.write(";\n")
            else:
                f.write("&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
                f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
                    j += 1
                f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
                j = 0
                while j < no_traces:
                    if j == no_traces - 1:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
                    else:
                        f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
                    j += 1

                f.write(";\n")
            det_index+=1
        index+=1

j = 0
while j < no_traces:
    f.write("\n   [] pickKN = 0 & trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" < currK_"+str(j+1)+" -> (fail_"+str(j+1)+"'=1);")
    j += 1
    f.write("\n")

# f.write("\n   [] pickKN = 0 &")

# j = 0
# while j < no_traces:
#     if j == no_traces - 1:
#         f.write(" trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+" & fail_"+str(j+1)+" = 0")
#     else:
#         f.write(" trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+" & fail_"+str(j+1)+" = 0 &")
#     j += 1

# f.write(" -> (pickKN' = 1);\n")

j = 0
while j < no_traces:
    f.write("\n   [] pickKN = 0 & trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+" & fail_"+str(j+1)+" = 0  -> (pickKN' = 1);\n")
    j += 1

# f.write("\n   [] ")
# j = 0
# while j < no_traces:
#     if j == no_traces - 1:
#         f.write("fail_"+str(j+1)+" = 0 -> (end_flag' = 1)\n")
#     else:
#         f.write("fail_"+str(j+1)+" = 0 & ")
#     j += 1

f.write("\nendmodule")