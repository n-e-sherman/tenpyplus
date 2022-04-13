#### TEMPORARY ####
import sys, os
sys.path.append(os.path.join(os.getcwd(), '..', 'tenpyplus'))
sys.path.append(os.path.join(os.getcwd(), '..'))
###################

import multiprocessing
import os
import time
import numpy as np
from tenpyplus.infrastructure import Options
from tenpyplus.measurements import MeasurementBuilder



# Main work
def run(options):
	print('g:', options['model_options']['g'], 'h:', options['model_options']['h'], 'chi:', options['global_options']['chi'])
	_options = Options.get_instance()
	_options.update(options)
	measurement = MeasurementBuilder().build(options)

def main():


	cores = 1
	nodes = 1
	node = 0
	if len(sys.argv) > 1:
	    cores = int(sys.argv[1])
	if len(sys.argv) > 2:
	    nodes = int(sys.argv[2])
	if len(sys.argv) > 3:
	    node = int(sys.argv[3])

	options = {}
	options['global_options'] = {'chi' : 50}
	options['model_options'] = {'type': 'Ising', 'dynamic': False, 'conserve': None}
	options['state_options'] = {'type': 'Ground'}
	options['measurement_options'] = {'type': 'IsingCritical'}

	gs = np.array(list(np.linspace(0.5, 1.5, 101)) + list(np.linspace(0,0.5,51)) + list(np.linspace(1.5,2,51)))
	hs = np.array([0] + list(np.linspace(-0.5,0.5,101)) + list(np.linspace(-1,-0.5,51)) + list(np.linspace(0.5,1,51)))
	# gs = [0.5, 1.0, 1.5]
	# hs = [0, -0.5, 0.5]
	hs = [0]
	args = []
	for g in gs:
		for h in hs:
			arg = options.copy()
			model_options = arg['model_options'].copy()
			model_options['g'] = g
			model_options['h'] = h
			arg['model_options'] = model_options.copy()
			args.append(arg)
	# p = multiprocessing.Pool(cores)
	# p.map(run, args[node::nodes], chunksize=1)
	[run(arg) for arg in args[node::nodes]]





if __name__ == '__main__':
    main()


