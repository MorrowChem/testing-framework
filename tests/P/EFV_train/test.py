from utilities import path_of_file, evaluate_file
import os

filenamelist = ["P20_liq_12_03_01_liqP4.xyz", "P20_liq_12_03_02_network.xyz",
                "P20_norss.xyz", "P20_random_kfolds_big.xyz",
                "P20_random_kfolds_small.xyz",  "P20_rss_3c.xyz"
                ]

for filename in filenamelist:
    evaluate_file(path_of_file(__file__)+"/"+filename)

properties = {"files": filenamelist}
