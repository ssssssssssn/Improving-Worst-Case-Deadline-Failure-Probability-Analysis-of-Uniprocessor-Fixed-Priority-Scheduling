#!/bin/bash

# each line represents one specific configuration
# - i is the meta name
# - n is the number of tasks per set  
# - s is the number of sets 
# - f is the fault rate 
# - h is the execution time of the longer version 
# - p is the number of processes (default is 1)
# - u is the total utilization
# - l is the flag for limited range [1,10] (default is [1,100])
# - o is the flag for running only Chernoff-Bound

python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 60 -l 
python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 80 -l

python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 60 
python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 80

python evaluations.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -l -o
python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -l -o

python evaluations.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -o
python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -o

python evaluations.py -i rtss -n 15 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -o
python evaluations.py -i rtss -n 25 -s 10 -f 0.025 -h 1.83 -p 4 -u 45 -o

sleep 1
