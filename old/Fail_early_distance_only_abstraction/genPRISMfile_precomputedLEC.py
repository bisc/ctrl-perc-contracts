import numpy as np
import csv
import math
import os

import argparse

parser = argparse.ArgumentParser(description='Generate PRISM model for K/N contract satisfaction')
parser.add_argument('--no_traces', default=1, help='number of traces for the starting point of non-braking mode')
parser.add_argument('--input_file', default='PRISMInput_test.csv', help='input file')
parser.add_argument('--outf', default='PRISMLECModel_test.prism', help='PRISM model file')
parser.add_argument('--m', default=3, help='window size for LEC filter')
parser.add_argument('--l_max', default=3, help='max value for conditioned LEC')
parser.add_argument('--det_bin_l_filename', default='binsHistLenghts.csv', help='file with bin no, l information')
parser.add_argument('--det_proba_filename', default='avgProbPerBinPerLen.csv', help='file with det proba valuesfor bins')
parser.add_argument('--vote', default='maj', help='voting for LEC')
args = parser.parse_args()

prism_input_file = args.outf

f = open(args.outf, 'w')
f.write("mdp \n")

# parameters to be tuned for running experiments
no_traces = int(args.no_traces)
#no_traces = 1
m = int(args.m)
l_max = int(args.l_max)
det_bin_l_filename = args.det_bin_l_filename
det_proba_filename = args.det_proba_filename
vote = args.vote
################################################

j = 0
inter = 0
curPos = 0
nextPos = 0


import csv
from collections import defaultdict

get_bin = lambda x: format(x, 'b').zfill(32)

def getl(fileName, bin):
    data = defaultdict(list)
    with open(fileName) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for i,row in enumerate(csvreader):
            data[int(row[0])].append([int(row[1]),i])
    
    values = data[bin]
    values.sort(key=lambda x: x[0])

    return values[-1] # l, line no. starting from 0

# print(getl('my-stateful-all-length-model/binsHistLenghts.csv',10))

def getDetProb(fileName, line_no):
    with open(fileName) as f: content = f.readlines()
    return [float(i) for i in content[line_no].split(',')]

# print(getDetProb('my-stateful-all-length-model/avgProbPerBinPerLen.csv',31))

def readAndFillSymbolic(fileName,proba_values,lthis,num_next_condition,num_traces):
    #print(fileName)
    output = defaultdict(list)

    if lthis==0:
        p = proba_values[0]
    else:
        for i in range(2**lthis):
            globals()['p{}'.format(get_bin(i)[-lthis:])] = proba_values[i]

    with open(fileName) as f: content = f.readlines()[1:]

    for row in content:
        if row=='\n':
            continue
        key,value = row.split(':')
        key_format = ''
        key_values = key.split(',')
        for i,k in enumerate(key_values):
            key_format+='s{}={}&'.format(str(i+1),k.strip())

        key_format = key_format[:-1]

        value = value.replace('{','')
        value = value.replace('}','')
        for v in value.split(','):
            exp = v.replace('^','**')
            output[key_format].append(eval(exp))

        probas = output[key_format]
        value_format = ''


        num_bits = num_next_condition

        counter = 0
        for i in range(2**num_traces):
            bin_i = get_bin(i)[-num_traces:]
            fail_format = ''
            for ii,kk in enumerate(bin_i):
                if kk=='0':
                    fail_format += '(fail_{}\'={})&'.format(str(ii+1),str(1))


            for j in range(2**num_bits):
                p = probas[counter]
                counter+=1
                if p > 0.0:
                    value_format+=str(p)
                    value_format+=':'
                    value_format+="(pickKN'=2)&"
                    bin_j = get_bin(j)[-num_bits:]

                    for ii,kk in enumerate(bin_j):
                        value_format+='(s{}\'={})&'.format(str(ii+1),kk)
                    
                    value_format+=fail_format
                    value_format=value_format[:-1]
                    value_format+='+'

        value_format=value_format[:-1]
        value_format+=";"
        output[key_format] = value_format
    
    return output

# for writing N, K and positions to the PRISM file
with open(args.input_file, newline='') as csvfile:
    KN_dict = {}
    while j < no_traces:
        N = []
        K = []
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 1
        for row in csvreader:
            line = (', '.join(row)) 
            if line != 'K_'+str(j+1):      
                # f.write("const int N"+str(j+1)+"_"+str(i)+" = " + line +";"+"\n")
                N.append(int(line))
                i += 1
            else:
                break
        
        # f.write("\n")
        i = 1
        for row in csvreader:
            line = (', '.join(row)) 
            if line != 'det_tth_'+str(j+1):      
                # f.write("const int K"+str(j+1)+"_"+str(i)+" = " + line +";"+"\n")
                K.append(int(line))
                i += 1
            else:
                break
        
        f.write("\n")

        for row in csvreader:
            line = (', '.join(row)) # for reading the det_tth value
            # f.write("const int det_tth_"+str(j+1)+"=" + line +";"+"\n")
            break

        # f.write("\n")
        KN_dict["N{}".format(j+1)] = N
        KN_dict["K{}".format(j+1)] = K
        j +=1

    i = 0
    start_positions = []
    for row in csvreader:
        if i == 0:
            i += 1
            continue # this will read the string 'pos'
        line = (', '.join(row)) 
        if line != 'det_prob':      
            # f.write("const int d"+str(i)+" = " + line +";"+"\n")
            start_positions.append(int(line))
            if i == 1:
                curPos = line
            if i == 2:
                nextPos = line
            i += 1
        else:
            inter = i-1
            break

    # f.write("\n")
    f.write("module LECMarkovChain\n\n")
    j = 0

    # print("Inter: ", inter)
    # print("Cur pos: ", curPos)
    # print("nextPos: ", nextPos)
    # print("start_pos: ", start_positions)
    # print(KN_dict)

    while j < no_traces:
        # f.write("   detects_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        # f.write("   trials_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        f.write("   fail_"+str(j+1)+" : [0..1] init 0;\n")
        # f.write("   currN_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")
        # f.write("   currK_"+str(j+1)+" : [0..det_tth_"+str(j+1)+"] init 0;\n")

        f.write("\n")
        j += 1

    f.write("   fail : [0..1] init 0;\n")

    f.write("   pickKN : [0..2] init 1;\n")
    f.write("   inter : [0.."+str(inter)+"] init 0;\n")
    # f.write("   currPos : [0.."+str(curPos)+"] init "+str(curPos)+";\n")
    # f.write("   carPos : [0.."+str(curPos)+"] init "+str(curPos)+";\n")
    # f.write("   nextPos : [0.."+str(nextPos)+"] init "+str(nextPos)+";\n")

    for i in range(0,max(m-1,l_max)):
        f.write("   s"+str(i+1)+": [0..1] init 0  ;\n")

    f.write("\n")

    # i = 1
    # while i<inter:
    f.write("   [] pickKN=1 & inter<"+str(inter-1)+"->(pickKN'=0)&(inter'=inter+1);\n")
        # f.write(";\n")
        # i += 1

    f.write("\n")

    for i in range(1,inter):
        #print('For interval: ', i)
        cur_start_pos = start_positions[i-1]/10
        this_bin = int(cur_start_pos/10)+1
        next_start_pos = start_positions[i]/10
        next_bin = int(next_start_pos/10)+1
        lthis, this_line_no = getl(det_bin_l_filename, this_bin)
        lnext, next_line_no = getl(det_bin_l_filename, next_bin)
        
        det_proba = getDetProb(det_proba_filename, this_line_no)

        num_curr_condition = max(m-1, lthis) # for no of rows from mathematica written before -> in PRISM
        num_next_condition = max(m-1, lnext) # for no of detections to be written after -> in PRISM

        # print(KN_dict)
        k_list = '{'
        n_list = '{'
        for j in range(no_traces):
            k_list = k_list+str(KN_dict['K{}'.format(j+1)][i-1])+','
            n_list = n_list+str(KN_dict['N{}'.format(j+1)][i-1])+','
        k_list=k_list[:-1]
        n_list=n_list[:-1]
        k_list = k_list+'}'
        n_list = n_list+'}'
        # print(k_list)
        # print(n_list)

        prob_dist_out_file = 'proba_dist/m={}_lthis={}_lnext={}_ks={}_ns={}_vote={}.txt'.format(m,lthis,lnext,k_list,n_list,vote)

        if not os.path.exists(prob_dist_out_file):
            os.system("wolframscript -f ./script-for-kn-anyvote-list.wls  m={} lthis={} lnext={} ks={} ns={} vote={} > {}".format(m,lthis,lnext,k_list,n_list,vote,prob_dist_out_file))
        
        proba_dist = readAndFillSymbolic(prob_dist_out_file, det_proba,lthis,num_next_condition,no_traces)
        
        for k,v in proba_dist.items():
            f.write("\n   [] pickKN=0 & inter="+str(i)+'&')
            f.write("{}->{}".format(k,v))


    ######################### ADD line for the last interval ###########################





    ############### ADD conditional LEC probabilities here ###############################
    # probs = []
    # with open('lecStatefulAverages.csv') as pr_csv_file:
    #     pr_csv_reader = csv.reader(pr_csv_file, delimiter=',')
    #     # print(pr_csv_reader)
    #     for pr_row in pr_csv_reader:
    #         pr_row = [float(row_) for row_ in pr_row]
    #         # print(pr_row)
    #         probs.append(pr_row)
    # # print(probs)

    # distDisc = 100

    # index = 0
    # for prob in probs:

    #     numHist = math.log(len(prob),2)
    #     distLower = (index*distDisc)
    #     distUpper = ((index+1)*distDisc)

    #     det_index = 0
    #     for detProb in prob:
    #         detProb = abs(detProb)
    #         s1 = 1-(det_index % 2)
    #         s2 = 1-(math.floor((det_index/2)) % 2)
    #         s3 = 1-(math.floor((det_index/4)) % 2)

    #         # for detects in the last 2 trials- inc detects by 1 with det pr
    #         f.write("   [] pickKN=0")
    #         j = 0
    #         while j < no_traces:
    #             f.write("& detects_"+str(j+1)+" <= det_tth_"+str(j+1))
    #             f.write("& detects_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
    #             f.write("& trials_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
                
    #             j += 1
            
    #         f.write("&")

    #         j = 0
    #         while j < no_traces:
    #             if no_traces == 1:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1))
    #             elif j == no_traces - 1:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+")")
    #             elif j == 0:
    #                 f.write("(trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
    #             else:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
    #             j += 1

    #         if(numHist==3):
    #             f.write("&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)) 
    #             f.write("& s=0 & s2=0") # CONDITION for detection in the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ "+str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1
    #             f.write(";\n")
    #         elif(numHist==2):
    #             f.write("&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& s=0 & s2=0") # CONDITION for detection in the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1
    #             f.write(";\n")
    #         elif(numHist==1):
    #             f.write("&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& s=0 & s2=0") # CONDITION for detection in the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1

    #             f.write(";\n")
    #         else:
    #             f.write("&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& s=0 & s2=0") # CONDITION for detection in the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&(detects_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? detects_"+str(j+1)+"+1:detects_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1

    #             f.write(";\n")

    #         # for no detect in at least one of last 2 trials- no inc of detects here
    #         f.write("   [] pickKN=0")
    #         j = 0
    #         while j < no_traces:
    #             f.write("& detects_"+str(j+1)+" <= det_tth_"+str(j+1))
    #             f.write("& detects_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
    #             f.write("& trials_"+str(j+1)+"+1 <= det_tth_"+str(j+1))
                
    #             j += 1
            
    #         f.write("&")

    #         j = 0
    #         while j < no_traces:
    #             if no_traces == 1:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1))
    #             elif j == no_traces - 1:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+")")
    #             elif j == 0:
    #                 f.write("(trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
    #             else:
    #                 f.write("trials_"+str(j+1)+"<currN_"+str(j+1)+"|")
    #             j += 1

    #         if(numHist==3):
    #             f.write("&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)) 
    #             f.write("& (s=1 | s2=1)") # CONDITION for no detection in at least one of the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ "+str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1
    #             f.write(";\n")
    #         elif(numHist==2):
    #             f.write("&s2=" + str(s2) + "&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& (s=1 | s2=1)") # CONDITION for no detection in at least one of the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1
    #             f.write(";\n")
    #         elif(numHist==1):
    #             f.write("&s=" + str(s1) + "&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& (s=1 | s2=1)") # CONDITION for no detection in at least one of the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1

    #             f.write(";\n")
    #         else:
    #             f.write("&carPos<" + str(distUpper) + "&carPos>=" + str(distLower))
    #             f.write("& (s=1 | s2=1)") # CONDITION for no detection in at least one of the last two trials
    #             f.write(" -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")            
    #                 j += 1
    #             f.write("+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&")
    #             j = 0
    #             while j < no_traces:
    #                 if j == no_traces - 1:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")")
    #                 else:
    #                     f.write("(trials_"+str(j+1)+"'=trials_"+str(j+1)+"<currN_"+str(j+1)+"? trials_"+str(j+1)+"+1:trials_"+str(j+1)+")&")          
    #                 j += 1

    #             f.write(";\n")
    #         det_index+=1
    #     index+=1



# LAST LINES for fail checking 

# j = 0
# while j < no_traces:
#     f.write("\n   [] pickKN = 0 & trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" < currK_"+str(j+1)+" -> (fail_"+str(j+1)+"'=1);")
#     j += 1
#     f.write("\n")

# f.write("\n   [] pickKN = 0 &")

# j = 0
# while j < no_traces:
#     if j == no_traces - 1:
#         f.write(" trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+" & fail_"+str(j+1)+" = 0")
#     else:
#         f.write(" trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+" & fail_"+str(j+1)+" = 0 &")
#     j += 1

# f.write(" -> (pickKN' = 1);\n")

f.write("\n\n   [] pickKN = 2")
# j = 0
# while j < no_traces:
#     f.write(" & ((trials_"+str(j+1)+" = currN_"+str(j+1)+" & detects_"+str(j+1)+" >= currK_"+str(j+1)+") | (fail_"+str(j+1)+" = 1))")
#     j += 1

j = 0
while j < no_traces:
    if no_traces == 1:
        f.write(" & (fail_"+str(j+1)+" = 0)")
    elif j == 0:
        f.write(" & (fail_"+str(j+1)+" = 0|")
    elif j == no_traces-1:
        f.write("fail_"+str(j+1)+" = 0)")
    else:
        f.write("fail_"+str(j+1)+" = 0|")
    j += 1

f.write("-> (pickKN' = 1);\n")


f.write("   [] pickKN = 2 &")
j = 0
while j < no_traces:
    if no_traces == 1:
        f.write(" (fail_"+str(j+1)+" = 1) ->")
    elif j == no_traces-1:
        f.write(" (fail_"+str(j+1)+" = 1) ->")
    else:
        f.write(" (fail_"+str(j+1)+" = 1) &")
    j += 1

f.write(" (fail' = 1);\n")
# j = 0
# while j < no_traces:
#     if j == no_traces - 1:
#         f.write("fail_"+str(j+1)+" = 0 -> (end_flag' = 1)\n")
#     else:
#         f.write("fail_"+str(j+1)+" = 0 & ")
#     j += 1

f.write("\nendmodule")
print("Done writing to: ", prism_input_file)
f.close()
