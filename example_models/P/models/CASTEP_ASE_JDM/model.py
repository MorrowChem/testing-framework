import os
from distutils import spawn
from ase.calculators.castep import Castep

model_abs_dir = os.path.abspath(os.path.dirname(__file__))

mpirun = "mpirun"
mpirun_args = "-n 16"
castep = "castep.mpi"

os.environ['CASTEP_COMMAND'] = 'module load use.local && module load intel/2019 && export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 && {0} {1} {2}'.format(mpirun, mpirun_args, castep)

no_checkpoint = True

def start(test_name):
    global calculator
    calculator = Castep(directory=test_name,
                        cut_off_energy=500,
                        spin_polarized=False,
                        opt_strategy='speed',
                        xc_functional='PBE',
                        elec_energy_tol=1e-6,
                        max_scf_cycles=250,
                        fix_occupancy=False,
                        calculate_stress=True,
                        finite_basis_corr='automatic',
                        smearing_width='0.05',
                        #fine_grid_scale=1,
                        mixing_scheme='pulay',
                        mix_history_length=20,
                        num_dump_cycles=0,
                        kpoints_mp_spacing='0.050', # note that other values were used for some tests, e.g. 0.015 for bulk E(V), 0.07 for minimization of GAP amorphous structures, and perhaps some other variations
                        species_pot = ("P","{}/P_OTF.usp".format(model_abs_dir)),
                        perc_extra_bands=200)
