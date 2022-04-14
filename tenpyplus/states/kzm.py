from ._base import State
import pandas as pd
import numpy as np


class KZMState(State):

	def __init__(self, **data):
		super().__init__(**data)
		

	def _set_data(self, **data):
		super()._set_data(**data)
		self._data.update({'initial' : data.get('initial', None),
						   'model': data.get('model',None), 
						   'evolver': data.get('evolver',None),
						   'observer': data.get('observer',None),
						   'log': None})
		self.state = data.get('state', None)
		self._label_skips += ['observer','log']
		self._query_skips += ['log']

	def calculate(self, repo):

		ts = self.model.path_times()
		for t in ts:
			self.model.update_couplings(t=t)
			self.psi = self.evolver.evolve(self.psi, self.model)
			self._observe()
			print('t0:', round(self.model.path.t0), 't:', round(t,3), 'tf:', round(self.model.path.tf,3), np.mean(self.model.bond_energies(self.psi)), self.model.exact_energy())
			repo.save(self)

	def _observe(self):

		df_observation = self.observer.observe(self)
		if df_observation is not None:
			if self.log is None:
				self.log = df_observation
			else:
				self.log = pd.concat([self.log, df_observation])

	def mongo_resolve_multiple(self, documents):
		document = documents[0]
		for doc in documents:
			if doc.model.t > document.model.t:
				document = doc
		return document

	@property
	def mongo_type(self):
	    from ._data import MongoKZMState
	    return MongoKZMState




