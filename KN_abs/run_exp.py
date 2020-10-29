import os
import yaml
import argparse

######################################################################################################
# command to run this file
# python run_exp.py -start_exp 1 -end_exp 1 -m 4 -init_v 200 -init_pos 1600  
#######################################################################################################

# parse command line arguments for the config file
def parse_args(): 
    parser = argparse.ArgumentParser(description='Running parallel experiments on development machine')
    parser.add_argument('-start_exp', dest='start_exp') 
    parser.add_argument('-end_exp', dest='end_exp') 
    parser.add_argument('-m', dest='m')
    parser.add_argument('-init_v', dest='init_v')
    parser.add_argument('-init_pos', dest='init_pos')

    args = parser.parse_args()

    return args

def run(args):

    start_exp = int(args.start_exp)
    end_exp = int(args.end_exp)
    m = int(args.m)
    init_v = float(args.init_v) # CHANGE it to FLOAT if you want the speed to be a floating point no
    init_pos = float(args.init_pos) # CHANGE it to FLOAT if you want the starting position to be a floating point no

    for exp in range(start_exp,end_exp+1):
        # for init_position in range(1200,1900, 100):
        #     for init_vel in range(100,340,40):
        #         print("init_vel: {}, init_pos: {}".format(init_vel, init_position))
        #         init_v = float(init_vel)
        #         init_pos = float(init_position)
        folder_name = 'ramneet_automated_exp_results/pos{}_v{}_m{}'.format(init_pos,init_v,m)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        prism_in = '{}/PRISMInput{}.csv'.format(folder_name,exp)
        prism_out = '{}/PRISMLECModel{}.prism'.format(folder_name,exp)
        os.system("python3 K_N_gen_with_same_int_V3.py --no_traces {} --outf {} --init_v {} --init_pos {}".format(exp,prism_in,init_v,init_pos))
        os.system("python3 genPRISMfile_precomputedLEC.py --no_traces {} --input_file {} --outf {} --m {}".format(exp,prism_in,prism_out,m))
        prop = 'Pmax=? [ F ('
        for i in range(0,exp):
            prop += 'fail_{}=1&'.format(i+1)
        prop = prop[:-1]
        prop += ')]'
        with open('{}/prop{}.props'.format(folder_name,exp), 'w') as prop_file:
            prop_file.write(prop)
        prop_file.close()

if __name__ == '__main__':
    args = parse_args()
    run(args)
    print("done")





