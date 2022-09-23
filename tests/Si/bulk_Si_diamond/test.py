import os.path, lattice
from utilities import relax_config

properties = lattice.do_lattice(os.path.abspath(os.path.dirname(__file__)), 'cubic')
