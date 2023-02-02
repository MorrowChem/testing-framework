import numpy as np
from ase.io import read
import os
from warnings import warn
from os.path import join
from utilities import path_of_file
from traceback import print_exc

import model

if not hasattr(model.calculator, 'VASP_PP_PATH'):
    raise TypeError('this test is only designed to work with VASP')

filenamelist = ['m-m-bonding_MPatoms.xyz']
ats = read(path_of_file(__file__)+"/"+filenamelist[0], ':')

print("Relaxing bulk")
orig_dir = './'
model.calculator.set(ibrion=2, nsw=100, ediffg=-0.005, 
                    kspacing=0.3, kpar=1, ncore=1, npar=model.nmpi)

try:
    ids = [at.info['mpid'] for at in ats]
except:
    ids = ['id'] * len(ats)

relaxed = []
nsteps = []
for i, at in enumerate(ats):
    model.calculator.set(directory=f'{i}-{ids[i]}')
    if not os.path.exists(join(model.calculator.directory, 'CONTCAR')):
        at.calc = model.calculator
        try:
            at.get_potential_energy()
        except:
            warn(f'Relaxation failed, skipping {i} {ids[i]} structure')
            print_exc()

        try:
            nstep = len(read(join(model.calculator.directory, "XDATCAR"), index=':'))
            nsteps.append(nstep)
            relaxed.append(read(join(model.calculator.directory, "CONTCAR"), index=-1))
        except:
            warn(f'Relaxation failed, skipping {i} {ids[i]} structure')
            print_exc()

    else:
        print('Relaxation already done, reading and skipping')
        bulk = read(join(model.calculator.directory, "CONTCAR"), index=-1)

    print(f'{i}-{ids[i]} successfully relaxed')

if relaxed == []:
    raise ValueError('No structures relaxed, calculation failed')
    
properties = {'relaxed_structure': relaxed, 'nsteps': nsteps}