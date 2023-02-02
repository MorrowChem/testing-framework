import numpy as np
from ase.io import read
import os
from utilities import path_of_file

import model

if not hasattr(model.calculator, 'VASP_PP_PATH'):
    raise TypeError('this test is only designed to work with VASP')

model.calculator.set(ediff=min(model.calculator.asdict()['inputs']['ediff'], 1e-6))
print('ediff is set to', model.calculator.asdict()['inputs']['ediff'])

bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))

kpts_range = np.linspace(0.5, 0.08, 8)
cutoff_range = np.linspace(100, 800, 8)

if hasattr(model, "kspacing_value"):
    default_kspacing = model.kspacing_value
else:
    default_kspacing = kpts_range[len(kpts_range)//2]

es_kpts = []; es_cutoff = []
for i, kpts in enumerate(kpts_range):
    model.calculator.set(kspacing=kpts, directory=f'kpts/{i}')
    bulk_copy = bulk.copy()
    bulk_copy.set_calculator(model.calculator)
    es_kpts.append(bulk_copy.get_potential_energy())

print('Testing cutoffs')
for i, cutoff in enumerate(cutoff_range):
    model.calculator.set(encut=cutoff, kspacing=default_kspacing, directory=f'cutoffs/{i}')
    bulk_copy = bulk.copy()
    bulk_copy.set_calculator(model.calculator)
    es_cutoff.append(bulk_copy.get_potential_energy())


# print a formatted table with columns kpts, es_kpts
print('kpts', 'es_kpts')
for k, e in zip(kpts_range, es_kpts):
    print('{:10.4f}    {:10.4f}'.format(k, e))
    
# print a table with columns cutoff, es_cutoff
print('cutoff', 'es_cutoffs')
for c, e in zip(cutoff_range, es_cutoff):
    print('{:10.4f}    {:10.4f}'.format(c, e))

properties = {'kpts': kpts_range, 'cutoff': cutoff_range, 'es_kpts': es_kpts, 'es_cutoff': es_cutoff}


