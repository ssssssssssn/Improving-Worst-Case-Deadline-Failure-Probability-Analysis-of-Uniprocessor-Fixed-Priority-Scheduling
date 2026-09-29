from __future__ import division

import copy
from importlib.metadata import distribution
from pickle import FALSE
import random
import math
import sys
from tkinter import W
import numpy as np
from operator import itemgetter, attrgetter
from pkg_resources import get_distribution
import mpmath as mp
from itertools import permutations


sys.path.append('../')
from algorithms import TDA

def permuteUnique(nums):
    def backtrack(i):
        if i == n:
            res.append(curres[:])
        else:
            for j in range(n):
                if not used[j]:
                    if j > 0 and nums[j] == nums[j - 1] and not used[j - 1]:
                        continue
                    used[j] = 1
                    curres.append(nums[j])
                    backtrack(i + 1)
                    used[j] = 0
                    curres.pop()

    nums.sort()
    n = len(nums)
    res = []
    curres = []
    used = [0] * n
    backtrack(0)
    return res

def get_distribution_SLD():
    threshold=3
    prob_abnormal=0.5
    distribution = []
    a = 2
    b = 4
    c1 = 3
    c2 = 10
    S_a=[]
    if threshold >= 2 ** a:
        for i in range(1, int(a) + 1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = permuteUnique(basic)
            M = round(c1 * (a - i) + c2 * i, 6)
            G = round((-1) * c2, 6)
            N = [a - i, i - 1]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
        for i in range(0, int(a)):
            basic = [c1] * (a - i - 1) + [c2] * i
            permutations_set = permuteUnique(basic)
            M = round(c1 * (a - i) + c2 * i, 6)
            G = round((-1) * c1, 6)
            N = [a - i - 1, i]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
    elif threshold < 2 ** a and threshold >= 2 ** (a - 1):
        for i in range(1, int(a) + 1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = permuteUnique(basic)
            M = round(c1 * (a - i) + c2 * i, 6)
            G = round((-1) * c2, 6)
            N = [a - i, i - 1]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
        turn = 0
        for i in range(0, int(a)):
            turn += 1
            if (a - turn + len(S_a) + (
                    math.factorial(a - 1) / (math.factorial(i) * math.factorial(a - 1 - i))) > threshold):
                break
            else:
                basic = [c1] * (a - i - 1) + [c2] * i
                permutations_set = permuteUnique(basic)
                M = round(c1 * (a - i) + c2 * i, 6)
                G = round((-1) * c1, 6)
                N = [a - i - 1, i]
                H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
                for delta in permutations_set:
                    S_a.append([M, list(delta), G, N, H])
        for j in range(i, int(a), 1):
            M = round(c1 * (a - j) + c2 * j, 6)
            H = (((1 - prob_abnormal) ** (a - j)) * (prob_abnormal ** j)) * (
                    math.factorial(a - 1) / (math.factorial(j) * math.factorial(a - 1 - j)))
            G = round((-1) * c1, 6)
            N = [a - j - 1, j]
            S_a.append([M, [c1] * (a - j - 1) + [c2] * (j), G, N, H])
    elif threshold < 2 ** (a - 1):
        turn = 0
        for i in range(1, int(a) + 1, 1):
            turn += 1
            if (2 * a - turn + len(S_a) + (
                    math.factorial(a - 1) / (math.factorial(i - 1) * math.factorial(a - i))) > threshold):
                break
            else:
                print("wrong")
                basic = [c1] * (a - i) + [c2] * (i - 1)
                permutations_set = permuteUnique(basic)
                M = round(c1 * (a - i) + c2 * i, 6)
                G = round((-1) * c2, 6)
                N = [a - i, i - 1]
                H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
                for delta in permutations_set:
                    S_a.append([M, list(delta), G, N, H])# sum = 0
        for j in range(i, int(a) + 1, 1):
            M =round(c1 * (a - j) + c2 * j,6)
            H = (((1 - prob_abnormal) ** (a - j)) * (prob_abnormal ** j)) * (
                    math.factorial(a - 1) / (math.factorial(j - 1) * math.factorial(a - j)))
            G = round((-1) * c2,6)
            N = [a - j, j - 1]
            S_a.append([M, [c1] * (a - j) + [c2] * (j - 1), G, N, H])
        for i in range(0, int(a), 1):
            M = round(c1 * (a - i) + c2 * i,6)
            H = (((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)) * (
                    math.factorial(a - 1) / (math.factorial(i) * math.factorial(a - i - 1)))
            G = round((-1) * c1,6)
            N = [a - i - 1, i]
            S_a.append([M, [c1] * (a - i - 1) + [c2] * (i), G, N, H])
    out = []
    CCC = [c1, c2]
    PPP = [1 - prob_abnormal, prob_abnormal]

    if a < b:
        print("begin", S_a)
        for l in range(a + 1, int(b) + 1):
            S_a_new = []
            for tuple in S_a:
                for cx in range(0, 2, 1):
                    diff = round(tuple[2] + CCC[cx],6)
                    delta_new = copy.deepcopy(tuple[1])
                    delta_new = delta_new[1:]
                    delta_new.append(CCC[cx])
                    H_new = tuple[4] * PPP[cx]
                    if diff > 0:
                        M_new = round(tuple[0] + diff,6)
                        G_new = round(-tuple[1][0],6)
                    else:
                        M_new = tuple[0]
                        G_new = round(diff - tuple[1][0],6)
                    N_new = copy.deepcopy(tuple[3])
                    if tuple[1][0] == c1:
                        N_new[0] -= 1
                    else:
                        N_new[1] -= 1
                    N_new[cx] += 1
                    tuple_new = [M_new, delta_new, G_new, N_new, H_new]

                    if (not (any(tuple_new[0:2] == item[0:2] for item in S_a_new))):
                        S_a_new.append(tuple_new)
                    else:
                        for item in S_a_new:
                            if item[0:2] == tuple_new[0:2]:
                                item[4] += tuple_new[4]

                                break
            print("pre",S_a_new)
            if len(S_a_new) > threshold:
                print("do pruning")
                S_a_new=do_pruning(S_a_new, threshold)
            S_a = copy.deepcopy(S_a_new)
    for x in S_a:
        pair = {}
        pair['misses'] = x[3][1]
        pair['execution'] = x[0]
        pair['prob'] = x[4]
        flagy = 1
        for y in out:
            if y['execution'] == pair['execution']:
                y['prob'] += x[4]
                flagy = 0
                break
        if flagy:
            out.append(pair)
    print("out222",len(S_a),"len(out)",len(out),sorted(out,key=lambda x: x['execution']))
    if(len(out)>101):
        print("wiked",len(out))
    print("return")
    return out

def do_pruning(S_a_new,threshold):
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("pr pre",S_a_new)
    S_a_new1 = sorted(S_a_new, key=lambda x: (x[2], x[0],x[3]), reverse=False)
    out=[]
    while(len(S_a_new1)+len(out)>threshold):
        if len(S_a_new1)==0 :
            print("that's right")
            break
        temp=S_a_new1[0]
        types=[]
        for item in S_a_new1:
            if ((item[0]==temp[0]) and (item[3]==temp[3])):
                types.append(item)
            else:
                break
        for x in types:
            S_a_new1.remove(x)
        if len(types)>1:
            sum=0
            for u in types:
                sum+=u[4]
            out.append([temp[0],sorted(temp[1], reverse=False),temp[2],temp[3],sum])
        else:
            out+=types

    out=out+S_a_new1
    print("out",out)
    return out

get_distribution_SLD()