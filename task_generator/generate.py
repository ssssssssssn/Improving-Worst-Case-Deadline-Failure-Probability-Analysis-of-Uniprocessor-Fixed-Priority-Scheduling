from __future__ import division

import task_generator
import mixed_task_builder
import getopt, sys, os
import numpy as np

sys.path.append('../')
from algorithms import TDA

'''
 @method Generates tasksets that can pass the time-demand analysis with only normal execution time
 @param utilization: Taskset utilizations
 @param hard_task_factor: Multiplier in case of abnormal mode
 @param fault_rate: Probability of a job being in abnormal mode
 @param num_task: Number of tasks in a taskset
 @param num_sets: Number of generated tasksets
'''

def tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task, num_sets, rounded, limited):
    def taskset_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task):
        while True:

            tasks = task_generator.taskGeneration_limited(num_task, utilization,limited)
            tasks = mixed_task_builder.mixed_task_set(tasks, hard_task_factor, fault_rate)
            tasks = mixed_task_builder.pdfForm(tasks)
            if TDA.TDAtest(tasks) == 0:
                break
            else:
                pass
        return tasks
    return [taskset_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task) for i in range(num_sets)]

def main():

    ident = "rtss"
    num_tasks = 20
    num_sets = 50
    fault_rate = 0.025
    hard_task_factor = 1.83
    rounded = True
    limited = 40
    print('Generating: %d tasksets, %d tasks, fault probability: %f, rounded: %r, limited: %d' % (num_sets, num_tasks, fault_rate, rounded,limited))
    for utilization in (45,50, 60,70 ,80):
        tasksets = tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_tasks, num_sets, rounded, limited)
        print(utilization,tasksets)
        try:
            if ident is not None:
                filename = '../tasksets/tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + 's_' + str(num_sets) + 'f_'+ str(fault_rate) + 'h_'+ str(hard_task_factor) + 'l_'+str(limited)
                np.save(filename, tasksets)
            else:
                raise Exception ("Please specify an identifier!")
        except IOError:
            print('Could not write filename %s' % filename)

if __name__=="__main__":
    main()
