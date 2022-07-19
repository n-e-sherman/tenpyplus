from .tebd import TEBDEvolver
from .utebd import UTEBDEvolver
from .tebdvar import TEBDVarEvolver
from .wii import WIIEvolver
from ._base import Evolver
from tenpyplus.infrastructure import Builder, Options

class EvolverBuilder(Builder):

	def __init__(self):
		pass

	def build(self, options = {}):
		
		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('evolver_options',{}))
		params.update(options)
		options = params.copy()
		
		choice = options['type'] = options.get('type', 'TEBD')
		
		if choice == 'TEBD':
			return TEBDEvolver(**options)
		if choice == 'UTEBD':
			return UTEBDEvolver(**options)
		if choice == 'TEBDVar':
			return TEBDVarEvolver(**options)
		elif choice == 'WII':
			return WIIEvolver(**options)
		elif choice == 'None':
			return Evolver(**options)
		else:
			raise NotImplementedError('evolver choice ' + choice + ' not implemented.')


