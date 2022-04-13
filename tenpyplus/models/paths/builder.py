from .path import DirectPath, SymmetricPath
from tenpyplus.infrastructure import Builder, Options

class PathBuilder(Builder):


	def build(self, options = {}):
		
		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('path_options',{}))
		params.update(options)
		options = params.copy()

		choice = options['type'] = options.get('type', 'Direct')
		if 'T' in options:
			T = options.pop('T')
			options['v'] = 1.0 / T
		if choice == 'Direct':
			return DirectPath(**options)
		elif choice == 'Symmetric':
			return SymmetricPath(**options)
		else:
			raise NotImplementedError('path choice ' + choice + ' not implemented.')


