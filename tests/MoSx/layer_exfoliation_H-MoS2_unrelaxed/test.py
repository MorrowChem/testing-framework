from utilities import relax_config
import numpy as np
import model
import os
from ase.io import read, write

directory = os.getcwd()
i=0
model.calculator.directory = directory + '/s{:04d}'.format(i)
bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))
bulk.set_calculator(model.calculator)

#fmax = 0.01
#bulk = relax_config(bulk, relax_pos=True, relax_cell=True, tol=fmax)

# set up supercell
bulk *= (1, 1, 1)
ebulk = bulk.get_potential_energy()
print('bulk cell energy', ebulk)

def surface_energy(bulk, opening, bulk_energy):
    Nat = bulk.get_number_of_atoms()

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
    model.calculator.set(directory=model.calculator.directory[:-4] + '{:04d}'.format(i+1))
    print(model.calculator.directory)
    bulk_copy.set_calculator(model.calculator)
    al.append(bulk_copy)
    es.append(surface_energy(bulk_copy, opening, ebulk))

es = np.array(es)
print('Min opening was ', bulk.cell[2,2] - openings[np.argmin(es)])

write('exfoliation_001.xyz', al)

properties = {'openings': openings, 'es': (es - es[-1]).tolist(), 'init_sep': bulk.cell[2, 2]/2}
