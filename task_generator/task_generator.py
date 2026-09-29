'''
Author Kevin Huang, Georg von der Brueggen and Kuan-Hsun Chen
The UUniFast / UUniFast_discard generator.

'''

from __future__ import division
import random
import math
import numpy
import sys, getopt
import json
import mixed_task_builder

ofile = "taskset-p.txt"
USet=[]

def loguniform(n, limited, Tmin=1, Tmax=100, base=10):
    TSet = []
    for i in range(n):
        TSet.append(round(math.pow(base, random.uniform(    math.floor(math.log(Tmin, base)*100), math.floor(math.log(limited, base)*100)  )/100),2))
    return TSet

def UUniFast(n,U_avg):
    global USet
    sumU=U_avg
    for i in range(n-1):
        nextSumU=sumU*math.pow(random.random(), 1/(n-i))
        USet.append(sumU-nextSumU)
        sumU=nextSumU
    USet.append(sumU)

def CSet_generate_rounded(n, limited):
    global USet,PSet
    j=0
    P = loguniform(n, limited)
    for i, p in zip(USet, P):
        pair={}
        pair['period']=round(p,2)
        pair['deadline']=round(p,2)
        pair['execution']=round(i*p,2)
        PSet.append(pair)
        j=j+1;

def CSet_generate_limited(n, limited):
    global USet,PSet
    j=0
    P = loguniform(n, limited)
    for i, p in zip(USet, P):
        pair={}
        pair['period']=round(p,2)
        pair['deadline']=round(p,2)
        pair['execution']=round(i*p,2)
        PSet.append(pair)
        j=j+1;

def init():
    global USet,PSet
    USet=[]
    PSet=[]

def taskGeneration_rounded(numTasks,uTotal):
    random.seed()
    init()
    UUniFast(numTasks,uTotal/100)
    CSet_generate_rounded(numTasks, False)
    return PSet

def taskGeneration_limited(numTasks,uTotal,limited):
    random.seed()
    init()
    UUniFast(numTasks,uTotal/100)
    CSet_generate_limited(numTasks, limited)
    return PSet

