

def convolute(dist1, dist2):
    dist = []
    for state1 in dist1:
        for state2 in dist2:
            pair={}
            pair['prob']=state1[1]*state2[1]
            pair['execution']=state1[0]+state2[0]
            dist.append(pair)
    return dist

a=[[1,1],[2,1]]
b=[[1,1],[2,1]]
print(convolute(a,b))


