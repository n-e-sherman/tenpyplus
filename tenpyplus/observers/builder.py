from ._data import *
from tenpyplus.infrastructure import Builder, Options
from .staggeredfield import StaggeredFieldObserver

class ObserverBuilder(Builder):

	
	def build(self, options = {}):

		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('observer_options',{}))
		params.update(options)
		options = params.copy()

		choice = options['type'] = options.get('type', 'Identity')

		if choice == 'StaggeredField':
			return StaggeredFieldObserver(**options)
		elif choice == 'Identity':
			return Observer(**options)

		else:
			raise NotImplementedError('model choice ' + choice + ' not implemented.')



