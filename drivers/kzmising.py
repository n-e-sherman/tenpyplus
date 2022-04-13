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
from copy import deepcopy



# Main work
def run(options):
	print('v:', options['path_options']['v'], 'chi:', options['global_options']['chi'])
	_options = Options.get_instance()
	_options.reset()
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


	choice = 'critical' # 'symmetric', 'off'
	ramp = 'smooth'
	options = {}
	options['global_options'] = {'chi' : 10}
	if choice == 'critical':
		options['model_options'] = {'type': 'Ising', 'dynamic': True, 'conserve': 'parity', 'g0': 2, 'gf': 1, 'J0': 0, 'Jf': 1, 'h': 0}
		options['path_options'] = {'v': 1, 'ramp': ramp}
	elif choice == 'symmetric': 
		options['model_options'] = {'type': 'Ising', 'dynamic': True, 'conserve': 'parity', 'g0': 2, 'gf': 0, 'J0': 0, 'Jf': 2, 'h': 0}
		options['path_options'] = {'v': 1, 'ramp': ramp}
	elif choice == 'off':
		options['model_options'] = {'type': 'Ising', 'dynamic': True, 'conserve': 'parity', 'g0': 2, 'gf': 0.5, 'J0': 0, 'Jf': 1.5, 'h': 0}
		options['path_options'] = {'v': 1, 'ramp': ramp}
	else:
		raise NotImplementedError('job choice ' + choice + ' not implemented.')
	options['evolver_options'] = {'type': 'TEBD', 'order': '4_opt'}
	options['product_options'] = {'type': 'up'}
	options['state_options'] = {'type': 'KZM'}
	options['measurement_options'] = {'type': 'KZMSweep'}

	vi = 1E-5
	vf = 0.5
	Nv = 50
	x = np.log(vf/vi)/(Nv-1)
	vs = [vi*np.exp(n*x) for n in range(Nv)][::-1]
	# vs = vs[35:]
	chis = [2*(1+x) for x in range(10)]

	# vs = [0.5]
	# chis = [10]
	args = []
	for v in vs:
		for chi in chis:
			arg = options.copy()
			global_options = deepcopy(arg['global_options'].copy())
			path_options = deepcopy(arg['path_options'].copy())
			path_options['v'] = v
			global_options['chi'] = chi
			arg['path_options'] = deepcopy(path_options.copy())
			arg['global_options'] = deepcopy(global_options.copy())
			args.append(arg)
	p = multiprocessing.Pool(cores)
	p.map(run, args[node::nodes], chunksize=1)
	# [run(arg) for arg in args[node::nodes]]





if __name__ == '__main__':
	main()


