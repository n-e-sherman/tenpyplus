from tenpyplus.infrastructure import Object
import os

class Measurement(Object):

	def __init__(self, **data):
		super().__init__(**data)

	def measure(self, repo):
		pass

	def _dir_choice(self, data_dir, res_dir):
		return os.path.join(res_dir, self.name)

	@property
	def mongo_type(self):
		from ._data import MongoMeasurementBase
		return MongoMeasurementBase

	@property
	def pickle_type(self):
		return 'data_frame'
	

	