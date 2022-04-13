from tenpyplus.infrastructure import Builder, Options
from .mongo import MongoRepository
from ._base import Repository

class RepositoryBuilder(Builder):

	def build(self, options = {}):
		
		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('repository_options',{}))
		params.update(options)
		options = params.copy()

		choice = options['type'] = options.get('type', 'Mongo')
		if choice == 'Mongo':
			return MongoRepository(options)
		elif choice == 'None':
			return Repository(options)
		else:
			raise NotImplementedError('repository choice ' + choice + ' not implemented.')

