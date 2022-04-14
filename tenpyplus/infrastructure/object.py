import mongoengine
from typing import Any

class Object:

	_query = None
	_data = {}
	_query_skips = []
	_label_skips = []

	def __getattr__(self, attr: str) -> Any:
	    if attr in self._data:
	        return self._data.get(attr)
	    return self.__getattribute__(attr)

	def __setattr__(self, key: str, value: Any) -> None:
	    if key in self._data:
	        self._data[key] = value
	    else:
	        super().__setattr__(key, value)

	def __init__(self, **data):

		self._set_data(**data)

	def _set_data(self, **data):
		self._data = {}
		self._query_skips = []
		self._label_skips = ['name']
		self._query = None
		self._data['name'] = data.get('type', data.get('name', self.__class__.__name__))


	def construct(self):

		for k,v in self._data.items():
			if isinstance(v, Object):
				self._data[k].construct()

	def update(self, **data):

		for k,v in data.items():
			if isinstance(v, dict):
				self._data[k].update(**v)
			else:
				self.__setattr__(k,v)

	def to_dict(self):
		data = {}
		for k,v in self._data.items():
			if v is None:
				continue
			if isinstance(v, Object):
				data[k] = v.to_dict()
			else:
				data[k] = v
		return data

	def to_mongo_dict(self):
		data = {}
		for k,v in self._data.items():
			if v is None:
				continue
			if isinstance(v, Object):
				data[k] = v.to_mongo()
			else:
				data[k] = v
		return data

	def to_mongo(self):
		data = {}
		for k,v in self._data.items():
			if v is None:
				continue
			if isinstance(v, Object):
				data[k] = v.to_mongo()
			else:
				data[k] = v
		return self.mongo_type(**data)

	def get_query(self, tag=''):

		if self._query is not None:
			return self._query
		query = {}
		for k,v in self._data.items():
			if (k in self._query_skips) or (v is None):
				continue
			key = tag + k
			if isinstance(v, Object):
				embedded_query = v.get_query(tag=key+'__')
				query.update(embedded_query)
			else:
				query[key] = v
		self._query = query
		return query

	def get_labels(self):
		labels = {}
		for k,v in self._data.items():
			if v is None or k in self._label_skips:
				continue
			if isinstance(v, Object):
				_labels = v.get_labels()
				for _k, _v in _labels.items():
					labels[_k] = _v
				labels[k] = v.name
			else:
				labels[k] = v
		return labels

	def mongo_resolve_multiple(self, documents):
		return documents.first()

	def copy(self):

		data = self._data.copy()
		return type(self)(**data)
				
	def _dir_choice(self, data_dir, res_dir):
		return data_dir

	@property
	def mongo_type(self):
		return mongoengine.Document

	@property
	def pickle_type(self):
		return 'check_point'

	










