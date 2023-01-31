from utilities import relax_config
import numpy as np
import model
import os
from os.path import join
from ase.io import read, write
from warnings import warn

n_steps = 12
max_opening = 1/7.5
min_opening = 0

##########################


bulk = read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MoS2-2H.xyz'))
bulk.set_calculator(model.calculator)

# fmax = 0.01

### relax bulk with VASP internal algo
if hasattr(model, "relax"):
    if model.relax:
        print("Relaxing bulk")
        orig_dir = './'
        model.calculator.set(ibrion=2, nsw=100, ediffg=-0.005, kspacing=0.3, directory='geom_relax') 
        
        if not os.path.exists(join(model.calculator.directory, 'CONTCAR')):
            try:
                bulk.calc = model.calculator
                bulk.get_potential_energy()
            except:
                pass
        else:
            print('Relaxation already done, reading and skipping')

        bulk = read(join(model.calculator.directory, "CONTCAR"), index=-1)
        model.calculator.set(ibrion=-1, nsw=-1, kspacing=model.kspacing_value)
        print('Bulk successfully relaxed')
else:
    print("Skipping bulk relaxation, assuming already relaxed")


# set up supercell
# bulk *= (2, 2, 1)

def surface_slip_energy(bulk, slide):
    # TODO implement a version that relaxes the surface at each step
    Nat = bulk.get_number_of_atoms()
    try:
        ebulk = bulk.get_potential_energy()
        print('bulk cell energy', ebulk)
    except:
        warn('Energy calculation failed for some reason - if SCAN+mbd then this is normal')
        ebulk = np.NaN

    pos = bulk.get_scaled_positions()
    pos[np.argwhere(pos[:, 2] > 0.5)] += [slide, -slide, 0]
    bulk.set_scaled_positions(pos)
    # bulk.cell[2, :] += [0.0, 0.0, 0.0]
    try:
        eexp  = bulk.get_potential_energy()
        print('expanded cell energy', eexp)
    except:
        warn('Energy calculation failed for some reason - if SCAN+mbd then this is normal')
        eexp = np.NaN

    e_form = (eexp - ebulk) / (bulk.cell[1,1]*bulk.cell[0,0])
    print('unrelaxed 001 surface formation energy', e_form)
    return e_form


slide_al = []

slides = []
slide_es = []
for i, slide in enumerate(np.linspace(min_opening, max_opening, n_steps)):
    print(f'doing slide {i:00d} {slide:7.3f}')
    slides.append(slide)
    bulk_copy = bulk.copy()
    model.calculator.set(directory=f'{i}')
    bulk_copy.set_calculator(model.calculator)
    slide_al.append(bulk_copy)
    slide_es.append(surface_slip_energy(bulk_copy, slide))

write('slide_11b0.xyz', slide_al)

properties = {'slide_path': slides, 'es': (slide_es - slide_es[0]).tolist()}
