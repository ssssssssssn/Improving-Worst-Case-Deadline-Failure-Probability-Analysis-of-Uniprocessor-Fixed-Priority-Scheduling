        S_a.append( [c1*a,   [c1]*(a-1), (-1)*c1,    [a-1,0],    (1-prob_abnormal)**a]  )
        S_a.append([c2 * a, [c2] * (a - 1), (-1) * c2, [0, a - 1],  prob_abnormal ** a])
        for i in range (1, int(a),1):
            basic=[c1]*(a-i-1)+[c2]*i
            permutations_set = set(permutations(basic))
            M=c1*(a-i)+c2*i
            G=(-1)*c1
            N=[a-i-1, i]
            H = (1 - prob_abnormal) ** (a - i) + prob_abnormal ** i
            for delta in permutations_set:
                S_a.append([M,delta,G,N,H])
            basic = [c1] * (a - i ) + [c2] * (i- 1)
            permutations_set = set(permutations(basic))
            M = c1 * (a - i) + c2 * i
            G = (-1) * c2
            N = [a - i , i- 1]
            H = (1 - prob_abnormal) ** (a - i) + prob_abnormal ** i
            for delta in permutations_set:
                S_a.append([M, delta, G, N, H])

S_a.append([c1 * a, [c1] * (a - 1), (-1) * c1, [a - 1, 0], (1 - prob_abnormal) ** a])
S_a.append([c2 * a, [c2] * (a - 1), (-1) * c2, [0, a - 1], prob_abnormal ** a])
for i in range(1, int(a), 1):
    if ((2 * a - 2) - 2 * i + len(S_a) + (math.factorial(a) / (math.factorial(i) * math.factorial(a - i))) > threshold):
        break
    else:
        basic = [c1] * (a - i - 1) + [c2] * i
        permutations_set = set(permutations(basic))
        M = c1 * (a - i) + c2 * i
        G = (-1) * c1
        N = [a - i - 1, i]
        H = (1 - prob_abnormal) ** (a - i) + prob_abnormal ** i
        for delta in permutations_set:
            S_a.append([M, j, G, N, H])
        basic = [c1] * (a - i) + [c2] * (i - 1)
        permutations_set = set(permutations(basic))
        M = c1 * (a - i) + c2 * i
        G = (-1) * c2
        N = [a - i, i - 1]
        H = (1 - prob_abnormal) ** (a - i) + prob_abnormal ** i
        for delta in permutations_set:
            S_a.append([M, j, G, N, H])
for j in range(i, int(a), 1):
    M = c1 * (a - j) + c2 * j
    H = (1 - prob_abnormal) ** (a - j) + prob_abnormal ** j
    S_a.append([M, [c1] * (a - j - 1) + [c2] * (j), (-1) * c1, [a - j - 1, j], (1 - prob_abnormal) ** a])
    S_a.append([M, [c1] * (a - j) + [c2] * (j - 1), (-1) * c2, [a - j, j - 1], (1 - prob_abnormal) ** a])