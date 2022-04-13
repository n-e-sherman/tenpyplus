
from ._base import Observer
import pandas as pd
import numpy as np

class StaggeredFieldObserver(Observer):

	def observe(self, obj):

		psi = obj.psi
		model = obj.model
		m = 0
		E = np.mean(model.bond_energies(psi))
		Xs = psi.expectation_value('Sigmax')
		for i,X in enumerate(Xs):
			m += (-1.0)**(i+1)*X
		labels = {'t': [model.t], 'm': [m], 'E': [E]}
		return pd.DataFrame(labels)

	@property
	def mongo_type(self):
	    from ._data import MongoStaggeredFieldObserver
	    return MongoStaggeredFieldObserver