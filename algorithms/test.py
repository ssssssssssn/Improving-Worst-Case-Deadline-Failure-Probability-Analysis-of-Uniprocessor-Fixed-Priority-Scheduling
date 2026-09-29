import math
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



def get_distribution_SLD( prob_abnormal):
    threshold=5000
    time=5
    exttime=5
    deadline=1
    distribution = []
    a = math.ceil(time / deadline)
    b = math.ceil((time + exttime) / deadline)
    c1 = 3
    c2 = 5
    S_a=[]
    print(a,b)
    if a==1:
        for k in range(0, 2, 1):
            pair = {}
            pair['misses'] = k

            if k == a:
                pair['prob'] = 1 - sum([p['prob'] for p in distribution])
            else:
                pair['prob'] = (math.factorial(b) / (math.factorial(k) * math.factorial(b - k))) * math.pow(
                    prob_abnormal, k) * math.pow((1 - prob_abnormal), (b - k))
            pair['execution'] = k * c2 + (a - k) * c1
            distribution.append(pair)
        return distribution


    if threshold >= 2**a:
        for i in range(1, int(a)+1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = set(permutations(basic))
            M = c1 * (a - i) + c2 * i
            G = (-1) * c2
            N = [a - i, i - 1]
            H = ((1 - prob_abnormal) ** (a - i)) *( prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
        for i in range(0, int(a)):
            basic = [c1] * (a - i - 1) + [c2] * i
            permutations_set = set(permutations(basic))
            M = c1 * (a - i) + c2 * i
            G = (-1) * c1
            N = [a - i - 1, i]
            H = ((1 - prob_abnormal) ** (a - i)) *( prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
    elif threshold < 2**a and threshold >= 2**(a-1):
        for i in range(1, int(a)+1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = set(permutations(basic))
            M = c1 * (a - i) + c2 * i
            G = (-1) * c2
            N = [a - i, i - 1]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
        turn=0
        for i in range(0, int(a)):
            turn+=1
            if (a - turn + len(S_a) + (
                    math.factorial(a-1) / (math.factorial(i) * math.factorial(a-1 - i))) > threshold):
                break
            else:
                basic = [c1] * (a - i - 1) + [c2] * i
                permutations_set = set(permutations(basic))
                M = c1 * (a - i) + c2 * i
                G = (-1) * c1
                N = [a - i - 1, i]
                H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
                for delta in permutations_set:
                    S_a.append([M, list(delta), G, N, H])
        for j in range(i,int(a),1):
            M=c1 * (a - j) + c2 * j
            H=(((1 - prob_abnormal) ** (a - j)) * (prob_abnormal ** j))*(
                    math.factorial(a-1) / (math.factorial(j) * math.factorial(a-1 - j)))
            G = (-1) * c1
            N = [a - j - 1, j]
            S_a.append([M, [c1] * (a - j-1)+[c2] * (j), G, N, H])
    elif threshold < 2 ** (a - 1):
        turn = 0
        for i in range(1, int(a) + 1, 1):
            turn += 1
            if (2*a - turn + len(S_a) + (
                    math.factorial(a - 1) / (math.factorial(i-1) * math.factorial(a - i))) > threshold):
                break
            else:
                basic = [c1] * (a - i) + [c2] * (i - 1)
                permutations_set = set(permutations(basic))
                M = c1 * (a - i) + c2 * i
                G = (-1) * c2
                N = [a - i, i - 1]
                H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
                for delta in permutations_set:
                    S_a.append([M, list(delta), G, N, H])
        for j in range(i, int(a)+1, 1):
            M = c1 * (a - j) + c2 * j
            H = (((1 - prob_abnormal) ** (a - j)) * (prob_abnormal ** j))*(
                    math.factorial(a - 1) / (math.factorial(j-1) * math.factorial(a - j)))
            G = (-1) * c2
            N = [a - j , j- 1]
            S_a.append([M, [c1] * (a - j ) + [c2] * (j- 1), G, N, H])
        for i in range(0, int(a), 1):
            M = c1 * (a - i) + c2 * i
            H = (((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i))*(
                    math.factorial(a - 1) / (math.factorial(i) * math.factorial(a - i-1)))
            G = (-1) * c1
            N = [a - i - 1, i]
            S_a.append([M, [c1] * (a - i - 1) + [c2] * (i), G, N, H])

    sum=0
    for t in S_a:
        sum+=t[4]
    print(sorted(S_a))
    print("len(S_a)",len(S_a),sum)
    out=[]
    CCC=[c1,c2]
    PPP=[1-prob_abnormal,prob_abnormal]
    if a<b:
        for l in range(a+1,int(b)+1) :
            S_a_new = []
            for tuple in S_a:
                if tuple[0]<(c2*int(a)):
                    for cx in range(0,2,1):
                        diff=tuple[2]+CCC[cx]
                        delta_new=copy.deepcopy(tuple[1])
                        delta_new=delta_new[1:]
                        delta_new.append(CCC[cx])
                        H_new=tuple[4]*PPP[cx]
                        if diff>0:
                            M_new=tuple[0]+diff
                            G_new = -tuple[1][0]
                        else:
                            M_new = tuple[0]
                            G_new = diff-tuple[1][0]
                        N_new=copy.deepcopy(tuple[3])
                        if tuple[1][0]==c1:
                            N_new[0]-=1
                        else :
                            N_new[1]-=1
                        N_new[cx]+=1
                        tuple_new=[M_new,delta_new,G_new,N_new,H_new]
                        if (not (any (tuple_new[0:4] == item[0:4] for item in S_a_new))):
                            S_a_new.append(tuple_new)
                        else:
                            for item in S_a_new:
                                if item[0:4] == tuple_new[0:4]:
                                    item[4] += tuple_new[4]
                                    break
                else:
                    S_a_new.append(tuple)
            if len (S_a_new)>threshold:
                print("do pruning")
                do_pruning(S_a_new,threshold)
            S_a=copy.deepcopy(S_a_new)
    for x in S_a:
        pair={}
        pair['misses']=x[3][1]
        pair['execution']=x[0]
        pair['prob'] = x[4]
        flagy=1
        for y in out:
            if y['execution']==pair['execution']:
                y['prob'] += x[4]
                flagy=0
                break
        if flagy:
            out.append(pair)
    print(out)
    return out

def do_pruning(S_a_new,threshold):
    S_a_new1 = sorted(S_a_new, key=lambda x: (x[2], -x[0],x[3]), reverse=False)
    out=[]
    while(len(S_a_new1)+len(out)>threshold):
        print("len(S_a_new1),len(out)",len(S_a_new1),len(out))
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
    return out

if __name__=="__main__":
    get_distribution_SLD(0.025)
    print(0.025 ** 5)
    aaaaaa=[1,2,3,4,5,6]
    print(aaaaaa[1:])
    print(aaaaaa[0:5])
    c=-3.1415926
    print(round(c))
    n=10
    Tset=[]
    limited=60
    print(math.pow(10,(math.floor(math.log(60, 10)*100))/100))
    for i in range(n):
        Tset.append(round(math.pow(10, random.uniform(math.floor(math.log(1, 10) * 100),
                                                  math.floor(math.log(limited, 10) * 100)) / 100),2))
    print(Tset)











