from tenpyplus.infrastructure import Object
from tenpy.networks.mps import TransferMatrix
import pandas as pd

class Observer(Object):

	def __init__(self, **data):
		super().__init__(**data)

	def observe(self, obj):
		return None

	@property
	def mongo_type(self):
	    from ._data import MongoObserverBase
	    return MongoObserverBase
