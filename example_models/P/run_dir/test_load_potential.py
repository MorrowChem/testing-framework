from quippy.potential import Potential
from sys import argv
from ase.io import read

pot = Potential(param_filename=argv[1])
at = read('/home/magnetite/vld/hert5155/applications/testing-framework/tests/P/bulk_betaP4/bulk.xyz')
at.calc = pot
print(at.get_potential_energy())
