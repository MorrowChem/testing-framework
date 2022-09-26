import os.path
from RSS import do_RSS
from ml_rss import ML_RSS
import numpy as np
from ase.units import mol
import utilities

# mr = ML_RSS(None, directory=os.path.join(os.path.abspath(os.path.dirname(__file__))))

# buildcell_options = ['NATOM=1-10', f'VARVOL={volume}', 'MINSEP=2.0', 'SYMMOPS=1-4', 'SPECIES=P']
# buildcell_atoms=[]
# tag='P_GAP20'
# N=50
# mr.buildcells(N, buildcell_options, buildcell_atoms, tag)
# write(os.path.join(os.path.abspath(os.path.dirname(__file__)),'random_structs.xyz'), )
# volume = 1/2.34 * (1e8)**3 / mol * 30.9736
# ps = np.genfromtxt(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rand_pressures_512_0.3GPa.txt'))
index = utilities.index
print('doing index ', index)

properties = do_RSS(os.path.join(os.path.abspath(os.path.dirname(__file__)),'random_structs_10k.xyz'), index)
