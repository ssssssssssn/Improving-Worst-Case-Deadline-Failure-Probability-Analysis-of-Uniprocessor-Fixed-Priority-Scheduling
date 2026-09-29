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

''' Calculates the probability of deadline miss with safe upper bounds (Carry-in or inflation), varience of ECRTS'18 implementation

'tasks represents' the given task set,
'prob_abnormal' the probability of abnormal execution, i.e., higher WCET.
'probabilities' tracks the calculated probabilities for each time point
'states' tracks the number of states considered for each time point '''


def calculate_safe(tasks, prob_abnormal, probabilties, states, bound, sortedList=False):
    if sortedList == True:
        tasks = sort(tasks, 'deadline', False)
    # suppose that we are checking for the last index task
    deadline = tasks[len(tasks) - 1]['deadline']
    min_time = TDA.min_time(tasks, 'execution')
    if sortedList == True:
        tasks = sort(tasks, 'deadline', True)
    all_times = last_release(tasks,
                             deadline)  
    times = []
    for i in all_times:
        if i >= min_time:
            times.append(i)
    times.sort()
    times = [deadline] 
    for time in times:
        prob, test = calculate_probabiltiy_safe(tasks, time, prob_abnormal, states, bound,
                                                True)
        probabilties.append(prob)
    probability = 1
    for i in range(0, len(times), 1):
        if (probabilties[i] < probability):
            probability = probabilties[i]
    return probability, test


''' Calculates the probability of deadline miss as detailed in Section 5 (ECRTS'18).
All job releases of higher priority tasks are considered.

'tasks represents' the given task set,
'prob_abnormal' the probability of abnormal execution, i.e., higher WCET.
'probabilities' tracks the calculated probabilities for each time point
'states' tracks the number of states considered for each time point '''


def calculate(tasks, prob_abnormal, probabilties, states, sortedList=False):
    if sortedList == True:
        tasks = sort(tasks, 'deadline', False)
    deadline = tasks[len(tasks) - 1]['deadline']
    min_time = TDA.min_time(tasks, 'execution')
    if sortedList == True:
        tasks = sort(tasks, 'execution', True)
    all_times = all_releases(tasks, deadline)
    times = []
    for i in all_times:
        if i > min_time:
            times.append(i)
    times.sort()
    for time in times:
        prob = calculate_probabiltiy(tasks, time, prob_abnormal, states)
        probabilties.append(prob)
    probability = 1
    for i in range(0, len(times), 1):
        if (probabilties[i] < probability):
            probability = probabilties[i]
    return probability


''' Calculates the deadline miss probability for a given point in time'''


def calculate_probabiltiy_safe(tasks, time, prob_abnormal, states, bound, sortedList=False):
    resample_up = 1000000
    if sortedList == True:
        order = sort(tasks, 'period', True)
    else:
        order = tasks
    distributions = []
    if bound == 'Carryin':
        for task in order:
            if task == order[0]:
                # if this is the lowest priority task k
                distributions.append(get_distribution(task, time, prob_abnormal))
            else:
                distributions.append(get_distribution_carryin(task, time, prob_abnormal))
    elif bound == 'Inflation':
        # Generates the binomial distribution of the tasks
        for task in order:
            if task == order[len(order) - 1]:
                # if this is the lowest priority task k
                distributions.append(get_distribution(task, time, prob_abnormal))
            else:
                if sortedList == True:
                    tasks = sort(tasks, 'deadline', False)
                saiTasks = []
                flag = False
                for i in range(0, len(tasks) - 1, 1):
                    if tasks[i] == task:
                        flag = True
                    if flag == True:
                        saiTasks.append(tasks[i])
                exttime = sum(tsk['deadline'] for tsk in saiTasks)
                distributions.append(get_distribution_inflation(task, time, exttime, prob_abnormal))
    elif bound == 'SLD':

        # Generates the binomial distribution of the tasks
        for task in order:
            if task == order[len(order) - 1]:
                # if this is the lowest priority task k
                distributions.append(get_distribution(task, time, prob_abnormal))
            else:
                if sortedList == True:
                    tasks = sort(tasks, 'deadline', False)
                SLDTasks = []
                flag = False
                for i in range(0, len(tasks) - 1, 1):
                    if tasks[i] == task:
                        flag = True
                    if flag == True:
                        SLDTasks.append(tasks[i])
                exttime = sum(tsk['deadline'] for tsk in SLDTasks)
                distributions.append(get_distribution_SLD(task, time, exttime, prob_abnormal))
    print(distributions)
    # creates an empty distribution as starting point for the convolution
    distri = empty_distri()
    # successively convolutes the starting distribution with the
    for i in range(0, len(distributions), 1):
        distri = convolute(distri, distributions[i])
        print("mark", len(distri))
        if len(distri) > resample_up:
            distri = resample(distri, resample_up)
    prob = calculate_miss_prob(distri, time)
    print(bound, prob)
    distri = sort(distri, 'execution', False)
    sumt = 0
    test = []
    for i in distri:
        sumt += i['prob']
        test.append(sumt)
    return prob, test


def resample(distri, resample_up):
    p = 0
    result = []
    distri = sorted(distri, key=lambda item: item['execution'])
    q = math.ceil(len(distri) / resample_up)
    for i in range(0, len(distri)):
        p = p + distri[i]['prob']
        if (((i % q) == 0 and (i != 0)) or (i == (len(distri) - 1))):
            pair = {}
            pair['prob'] = p
            pair['execution'] = distri[i]['execution']
            result.append(pair)
            p = 0
    return result


''' Calculates the deadline miss probability for a given point in time'''


def calculate_probabiltiy(tasks, time, prob_abnormal, states):
    order = sort(tasks, 'execution', True)
    distributions = []
    # Generates the binomial distribution of the tasks
    for task in order:
        distributions.append(get_distribution(task, time, prob_abnormal))
    # creates an empty distribution as starting point for the convolution
    distri = empty_distri()
    # successively convolutes the starting distribution with the
    for i in range(0, len(distributions), 1):
        distri = convolute(distri, distributions[i])
    prob = calculate_miss_prob(distri, time)
    return prob


# calculates the binomial distribution with the inflated pdf
def get_distribution_inflation(task, time, exttime, prob_abnormal):
    distribution = []
    a = math.ceil(time / task['deadline'])
    b = math.ceil((time + exttime) / task['deadline'])
    for k in range(0, int(a) + 1, 1):
        pair = {}
        pair['misses'] = k

        if k == a:
            pair['prob'] = 1 - sum([p['prob'] for p in distribution])
        else:
            pair['prob'] = (math.factorial(b) / (math.factorial(k) * math.factorial(b - k))) * math.pow(prob_abnormal,
                                                                                                        k) * math.pow(
                (1 - prob_abnormal), (b - k))
        pair['execution'] = round(k * task['abnormal_exe'] + (a - k) * task['execution'], 6)
        distribution.append(pair)
    print("out", "len(out)", len(distribution), sorted(distribution, key=lambda x: x['execution']))
    return distribution


# SLD

def get_distribution_SLD(task, time, exttime, prob_abnormal):
    threshold = 5000
    distribution = []
    a = math.ceil(time / task['deadline'])
    b = math.ceil((time + exttime) / task['deadline'])
    c1 = task['execution']
    c2 = task['abnormal_exe']
    S_a = []
    print("basic imformations", task)
    print("basic imformations_2", a, b, c1, c2, 1 - prob_abnormal, prob_abnormal)
    if a == 1:
        for k in range(0, 2, 1):

            pair = {}
            pair['misses'] = k

            if k == a:
                pair['prob'] = 1 - sum([p['prob'] for p in distribution])
            else:
                pair['prob'] = (math.factorial(b) / (math.factorial(k) * math.factorial(b - k))) * math.pow(
                    prob_abnormal, k) * math.pow((1 - prob_abnormal), (b - k))
            pair['execution'] = round(k * task['abnormal_exe'] + (a - k) * task['execution'], 6)
            distribution.append(pair)
        print("out", sorted(distribution, key=lambda x: x['execution']))
        return distribution

    if threshold >= 2 ** a:
        print("case1")
        for i in range(1, int(a) + 1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = set(permutations(basic))
            M = round(c1 * (a - i) + c2 * i, 6)
            G = round((-1) * c2, 6)
            N = [a - i, i - 1]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
        for i in range(0, int(a)):
            basic = [c1] * (a - i - 1) + [c2] * i
            permutations_set = set(permutations(basic))
            M = round(c1 * (a - i) + c2 * i, 6)
            G = round((-1) * c1, 6)
            N = [a - i - 1, i]
            H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
            for delta in permutations_set:
                S_a.append([M, list(delta), G, N, H])
    elif threshold < 2 ** a and threshold >= 2 ** (a - 1):
        print("case2")
        for i in range(1, int(a) + 1, 1):
            basic = [c1] * (a - i) + [c2] * (i - 1)
            permutations_set = set(permutations(basic))
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
                permutations_set = set(permutations(basic))
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
        print("case3")
        turn = 0
        for i in range(1, int(a) + 1, 1):
            turn += 1
            if (2 * a - turn + len(S_a) + (
                    math.factorial(a - 1) / (math.factorial(i - 1) * math.factorial(a - i))) > threshold):
                break
            else:
                basic = [c1] * (a - i) + [c2] * (i - 1)
                permutations_set = set(permutations(basic))
                M = round(c1 * (a - i) + c2 * i, 6)
                G = round((-1) * c2, 6)
                N = [a - i, i - 1]
                H = ((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)
                for delta in permutations_set:
                    S_a.append([M, list(delta), G, N, H])
        for j in range(i, int(a) + 1, 1):
            M = round(c1 * (a - j) + c2 * j, 6)
            H = (((1 - prob_abnormal) ** (a - j)) * (prob_abnormal ** j)) * (
                    math.factorial(a - 1) / (math.factorial(j - 1) * math.factorial(a - j)))
            G = round((-1) * c2, 6)
            N = [a - j, j - 1]
            S_a.append([M, [c1] * (a - j) + [c2] * (j - 1), G, N, H])
        for i in range(0, int(a), 1):
            M = round(c1 * (a - i) + c2 * i, 6)
            H = (((1 - prob_abnormal) ** (a - i)) * (prob_abnormal ** i)) * (
                    math.factorial(a - 1) / (math.factorial(i) * math.factorial(a - i - 1)))
            G = round((-1) * c1, 6)
            N = [a - i - 1, i]
            S_a.append([M, [c1] * (a - i - 1) + [c2] * (i), G, N, H])

    print(sorted(S_a))
    out = []
    CCC = [c1, c2]
    PPP = [1 - prob_abnormal, prob_abnormal]
    if a < b:
        for l in range(a + 1, int(b) + 1):
            S_a_new = []
            for tuple in S_a:
                if tuple[0] < (c2 * int(a)):
                    for cx in range(0, 2, 1):
                        diff = round(tuple[2] + CCC[cx], 6)
                        delta_new = copy.deepcopy(tuple[1])
                        delta_new = delta_new[1:]
                        delta_new.append(CCC[cx])
                        H_new = tuple[4] * PPP[cx]
                        if diff > 0:
                            M_new = round(tuple[0] + diff, 6)
                            G_new = round(-tuple[1][0], 6)
                        else:
                            M_new = tuple[0]
                            G_new = round(diff - tuple[1][0], 6)
                        N_new = copy.deepcopy(tuple[3])
                        if tuple[1][0] == c1:
                            N_new[0] -= 1
                        else:
                            N_new[1] -= 1
                        N_new[cx] += 1
                        tuple_new = [M_new, delta_new, G_new, N_new, H_new]
                        if (not (any(tuple_new[0:4] == item[0:4] for item in S_a_new))):
                            print("deal111111111111111")
                            S_a_new.append(tuple_new)
                        else:
                            print("deal222222222222222")
                            for item in S_a_new:
                                if item[0:4] == tuple_new[0:4]:
                                    item[4] += tuple_new[4]
                                    break
                else:
                    S_a_new.append(tuple)
            if len(S_a_new) > threshold:
                print("do pruning")
                do_pruning(S_a_new, threshold)
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
    print("out", len(S_a), "len(out)", len(out), sorted(out, key=lambda x: x['execution']))
    return out


def do_pruning(S_a_new, threshold):
    S_a_new1 = sorted(S_a_new, key=lambda x: (x[2], x[0], x[3]), reverse=False)
    out = []
    while (len(S_a_new1) + len(out) > threshold):
        temp = S_a_new1[0]
        types = []
        for item in S_a_new1:
            if ((item[0] == temp[0]) and (item[3] == temp[3])):
                types.append(item)
            else:
                break
        for x in types:
            S_a_new1.remove(x)
        if len(types) > 1:
            sum = 0
            for u in types:
                sum += u[4]
            out.append([temp[0], sorted(temp[1], reverse=False), temp[2], temp[3], sum])
        else:
            out += types
    out = out + S_a_new1
    return out


# calculates the binomial distribution with carryin
def get_distribution_carryin(task, time, prob_abnormal):
    distribution = []
    n = math.ceil((time + task['deadline']) / task['deadline'])
    for k in range(0, int(n) + 1, 1):
        pair = {}
        pair['misses'] = k
        pair['prob'] = (math.factorial(n) / (math.factorial(k) * math.factorial(n - k))) * math.pow(prob_abnormal,
                                                                                                    k) * math.pow(
            (1 - prob_abnormal), (n - k))
        pair['execution'] = k * task['abnormal_exe'] + (n - k) * task['execution']
        distribution.append(pair)
    return distribution


# calculates the binomial distribution for a given task, time, and probability of abnormal execution
def get_distribution(task, time, prob_abnormal):
    distribution = []
    n = math.ceil(time / task['deadline'])
    for k in range(0, int(n) + 1, 1):
        pair = {}
        pair['misses'] = k
        pair['prob'] = (math.factorial(n) / (math.factorial(k) * math.factorial(n - k))) * math.pow(prob_abnormal,
                                                                                                    k) * math.pow(
            (1 - prob_abnormal), (n - k))
        pair['execution'] = k * task['abnormal_exe'] + (n - k) * task['execution']
        distribution.append(pair)
    return distribution


# direct convolution of two distributions
def convolute(dist1, dist2):
    dist = []
    for state1 in dist1:
        for state2 in dist2:
            pair = {}
            pair['prob'] = state1['prob'] * state2['prob']
            pair['execution'] = state1['execution'] + state2['execution']
            dist.append(pair)
    return dist


def convolute_prune(dist1, dist2, minimum, maximum, num_states, pruned, prob_cut, time):
    prob = 0.0
    dist = []
    prune = 0
    states = 0
    for state1 in dist1:
        for state2 in dist2:
            states = states + 1
            pair = {}
            pair['prob'] = state1['prob'] * state2['prob']
            pair['execution'] = state1['execution'] + state2['execution']
            # if a new state will always result in a deadline miss it can be pruned
            # probability of the state is added to the miss probabiltiy
            if ((pair['execution'] + minimum) > time):
                prune = prune + 1
                prob = prob + pair['prob']
            # if a new state will never result in a deadline miss it can be pruned
            elif ((pair['execution'] + maximum) < time):
                prune = prune + 1
            # otherwise, it has to be considered further
            else:
                dist.append(pair)
    prob_cut.append(prob)
    pruned.append(prune)
    num_states.append(states)
    return dist


# Calculates the deadline miss probability for a given distribution and the time,
# related probabilities.
def calculate_miss_prob(distribution, time):
    prob = mp.mpf(0.0)
    for dist in distribution:
        if (dist['execution'] > time):
            prob = prob + dist['prob']
    return prob


# calculates the time for the last releases of all tasks before the deadline (and adds the deadline)
# (Binomial based approach)
def last_release(tasks, deadline):
    times = []
    for task in tasks:
        times.append(math.floor(deadline / task['deadline']) * task['deadline'])
    return times


# calculates the time for all releases of all tasks before the deadline (and adds the deadline)
# (Binomial based approach)
def all_releases(tasks, deadline):
    times = []
    times.append(deadline)
    for task in tasks:
        count = task['period']
        while (count < deadline):
            times.append(count)
            count = count + task['period']
    return times


# creates the jobs that have to be convoluted in the convolution based approach
def calculate_releases(tasks, deadline, releases, prob_abnormal):
    for task in tasks:
        time = 0.0
        while (time < deadline):
            distribution = []
            for k in range(0, 2, 1):
                pair = {}
                pair['time'] = time
                pair['prob'] = math.pow(prob_abnormal, k) * math.pow((1 - prob_abnormal), (1 - k))
                pair['execution'] = k * task['abnormal_exe'] + (1 - k) * task['execution']
                distribution.append(pair)
            releases.append(distribution)
            time = time + task['period']


def sort(tasks, criteria, reverse_order):
    return sorted(tasks, key=lambda item: item[criteria], reverse=reverse_order)


# initializes an empty distribution (workload 0 with probability 1)
def empty_distri():
    distri = []
    pair = {}
    pair['misses'] = ''
    # pair['prob']=np.longdouble(1.0)
    pair['prob'] = mp.mpf(1.0)
    pair['execution'] = 0.0
    distri.append(pair)
    return distri
