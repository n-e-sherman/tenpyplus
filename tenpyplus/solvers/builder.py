from .dmrg import DMRGSolver
from tenpyplus.infrastructure import Builder, Options

class SolverBuilder(Builder):

	def __init__(self):
		pass

	def build(self, options = {}):

		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('solver_options',{}))
		params.update(options)
		options = params.copy()

		choice = options['type'] = options.get('type', 'DMRG')
		if choice == 'DMRG':
			return DMRGSolver(**options)
		else:
			raise NotImplementedError('solver choice ' + choice + ' not implemented.')


