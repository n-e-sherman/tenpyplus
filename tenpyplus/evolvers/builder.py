from .tebd import TEBDEvolver
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
		elif choice == 'None':
			return Evolver(**options)
		else:
			raise NotImplementedError('evolver choice ' + choice + ' not implemented.')


