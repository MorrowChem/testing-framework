import os

from mtp import MTP

orig_dir = os.getcwd()
model_dir = os.path.dirname(__file__)
gls = {'parallel': False, 'mtp_command': '/u/vld/hert5155/mlip-2/bin/mlp'}
mtp_filename = "g18_u20_fw0.1_direct.mtp"

if model_dir != '':
    os.chdir(model_dir)

try:
    calculator = MTP(os.path.join(model_dir, mtp_filename), **gls)
finally:
    os.chdir(orig_dir)

no_checkpoint = True

name = 'MTP_test'
