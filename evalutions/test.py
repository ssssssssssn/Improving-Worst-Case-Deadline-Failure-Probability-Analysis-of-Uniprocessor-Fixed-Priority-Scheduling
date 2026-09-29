import copy
a=[[-1,-2,-3,-4,-5,-6,-7]]
b = sorted(a, key=lambda x: x, reverse=False)
print(b)
c=copy.deepcopy( a)
for item in a:
    if (item[1] == -2):
        item[1] += 1
        flag = 1
        break
print(a)