import os
import yaml
import argparse

######################################################################################################
# command to run this file
# python run_exp.py -exps 1 -m 3 -init_v 200 -init_pos 1600 # exps = no of experiments to be run with 1, 2, 3, 4,... traces
#######################################################################################################

# parse command line arguments for the config file
def parse_args(): 
    parser = argparse.ArgumentParser(description='Running parallel experiments on development machine')
    parser.add_argument('-exps', dest='exps') 
    parser.add_argument('-m', dest='m')
    parser.add_argument('-init_v', dest='init_v')
    parser.add_argument('-init_pos', dest='init_pos')

    args = parser.parse_args()

    return args

def run(args):

    no_exps = int(args.exps)
    m = int(args.m)
    init_v = int(args.init_v) # CHANGE it to FLOAT if you want the speed to be a floating point no
    init_pos = int(args.init_pos) # CHANGE it to FLOAT if you want the starting position to be a floating point no

    for exp in range(no_exps):
        prism_in = 'ramneet_automated_exp_results/PRISMInput{}.csv'.format(exp+1)
        prism_out = 'ramneet_automated_exp_results/PRISMLECModel{}.prism'.format(exp+1)
        os.system("python K_N_gen_with_same_int_V3.py --no_traces {} --outf {} --init_v {} --init_pos {}".format(exp+1,prism_in,init_v,init_pos))
        os.system("python genPRISMfile_precomputedLEC.py --no_traces {} --input_file {} --outf {} --m {}".format(exp+1,prism_in,prism_out,m))
        prop = 'Pmax=? [ F ('
        for i in range(0,exp+1):
            prop += 'fail_{}=1&'.format(i+1)
        prop = prop[:-1]
        prop += ')]'
        with open('ramneet_automated_exp_results/prop{}.props'.format(exp+1), 'w') as prop_file:
            prop_file.write(prop)
        prop_file.close()

if __name__ == '__main__':
    args = parse_args()
    run(args)





