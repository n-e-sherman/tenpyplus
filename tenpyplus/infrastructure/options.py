from tenpyplus.infrastructure import Object
import os
from copy import deepcopy

class Options(Object):

	__instance = None
	@staticmethod 
	def get_instance():
		""" Static access method. """
		if Options.__instance == None:
			Options()
		options = Options.__instance
		if os.getpid() not in options._data:
			options._set_defaults()
		return options

	def __init__(self):

		if not Options.__instance is None:
			raise Exception("This class is a singleton!")
		else:
			self._set_defaults()
			Options.__instance = self

	def reset(self):
		self._set_defaults()

	def update(self, options={}):
		data = self._data[os.getpid()]

		for k,v in options.items():
			if isinstance(v, dict) and k in data:
				data[k].update(v)
			else:
				data[k] = v

		self.make_uniform(data)
		self._data[os.getpid()] = data

	def get_data(self):
		data = deepcopy(self._data[os.getpid()].copy())
		return data

	def _set_defaults(self):

		data = {}

		data['global_options'] = {
			'chi': 10,
			'dt': 0.1
		}
		data['tebd_options'] = {
			'type': 'TEBD',
		    'order': 2,
		    'N_steps': 1,
		    'compression_method': 'variational',
		    'trunc_params': {
		        'chi_max': 10,
		        'chi_min': 10,
		        'degeneracy_tol': 0,
		        'svd_min': 0,
		        'trunc_cut': 0
		    }
		}
		data['evolver_options'] = data['tebd_options'].copy()

		data['dmrg_options'] = {
			'type': 'DMRG',
			'sites': 2,
		    'mixer': True, 
		    'trunc_params': {
		        'chi_max': 10,
		        'chi_min': 10,
		        'degeneracy_tol': 0,
		        'svd_min': 0,
		        'trunc_cut': 0
		    }
		}
		data['solver_options'] = data['dmrg_options'].copy()

		data['kzm_options'] = {
			'type': 'KZM',
			'initial': 'Product',
		}
		data['ground_options'] = {
			'type': 'Ground',
			'initial': 'Product',
		}
		data['state_options'] = data['ground_options'].copy()

		data['product_options'] = {
			'type': 'random'
		}

		data['observer_options'] = {
			'type': 'Identity',

		}

		data['model_options'] = {
			'type': 'Ising',
			'L': 2,
			'bc_MPS': 'infinite',
			'conserve': None,
			'J': 1.0,
			'g': 1.0,
			'h': 0.0
		}

		data['path_options'] = {
			'type': 'Direct',
			'v': 0.5,
			'ramp': 'linear',
			'dt': 0.1,
		}

		data['repository_options'] = {
			'type': 'Mongo',
			'data_dir': '.data/',
			'res_dir': '.results/'
		}

		data['measurement_options'] = {
			'type': 'IsingCritical'
		}
		self.make_uniform(data)
		self._data[os.getpid()] = data

	def make_uniform(self, data):
		# data['evolver_options']['trunc_params']['chi_min'] = data['solver_options']['trunc_params']['chi_min'] = data['global_options']['chi']
		data['evolver_options']['trunc_params']['chi_max'] = data['solver_options']['trunc_params']['chi_max'] = data['global_options']['chi']
		data['path_options']['dt'] = data['evolver_options']['dt'] = data['global_options']['dt']
