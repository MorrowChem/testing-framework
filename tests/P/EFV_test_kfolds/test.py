from utilities import path_of_file, evaluate_file
import os

filenamelist = [f'P20_small_{i}.xyz' for i in range(6)]

for filename in filenamelist:
    evaluate_file(path_of_file(__file__)+"/"+filename)

properties = {"files": filenamelist}
