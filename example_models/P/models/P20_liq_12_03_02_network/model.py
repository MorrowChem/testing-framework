import os

import sys; sys.path.insert(0, '/home/magnetite/vld/hert5155/QUIP_new/build/linux_x86_64_gfortran_openmp')
from quippy.potential import Potential
import builtins

orig_dir = os.getcwd()
model_dir = os.path.dirname(__file__)
if model_dir != '':
    os.chdir(model_dir)

#if os.path.exists('gp_iter6_sparse9k.xml.sparseX.GAP_2017_6_17_60_4_3_56_1651.bz2'):
#    os.system('bunzip2 gp_iter6_sparse9k.xml.sparseX.GAP_2017_6_17_60_4_3_56_1651.bz2')

try:
    if hasattr(builtins, 'mpi_glob'):
        calculator = Potential(param_filename='P20_liq_12_03_02_network.xml', mpi_obj=mpi_glob)
    else:
        calculator = Potential(param_filename='P20_liq_12_03_02_network.xml')

    Potential.__str__ = lambda self: '<GAP Potential>'
finally:
    os.chdir(orig_dir)

no_checkpoint = True

name = 'GAP'
