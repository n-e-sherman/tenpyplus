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
	print('v:', options['path_options']['v'])
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
	options['global_options'] = {'chi' : 64}
	options['model_options'] = {
		'type': 'XX', 
		'dynamic': True, 
		'conserve': None,
		'h0': 1, 'hf': 0,
		'J0': 0, 'Jf': 1,
		'L': 129,
		'bc_MPS': 'finite',
	}
	# options['model_options'] = {
	# 	'type': 'XX', 
	# 	'dynamic': True, 
	# 	'conserve': None,
	# 	'h0': 1, 'hf': 0,
	# 	'J0': 0, 'Jf': 1,
	# 	'L': 2,
	# 	'bc_MPS': 'infinite',
	# }
	options['repository_options'] = {'load': True}
	options['observer_options'] = {'type': 'StaggeredField'}
	options['path_options'] = {'type': 'Direct', 'v': 1.0}
	options['product_options'] = {'type': 'rightleft'}
	# options['product_options'] = {'type': 'leftright'}
	options['state_options'] = {'type': 'KZM', 'initial': 'Product'}
	options['measurement_options'] = {'type': 'XXSineGordonMass'}

	# gs = [0.5, 1.0, 1.5]
	# hs = [0, -0.5, 0.5]
	vs = 1.0 / np.array([2**x for x in range(10,14)])
	hs = [0]
	args = []
	for v in vs:
		arg = options.copy()
		path_options = arg['path_options'].copy()
		path_options['v'] = v
		arg['path_options'] = path_options.copy()
		args.append(arg)
	# p = multiprocessing.Pool(cores)
	# p.map(run, args[node::nodes], chunksize=1)
	[run(arg) for arg in args[node::nodes]]





if __name__ == '__main__':
    main()


