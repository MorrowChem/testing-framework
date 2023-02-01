import model
from ase.io import read, write
from ase import Atoms
import numpy as np
from warnings import warn


mi = 1.4; ma = 5.4; n=20

########################################

pos = np.array([[0, 0, 0], [0, 0, 10.]])
Mo2 = Atoms('Mo2', positions=pos, cell=20*np.identity(3), pbc=True)
MoS = Atoms('MoS', positions=pos, cell=20*np.identity(3), pbc=True)
S2 = Atoms('S2', positions=pos, cell=20*np.identity(3), pbc=True)
names = ['Mo2', 'MoS', 'S2']
ats = [Mo2, MoS, S2]

#########################################

# for i in range(len(ats)):
#     ats[i].calc = model.calculator

for at in ats:
    model.calculator.set(directory=f'e0_{str(at.symbols)}')
    at.calc = model.calculator
    e0s = at.get_potential_energy()

traj = [[] for at in ats]
es = [[] for at in ats]

x = np.linspace(mi, ma, n)
for ct, i in enumerate(x):
    pos[1, 2] = i
    ats_copy = [at.copy() for at in ats]
    for i in range(len(ats)):
        at_c = ats[i].copy()
        at_c.set_positions(pos)
        traj[i].append(ats_copy[i])
        model.calculator.set(directory=f'{i}')
        at_c.calc = model.calculator

        try:
            es[i].append(at_c.get_potential_energy())
        except:
            warn('didn\'t work for ', i)
        write('./dimer_traj_f{names[i]}.xyz', traj[i])

es = np.array(es) - np.array(e0s)[:, np.newaxis]

print('Separations ', x)
print("Energies ")
for i in range(len(ats)):
    print(names[i], ' ', es[i])
# from scipy import interpolate
# spline = interpolate.splrep(x, es, s=0)

properties = {'dimer_separations': x.tolist()}
properties.update({f'{names[i]}_dimer_energies': es[i].tolist() for i in range(len(ats))})