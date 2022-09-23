from utilities import path_of_file, evaluate_file
import os

filenamelist = ["P20_liq_12_03_01_liqP4_complement.xyz", "P20_liq_12_03_02_network_complement.xyz",
                "P20_norss_complement.xyz", "P20_random_kfolds_big_complement.xyz",
                "P20_random_kfolds_small_complement.xyz",  "P20_rss_3c_complement.xyz",
                "P_test_set.xyz"]

for filename in filenamelist:
    evaluate_file(path_of_file(__file__)+"/"+filename)

properties = {"files": filenamelist}
