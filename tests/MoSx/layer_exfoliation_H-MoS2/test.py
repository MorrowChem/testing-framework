from utilities import relax_config
import numpy as np
import model
import os
from ase.io import read, write


bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))
bulk.set_calculator(model.calculator)

fmax = 0.01
bulk = relax_config(bulk, relax_pos=True, relax_cell=True, tol=fmax)

# set up supercell
bulk *= (1, 1, 1)


def surface_energy(bulk, opening):
    Nat = bulk.get_number_of_atoms()

    ebulk = bulk.get_potential_energy()
    print('bulk cell energy', ebulk)

    bulk.positions[np.argwhere(bulk.get_scaled_positions()[:, 2] > 0.5)] += [0.0, 0.0, opening/2]
    bulk.cell[2, :] += [0.0, 0.0, opening]
    
    eexp  = bulk.get_potential_energy()

    print('expanded cell energy', eexp)
    e_form = (eexp - ebulk) / (bulk.cell[1,1]*bulk.cell[0,0])
    print('unrelaxed 001 surface formation energy', e_form)
    return e_form

n_steps = 35
max_opening = 8.0
min_opening = -1

al = []

openings = []
es = []
for i in range(n_steps + 1):
    opening = float(i)/float(n_steps)*(max_opening - min_opening) + min_opening
    openings.append(opening)
    bulk_copy = bulk.copy()
    bulk_copy.set_calculator(model.calculator)
    al.append(bulk_copy)
    es.append(surface_energy(bulk_copy, opening))

es = np.array(es)
print('Min opening was ', bulk.cell[2,2] - openings[np.argmin(es)])

write('exfoliation_001.xyz', al)

properties = {'openings': openings, 'es': (es - es[-1]).tolist(), 'init_sep': bulk.cell[2, 2]/2}
