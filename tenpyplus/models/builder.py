from .ising import IsingModel, DynamicIsingModel
from .xx import XXModel, DynamicXXModel
from .paths import PathBuilder

from tenpyplus.infrastructure import Builder, Options

class ModelBuilder(Builder):

	def __init__(self):
		self.pathBuilder = PathBuilder()

	def build(self, options = {}):
		
		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('model_options',{}))
		params.update(options)
		options = params.copy()
		
		choice = options['type'] = options.get('type', 'Ising')

		dynamic = options.get('dynamic', False)

		if choice == 'Ising':
			if dynamic:
				options['path'] = self.pathBuilder.build(options.get('path_options', {}))
				model = DynamicIsingModel(**options) # define path

				return model
			return IsingModel(**options)

		elif choice == 'XX':
			if dynamic:
				options['path'] = self.pathBuilder.build(options.get('path_options', {}))
				return DynamicXXModel(**options) # define path
			return XXModel(**options)

		else:
			raise NotImplementedError('model choice ' + choice + ' not implemented.')



