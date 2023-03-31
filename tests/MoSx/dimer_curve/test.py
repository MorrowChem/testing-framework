import model
from ase.io import read, write
from ase import Atoms
from ase.calculators.vasp import Vasp
import numpy as np
import os
from copy import deepcopy


directory = os.getcwd()
i=0
model.calculator.directory = directory + '/s{:04d}'.format(i)
mi = 1.0; ma = 5.5; n=50

if isinstance(model.calculator, Vasp):
    model.calculator.set(kspacing=100, nbands=24) # no need for kpoints, use exact diagonalization
    n = 30 # do fewer steps for VASP


########################################

pos = np.array([[0, 0, 0], [0, 0, 10.]])
Mo2 = Atoms('Mo2', positions=pos, cell=20*np.identity(3), pbc=True)
MoS = Atoms('MoS', positions=pos, cell=20*np.identity(3), pbc=True)
S2 = Atoms('S2', positions=pos, cell=20*np.identity(3), pbc=True)
names = ['Mo2', 'MoS', 'S2']
ats = [Mo2, MoS, S2]

#########################################

for i in range(len(ats)):
    calc = deepcopy(model.calculator)
    calc.set(directory=model.calculator.directory[:-4] + '{:04d}'.format(i+1))
    ats[i].calc = calc
    print('Setting original calc directory ', ats[i].calc._directory)

e0s = [at.get_potential_energy() for at in ats]

traj = [[] for at in ats]
es = [[] for at in ats]

x = np.linspace(mi, ma, n)
print('Separations ', x[0], ' to ', x[-1])

ats_copy = [at.copy() for at in ats]
for at_ct, at in enumerate(ats_copy):
    ats_copy[at_ct].calc = deepcopy(ats[at_ct].calc)
    ats_copy[at_ct].calc.set(directory= ats[at_ct].calc._directory + f'_0000')
for a in range(len(ats)):
    for ct, i in enumerate(x):
        pos[1, 2] = i
        ats_copy[a].set_positions(pos)
        traj[a].append(ats_copy[a])
        ats_copy[a].calc.set(directory=ats_copy[a].calc._directory[:-4] + f'{ct:04d}')
        print('setting ats_copy directory to ', ats_copy[a].calc._directory)
        es[a].append(ats_copy[a].get_potential_energy())
        write(f'./dimer_traj_f{names[i]}.xyz', traj[a])

es = np.array(es) - np.array(e0s)[:, np.newaxis]

print("Energies ")
for i in range(len(ats)):
    print(names[i], ' ', es[i])

properties = {'dimer_separations': x.tolist()}
properties.update({f'{names[i]}_dimer_energies': es[i].tolist() for i in range(len(ats))})
