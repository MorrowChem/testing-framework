from utilities import path_of_file, evaluate_file, model_test_root, name_of_file
import numpy as np

filenamelist = ['mp_MoSx.xyz']
ats = []
for filename in filenamelist: 
    ats.append(evaluate_file(path_of_file(__file__)+"/"+filename))



properties = {"files": [model_test_root()+"/"+filename for filename in filenamelist],
              "es": [[j.get_potential_energy() for j in i] for i in ats],
              "forces": [[j.get_forces().tolist() for j in i] for i in ats],
              "ls": [[len(j) for j in i] for i in ats]}

 