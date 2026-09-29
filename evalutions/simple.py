from __future__ import division
from multiprocessing import Pool, freeze_support
import itertools

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algorithms import chernoff, taskConvolution


results_conv_ori = []
results_conv_carry = []
results_conv_inflation = []
results_ori = []
results_carry = []
results_inflation = []
results_sld=[]
rel = []
rel=[[2.5953818237967577e-7, 0.00050249480668694785, 0.99999999999884137, 0.00064984147854122343],
 [9.0255537470982714e-5, 0.0039362992125324707, 0.99999999999809064, 0.014193417314988698],
 [1.680508332738874e-9, 8.3826587656366376e-7, 0.22715454428659407, 3.3215563835799162e-5],
 [1.3682619512076389e-6, 0.00089859252907166542, 0.99999999999742484, 0.0026021330018303796],
 [1.0093978372465658e-11, 2.6155143353641018e-8, 0.3345902563859498, 6.3429037878471413e-7],
 [8.7385445118449326e-13, 4.3809641970710608e-9, 0.04152147476010512, 1.049040102120609e-6],
 [2.8575688036204011e-10, 3.5865698205408609e-7, 0.1805827616462988, 1.4430349778516576e-5],
 [2.2925346287771382e-11, 2.3814160261737762e-8, 0.10160513503803402, 1.5609372186643801e-6],
 [2.2571689970501385e-11, 1.1889251734079725e-7, 0.12233457679469339, 5.1301242769053941e-6],
 [2.2925346287771382e-11, 2.3814160261737762e-8, 0.10160513503803402, 1.5609372186643801e-6]]

for i in rel:
    results_conv_ori.append(i[0][0])
    results_conv_carry.append(i[1][0])
    results_conv_inflation.append(i[2][0])
    print("compny", i[2][0])
    results_sld.append(i[3][0])

np.save('../results/mp_res_conv_ori_' + filename + '.npy', results_conv_ori)
np.save('../results/mp_res_conv_carry_' + filename + '.npy', results_conv_carry)
np.save('../results/mp_res_conv_inflation_' + filename + '.npy', results_conv_inflation)
np.save('../results/mp_res_conv_sld_' + filename + '.npy', results_sld)