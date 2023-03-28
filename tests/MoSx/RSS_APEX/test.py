import numpy as np
import os
from ase.io import read, write

from utilities import model_test_root
import model

from apex.buildcells import RSS
from apex.md import lammps_nvt_meltquench, lammps_multijob
from apex.optimization import lammps_optimization

print('Running buildcell')

dir = os.getcwd() # will be run_root by the time this is called
rss = RSS(dir, buildcell_command='buildcell')

N = 10000
p = 0 # pressure / GPa
if 'NSLOTS' in os.environ:
    nprocs = int(os.environ['NSLOTS'])
else:
    nprocs = 20
## RSS settings ##
r1=1.45
r2=1.00
r_char = (r1 + r2)/2 # mean covalent radius of Mo and S
volume_factor = 14.5
bc_opts_narrow = ['VARVOL={}'.format(r_char**3 * volume_factor),
                'SYMMOPS=1-8',
                'NFORM={1,2,3,4,5,6,7,8,9,10}',
                'SLACK=0.25',
                'OVERLAP=0.1',
                'COMPACT',
                'MINSEP={}, Mo-Mo={} S-S={} Mo-S={}'.format(min(r1,r2)*1.8, r1*1.8, r2*1.8, 2),
                'SPECIES=Mo%NUM=1,S%NUM=2']

rss.buildcells(N, bc_opts_narrow, tag='MoS2', nprocs=nprocs)
atoms = rss.init_atoms['MoS2']
write('MoS2_rss_init.xyz', atoms)


print('Doing minimisations')
min_kwargs = {
    'hookean_params': {'spring': [20, 20, 20], 'threshold': [1.6, 1.6, 1.6]},
    'pair_style':   'quip',
    'pair_coeff':   f'* * {model.param_filename} \"\" 42 16',
    'steps':        50,
    'timestep':     0.001, # in ps
    'nevery':       1,
    'directory':    'lammps_minimize',
    'logfile':      'min.log',

    'min_style':    'cg',
    'etol':         1e-6,
    'ftol':         1e-5,
    'maxeval':      100000,
    }

min_kwargs['pressures'] = np.random.exponential(p, len(atoms))
min_atoms_par = lammps_multijob(lammps_optimization, nprocs=nprocs, 
                               atoms=atoms, tag='MoS2',
                               **min_kwargs)

rss_structures = [i[-1] for i in min_atoms_par]
write('rss_minimized.xyz', rss_structures)             

properties = {"files": ['MoS2_rss_init.xyz'],
              "es": [j.info['energy'] for j in rss_structures],
              "local_energies": [j.arrays['c_pe_at'].tolist() for j in rss_structures],
              "ls": [len(j) for j in rss_structures],}