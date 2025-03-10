from utilities import relax_config
import numpy as np
import model
import os
from ase.io import read, write

n_steps = 12
max_opening = 1/7.5
min_opening = 0

##########################


bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))
bulk.set_calculator(model.calculator)

fmax = 0.01
bulk = relax_config(bulk, relax_pos=True, relax_cell=True, tol=fmax)


# set up supercell
bulk *= (2, 2, 1)

def surface_slip_energy(bulk, slide):
    Nat = bulk.get_number_of_atoms()

    ebulk = bulk.get_potential_energy()
    print('bulk cell energy', ebulk)
    pos = bulk.get_scaled_positions()
    pos[np.argwhere(pos[:, 2] > 0.5)] += [slide, -slide, 0]
    bulk.set_scaled_positions(pos)
    


    # bulk.cell[2, :] += [0.0, 0.0, 0.0]
    
    eexp  = bulk.get_potential_energy()

    print('expanded cell energy', eexp)
    e_form = (eexp - ebulk) / (bulk.cell[1,1]*bulk.cell[0,0])
    print('unrelaxed 001 surface formation energy', e_form)
    return e_form


slide_al = []

slides = []
slide_es = []
for i in range(n_steps + 1):
    slide = float(i)/float(n_steps)*(max_opening - min_opening) + min_opening
    slides.append(slide)
    bulk_copy = bulk.copy()
    bulk_copy.set_calculator(model.calculator)
    slide_al.append(bulk_copy)
    slide_es.append(surface_slip_energy(bulk_copy, slide))

write('slide_11b0.xyz', slide_al)

properties = {'slide_path': slides, 'es': (slide_es - slide_es[0]).tolist()}
