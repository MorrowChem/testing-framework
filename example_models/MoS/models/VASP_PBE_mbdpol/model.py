import sys, os
import numpy as np

from ase.calculators.vasp import Vasp

mydir=os.path.abspath(os.path.dirname(__file__))
relax=True

# VASP KSPACING units
kspacing_value=0.15
nmpi=8

# keywords related to this model (except k-points, which are handled separately)
vasp_keywords = { 'encut' : 300.0, 'xc' : 'PBE', 'ismear' : 0, 'sigma' : 0.1, 
                 'nelm' : 150, 'amix' : 0.03, 'bmix' : 0.01, 'pp':'pbe',
                 'ivdw': 263, 'vdw_sr':0.83, 'ialgo':58, 'istart':0, 'icharg':2, 'ispin':1}
# keywords related to accuracy
vasp_keywords.update( { 'ediff' : 1.0e-5, 'prec' : 'Accurate', 'addgrid' : False, 'lreal' : True } )
# keywords that should always be there
vasp_keywords.update( { 'ignore_constraints' : True, 'isif' : 3, 'isym' : 0 } )
# keywords related to parallelism.  Setting ncore sensibly is important for efficiency
#vasp_keywords.update( { 'lscalapack' : False, 'lplane' : False, 'kpar' : 10, 
    # 'ncore' : int(os.environ["VASP_NCORE"]) } )
vasp_keywords.update( { 'lscalapack' : True, 'lplane' : True, 'kpar' : 4, 
    'ncore' : nmpi } )

vasp_command =  ('module use /opt/intel/modulefiles && '
                'module load compiler mpi mkl && '
                'export OMP_NUM_THREADS={} && '
                'export MKL_NUM_THREADS={} && '
                'mpirun -np {} /usr/local/vasp.6.3.1/bin/vasp_std').format(1, 1, nmpi)

def wipe_restart(directory):
    try:
        os.unlink(os.path.join(directory,"WAVECAR"))
        sys.stderr.write("wiped {}\n".format(os.path.join(directory,"WAVECAR")))
    except FileNotFoundError:
        pass
    try:
        os.unlink(os.path.join(directory,"CHGCAR"))
        sys.stderr.write("wiped {}\n".format(os.path.join(directory,"CHGCAR")))
    except FileNotFoundError:
        pass

# default calculator to kspacing_value, gamma-centered
default_calculator = Vasp(command=vasp_command, kspacing=kspacing_value,kgamma=True, **vasp_keywords)
calculator = default_calculator

# wipe KPOINTS in case running in old dir and first run might be KSPACING based
try:
    os.unlink(os.path.join(calculator.directory,"KPOINTS"))
except FileNotFoundError:
    pass
wipe_restart(calculator.directory)

# monkey patch Vasp2.set_atoms to wipe restart files if major changes found
def vasp2_set_atoms(self, atoms):
    sys.stderr.write("monkey-patched set_atoms checking\n")
    if hasattr(self, "atoms") and atoms != self.atoms:
        sys.stderr.write("monkey-patched set_atoms trying to wipe\n")
        self.results = {}
        wipe_restart(self.directory)
    self.atoms = atoms.copy()
Vasp.set_atoms = vasp2_set_atoms

# explicitly set number of k-points from now on using kspacing_value, still gamma-centered
# driver will write KPOINTS file
# at=None undoes fixed k-points
def fix_cell_dependence(at=None):
    global calculator
    if at is None:
        calculator = default_calculator
        try:
            os.unlink(os.path.join(calculator.directory,"KPOINTS"))
        except:
            pass
        print("fix_cell_dependence() going back to default")
    else:
        bz_cell = at.get_reciprocal_cell()
        n_kpts = np.floor(np.linalg.norm(bz_cell,axis=1)*2.0*np.pi/kspacing_value).astype(int)+1
        print("fix_cell_dependence() got n_kpts", n_kpts,"from recip cell",bz_cell)
        calculator = Vasp(kpts=n_kpts, gamma=True, **vasp_keywords)

# want checkpointing, but broken now because of force_consistent
# no_checkpoint = False
no_checkpoint = True
name = 'VASP'
