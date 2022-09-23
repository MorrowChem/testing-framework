import os.path, lattice
from os.path import join
from ase.io import read

bulks = read(join(os.path.abspath(os.path.dirname(__file__)), 'prototypes.xyz'), index=':')
properties = {}
for i, val in enumerate(bulks):
    ev = lattice.calc_E_vs_V
