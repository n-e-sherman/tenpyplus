
from tenpyplus.infrastructure import Builder, Options
from tenpyplus.states import StateBuilder
from tenpyplus.repositories import RepositoryBuilder
from .measurement import IsingCriticalMeasurement, StateMeasurement, XXSineGordonMassMeasurement, KZMSweepMeasurement


class MeasurementBuilder(Builder):

	def __init__(self):
		self.stateBuilder = StateBuilder()
		self.repoBuilder = RepositoryBuilder()

	def build(self, options = {}):

		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('measurement_options',{}))
		params.update(options)
		options = params.copy()

		repo = self.repoBuilder.build(options.get('repository_options',{}))
		choice = options['type'] = options.get('type', 'IsingCritical')
		if choice == 'KZMSweep':
			options['state'] = self.stateBuilder.build({**options.get('state_options', {}), **{'type': 'KZM'}})
			measurement = KZMSweepMeasurement(**options)
		elif choice == 'IsingCritical':
			options['state'] = self.stateBuilder.build({**options.get('state_options', {}), **{'type': 'Ground'}})
			measurement = IsingCriticalMeasurement(**options)
		elif choice == 'StateMeasurement':
			options['state'] = self.stateBuilder.build(options.get('state_options', {}))
			measurement = StateMeasurement(**options)
		elif choice == 'XXSineGordonMass':
			options['state'] = self.stateBuilder.build(options.get('state_options', {}))
			measurement = XXSineGordonMassMeasurement(**options)
		else:
			raise NotImplementedError('measurement choice ' + choice + ' not implemented.')
		measurement.measure(repo)
		return measurement