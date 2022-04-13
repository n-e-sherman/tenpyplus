import mongoengine
import os
import pandas as pd
from tenpyplus.infrastructure import Object

class MongoBase:

	_object = Object
	load_failed = False

	name = mongoengine.StringField()
	converted = mongoengine.BooleanField(default=False)
	new = mongoengine.BooleanField(default=True)

	def __init__(self, *args, **kwargs):
	            
	    # super().__init__(*args, **kwargs)
	    self.name = kwargs.get('name', self._object.__name__)


		    

	def to_dict(self):
		self.load_failed = False
		return self._to_dict()

	def to_object_dict(self):
	    self.load_failed = False
	    return self._to_object_dict()

	def to_object(self):
	    data = self._to_object_dict()
	    return self._object(**data)

	def _to_dict(self):
		data = self.to_mongo().to_dict()
		if '_id' in data:
			del data['_id']
		return data

	def _to_object_dict(self):
		data = self.to_mongo().to_dict()
		if '_id' in data:
			del data['_id']
		return data

	def to_df(self):
		data = self._to_dict()
		res = {}
		for k,v in data.items():
			if isinstance(v, dict):
				res[k] = v.pop('name')
				res.update(v)
			else:
				res[k] = v
		return pd.DataFrame([res])

	@classmethod
	def from_object(cls, obj):
		data = obj.to_dict()
		doc = cls(**data)
		doc.save()
		return doc



class MongoDynamicEmbeddedDocument(mongoengine.DynamicEmbeddedDocument, MongoBase):

	meta = {'allow_inheritance': True}


class MongoDynamicDocument(mongoengine.DynamicDocument, MongoBase):

	meta = {'allow_inheritance': True}
