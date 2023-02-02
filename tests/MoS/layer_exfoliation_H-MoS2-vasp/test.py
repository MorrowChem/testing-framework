import numpy as np
import model
import os
from os.path import join
from ase.io import read, write
from warnings import warn


bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))
bulk.set_calculator(model.calculator)

### relax bulk with VASP internal algo
if hasattr(model, "relax"):
    if model.relax:
        print("Relaxing bulk")
        orig_dir = './'
        model.calculator.set(ibrion=2, nsw=100, ediffg=-0.005, kspacing=0.3, directory='geom_relax') 
        
        if not os.path.exists(join(model.calculator.directory, 'CONTCAR')):
            bulk.calc = model.calculator
            bulk.get_potential_energy()
        else:
            print('Relaxation already done, reading and skipping')

        bulk = read(join(model.calculator.directory, "CONTCAR"), index=-1)
        model.calculator.set(ibrion=-1, nsw=-1, kspacing=model.kspacing_value)
        print('Bulk successfully relaxed')
else:
    print("Skipping bulk relaxation, assuming already relaxed")

# set up supercell
bulk *= (1, 1, 1)


def surface_energy(bulk, opening):
    Nat = bulk.get_number_of_atoms()

    try:
        ebulk = bulk.get_potential_energy()
        print('bulk cell energy', ebulk)
    except:
        warn('Energy calculation failed for some reason - if SCAN+mbd then this is normal')
        ebulk = np.NaN

    bulk.positions[np.argwhere(bulk.get_scaled_positions()[:, 2] > 0.5)] += [0.0, 0.0, opening/2]
    bulk.cell[2, :] += [0.0, 0.0, opening]
    
    try:
        eexp  = bulk.get_potential_energy()
        print('expanded cell energy', eexp)
    except:
        warn('Energy calculation failed for some reason - if SCAN+mbd then this is normal')
        eexp = np.NaN

    e_form = (eexp - ebulk) / (bulk.cell[1,1]*bulk.cell[0,0])
    print('unrelaxed 001 surface formation energy', e_form)
    return e_form

n_steps = 12
max_opening = 5.0
min_opening = -0.5

al = []

openings = []
es = []
for i in range(n_steps + 1):
    opening = float(i)/float(n_steps)*(max_opening - min_opening) + min_opening
    openings.append(opening)
    bulk_copy = bulk.copy()
    model.calculator.set(directory=f'{i}')
    bulk_copy.set_calculator(model.calculator)
    al.append(bulk_copy)
    es.append(surface_energy(bulk_copy, opening))

es = np.array(es)
print('Min opening was ', bulk.cell[2,2] - openings[np.argmin(es)])

write('exfoliation_001.xyz', al)

properties = {'openings': openings, 'es': (es - es[-1]).tolist(), 'init_sep': bulk.cell[2, 2]/2}
