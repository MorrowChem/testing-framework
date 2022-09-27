import traceback
import ase.io
from utilities import robust_minim_cell_pos
import numpy as np
import traceback

def do_RSS(initial_configs_file, index=':', tol=0.01, ps=0.0):
    import model

    ats = ase.io.read(initial_configs_file, index)
    range_slice_args = [ None if i == '' else int(i) for i in index.split(':')]

    print("got index ", index, "range_slice_args",range_slice_args)
    print("using i_config",range(len(ats))[slice(*range_slice_args)])

    energies = []
    volumes = []
    N = len(ats)
    fac=0.1; inc=0.1
    i_selection = np.arange(*range_slice_args)
    print(i_selection)

    for (i_config, at) in zip(range(len(ats))[slice(*range_slice_args)], ats):
        gi_config = i_selection[i_config]
        try:
            if str(type(model.calculator)) == "<class 'ase.calculators.castep.Castep'>":
                model.calculator._label = str(gi_config)
            robust_minim_cell_pos(at, tol, "RSS_%04d" % gi_config)
            print("RSS completed minimization", flush=True)
            if hasattr(model, "fix_cell_dependence"):
                model.fix_cell_dependence()
            energies.append(at.get_potential_energy()/len(at))
            volumes.append(at.get_volume()/len(at))
            ase.io.write("RSS_relaxed_%04d.extxyz" % gi_config, at)
            print(f'{gi_config+1}/{N}')
            if (gi_config+1)/len(ats) > fac:
                print('{:3.0f}% done'.format(fac), end='\r', flush=True)
                fac += inc
        except:
            print(f'Failed on {gi_config}', flush=True)
            traceback.print_exc()
            energies.append(np.NaN)
            volumes.append(np.NaN)


    return { 'energies' : energies, 'volumes' : volumes }
