from __future__ import division
import math
import random
import numpy

def determineWorkload(task, higherPriorityTasks, criteria, time):
    workload = task[criteria]
    for i in higherPriorityTasks:
        jobs = math.ceil(time / i['period'])
        workload += jobs * i[criteria]
    return workload

def min_time(tasks, criteria, numD=1):
    copy = list(tasks)
    task = copy[len(copy)-1]
    del copy[len(copy)-1]
    t = task[criteria]
    for i in copy:
        t += i[criteria]
    while(t < task['deadline']*numD):
        workload = determineWorkload(task, copy, criteria, t)
        if workload <= t:
            return t
        else:
            t = workload
    return -1


def Workload_Contrained(T,C,t):
    return C*math.ceil((t)/T)

def TDAWorst(task,HPTasks):
    C=task['abnormal_exe']
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Contrained(itask['period'], itask['abnormal_exe'],R)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R

def TDA(task,HPTasks):
    C=task['execution']
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Contrained(itask['period'], itask['execution'],R)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R
def TDAtestWorst(tasks):
    x = 0
    fail = 0
    for i in tasks:
        hpTasks = tasks[:x]
        RT=TDAWorst(i, hpTasks)
        if RT > i['deadline']:
            fail = 1
            break
        x+=1
    return fail

def TDAtest(tasks):
    x = 0
    fail = 0
    for i in tasks:
        hpTasks = tasks[:x]
        RT=TDA(i, hpTasks)
        if RT > i['deadline']:
            fail = 1
            break
        x+=1
    return fail

def sort(tasks, criteria, reverse_order):
    return sorted(tasks, key=lambda item:item[criteria], reverse=reverse_order)
