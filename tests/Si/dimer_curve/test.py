import model
from ase.io import read, write
from ase import Atoms
import numpy as np


mi = 1.4; ma = 5.4; n=20

########################################

pos = np.array([[0, 0, 0], [0, 0, 10.]])
at = Atoms('SiSi', positions=pos, cell=20*np.identity(3), pbc=True)
at.calc = model.calculator
e0 = at.get_potential_energy()
traj = []
es = []

x = np.linspace(mi, ma, n)
for i in x:
    pos[1, 2] = i
    at_copy = at.copy()
    at.set_positions(pos)

    traj.append(at_copy)
    es.append(at.get_potential_energy())

write('./dimer_traj.xyz', traj)
es = np.array(es) - e0

print('Separations ', x)
print("Energies ", es)
# from scipy import interpolate
# spline = interpolate.splrep(x, es, s=0)

properties = {'dimer_separations': x.tolist(), 'dimer_energies': es.tolist()}