#!/bin/bash

# each line represents one specific configuration
# - i is the meta name
# - n is the number of tasks per set  
# - s is the number of sets 
# - f is the fault rate 
# - h is the execution time of the longer version 
# - r is the flag for rounding
# - l is the flag for generating periods in range [1,10] (default is [1,100])

python generate.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -r -l # [1,10]
python generate.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -r -l # [1,10]
python generate.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -r # [1,100]
python generate.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -r # [1,100]
python generate.py -i rtss -n 15 -s 10 -f 0.025 -h 1.83 -r # [1,100]
python generate.py -i rtss -n 25 -s 10 -f 0.025 -h 1.83 -r # [1,100]

sleep 1
