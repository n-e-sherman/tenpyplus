from tenpyplus.infrastructure import Object

class Measurement(Object):

	def __init__(self, **data):
		super().__init__(**data)

	def measure(self, repo):
		pass

	@property
	def mongo_type(self):
		from ._data import MongoMeasurementBase
		return MongoMeasurementBase