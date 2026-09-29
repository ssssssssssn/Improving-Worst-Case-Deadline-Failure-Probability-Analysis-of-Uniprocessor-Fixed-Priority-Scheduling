from __future__ import division
from multiprocessing import Pool, freeze_support
import itertools

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algorithms import chernoff, taskConvolution

'''
@function this is for parellel execution
'''
def func_star(a_b):
    return insideroutine(*a_b)

def func_star_1(a_b):
    return insideroutine_1(*a_b)

'''
@function this is for parellel execution
'''
def func_star_CB(a_b):
    return insideroutine_CB(*a_b)

'''
@function this is for parellel execution
'''


def insideroutine_1(taskset, fault_rate,the,resample_up):
    print("im in1")
    print(taskset, fault_rate,the,resample_up)
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []
    results_sld1 = []
    results_sld500 = []
    results_sld1000 = []
    results_sld10000=[]


    start=time.time()
    results_conv_carry.append(1)
    finish1 = time.time()
    results_conv_inflation.append(1)
    finish2 = time.time()
    results_sld1.append(taskConvolution.calculate_safe(taskset, fault_rate, 1,resample_up,[], [], 'SLD', True))
    finish3 = time.time()
    results_sld500.append(1)
    finish4 = time.time()
    results_sld1000.append(1)
    finish5 = time.time()
    print("carryin,inflation,1,500,1000",results_conv_carry,results_conv_inflation,results_sld1,results_sld500,results_sld1000,[finish1-start],[finish2-finish1],[finish3-finish2],[finish4-finish3],[finish5-finish4])
    return [results_conv_carry,results_conv_inflation,results_sld1,results_sld500,results_sld1000,[finish1-start],[finish2-finish1],[finish3-finish2],[finish4-finish3],[finish5-finish4]]  # , results_ori, results_carry, results_inflation]


def insideroutine(taskset, fault_rate):
    print("im in1")
    results_conv_ori = []
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []
    results_sld=[]

    results_conv_ori.append(taskConvolution.calculate(taskset, fault_rate, [], [], True))
    results_conv_carry.append(taskConvolution.calculate_safe(taskset, fault_rate, [], [], 'Carryin', True))
    results_conv_inflation.append(taskConvolution.calculate_safe(taskset, fault_rate, [], [], 'Inflation', True))

    results_sld.append(taskConvolution.calculate_safe(taskset, fault_rate, [], [], 'SLD', True))
                            
    print("results_sld,results_inflation",results_conv_ori,results_sld,results_conv_carry,results_conv_inflation)
    return [results_conv_ori,results_conv_carry, results_conv_inflation, results_sld]#, results_ori, results_carry, results_inflation]

'''
@function this is for parellel execution (CB only)
'''
def insideroutine_CB(taskset, fault_rate):
    results_conv_ori = []
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []

    results_conv_ori.append(0)
    results_conv_carry.append(0)
    results_conv_inflation.append(0)
                            
    results_ori.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Original'))
    results_carry.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Carry'))
    results_inflation.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Inflation'))
    
    return [results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation]

def main(ident , num_tasks,num_sets,fault_rate,hard_task_factor,processes,utilization,limited,the,resample_up,onlyCB):
    print("the,resample",the,resample_up)

    print ('Evaluating: %d tasksets, %d tasks, fault probability: %f, processes: %r, utilization: %r, limited: %r ' % (num_sets, num_tasks, fault_rate, processes, utilization, limited))
    try:
        if ident is not None:
            filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + 's_' + str(num_sets) + 'f_'+ str(fault_rate) + 'h_'+ str(hard_task_factor) + 'l_'+str(limited)

            # Load the generated tasksets
            try:
                tasksets = np.load('../tasksets/' + filename + '.npy', allow_pickle=True)
            except:
                raise Exception("Could not read")

            # Init lists for storing Calculated DMP
            results_conv_ori = []
            results_conv_carry = []
            results_conv_inflation = []
            results_ori = []
            results_carry = []
            results_inflation = []
            results_sld1=[]
            results_sld500 = []
            results_sld1000 = []
            results_sld10000=[]

            time_conv_carry = []
            time_conv_inflation = []
            time_sld1 = []
            time_sld500 = []
            time_sld1000 = []
            time_sld10000=[]
            rel = []

            # Distribute to multiprocesses
            print(tasksets)
            if __name__=='__main__':
                freeze_support()
                p = Pool(processes)
                if onlyCB == True:
                    rel = (p.map(func_star_CB, zip(tasksets,itertools.repeat(fault_rate))))
                else:
                    rel = (p.map(func_star_1, zip(tasksets, itertools.repeat(fault_rate),itertools.repeat(the),itertools.repeat(resample_up))))
            print('Parallel execution is finished!')
            # Distribute the results into each pile
            print("rel",rel)
            for i in rel:
                results_conv_carry.append(i[0][0])
                results_conv_inflation.append(i[1][0])
                results_sld1.append(i[2][0])
                results_sld500.append(i[3][0])
                results_sld1000.append(i[4][0])


                time_conv_carry.append(i[5][0])
                time_conv_inflation.append(i[6][0])
                time_sld1.append(i[7][0])
                time_sld500.append(i[8][0])
                time_sld1000.append(i[9][0])



            print("time_conv_carry",time_conv_carry)
            print("time_conv_inflation",time_conv_inflation)
            print("time_sld500",time_sld500)
            print("time_sld1000",time_sld1000)
            print("time_sld1",time_sld1)

            np.save('../results/mp_res_conv_carry_' + filename + '.npy', results_conv_carry)
            np.save('../results/mp_res_conv_inflation_' + filename + '.npy', results_conv_inflation)
            np.save('../results/mp_res_conv_sld1_' + filename + '.npy', results_sld1)
            np.save('../results/mp_res_conv_sld500_' + filename + '.npy', results_sld500)
            np.save('../results/mp_res_conv_sld1000_' + filename + '.npy', results_sld1000)

        else:
            raise Exception("Please specify an identifier!")

    except IOError:
        print('Could not write filename %s' % filename)

if __name__=="__main__":
    print("test")
    ident = "rtss"
    num_tasks = 20
    num_sets = 10
    fault_rate = 0.025
    hard_task_factor = 1.83
    processes = 4
    utilization = 60
    limited = 10  # False
    onlyCB = False
    the=5000
    resample_up=10000



    print("......................6.......................")
    main("rtss", 20, 50, 0.025, 1.83, 4, 60, 40, the, resample_up, onlyCB=False)






















    rel = [[2.5953818237967577e-7, 0.00050249480668694785, 0.99999999999884137, 0.00064984147854122343],
           [9.0255537470982714e-5, 0.0039362992125324707, 0.99999999999809064, 0.014193417314988698],
           [1.680508332738874e-9, 8.3826587656366376e-7, 0.22715454428659407, 3.3215563835799162e-5],
           [1.3682619512076389e-6, 0.00089859252907166542, 0.99999999999742484, 0.0026021330018303796],
           [1.0093978372465658e-11, 2.6155143353641018e-8, 0.3345902563859498, 6.3429037878471413e-7],
           [8.7385445118449326e-13, 4.3809641970710608e-9, 0.04152147476010512, 1.049040102120609e-6],
           [2.8575688036204011e-10, 3.5865698205408609e-7, 0.1805827616462988, 1.4430349778516576e-5],
           [2.2925346287771382e-11, 2.3814160261737762e-8, 0.10160513503803402, 1.5609372186643801e-6],
           [2.2571689970501385e-11, 1.1889251734079725e-7, 0.12233457679469339, 5.1301242769053941e-6],
           [2.2925346287771382e-11, 2.3814160261737762e-8, 0.10160513503803402, 1.5609372186643801e-6]]
