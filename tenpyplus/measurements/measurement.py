
from ._base import Measurement
from tenpyplus.models import IsingModel
import pandas as pd
import numpy as np

class StateMeasurement(Measurement):

	def _set_data(self, **data):
		super()._set_data(**data)
		self._state = data.get('state', None)
	
	def measure(self, repo):

		psi = self._state.psi
		M = self._state.model
		E = np.mean(M.bond_energies(psi))
		Sx = np.mean(psi.expectation_value('Sx'))
		Sy = np.mean(psi.expectation_value('Sy'))
		Sz = np.mean(psi.expectation_value('Sz'))
		S = np.mean((psi.entanglement_entropy()))
		xi = psi.correlation_length()
		res = {
				   'E': E, 
				   'S': S, 
				   'Sx': Sx, 
				   'Sy': Sy, 
				   'Sz': Sz, 
				   'xi': xi
			   }
		res.update(self._state.get_labels())
		res['state'] = self._state.name
		self._data.update(res)
		repo.save(self)

	@property
	def mongo_type(self):
		from ._data import MongoStateMeasurement
		return MongoStateMeasurement

class IsingCriticalMeasurement(Measurement):

	def _set_data(self, **data):
		super()._set_data(**data)
		self._state = data.get('state', None)
		self._query_skips += ['E0', 'Ec', 'S']

	def measure(self, repo):

		psi = self._state.psi
		model_params = {'J': 1.0, 'g': 1.0, 'h': 0.0}
		data = self._state.model._data.copy()
		model = IsingModel(**data)
		model.update_couplings(**model_params)
		Ec = np.mean(model.bond_energies(psi))
		S = np.mean((psi.entanglement_entropy()))
		res= {'Ec': Ec, 'S': S}
		res.update(self._state.get_labels())
		res['state'] = self._state.name
		self._data.update(res)
		repo.save(self)

	@property
	def mongo_type(self):
		from ._data import MongoIsingCriticalMeasurement
		return MongoIsingCriticalMeasurement

class KZMSweepMeasurement(Measurement):

	# This is defined by the KZM state, use the parameters of the KZM state to compute the ground state

	def _set_data(self, **data):
		super()._set_data(**data)
		self._state = data.get('state', None)
		self._query_skips += ['l', 'Ep', 'Ec', 'E0']

	def measure(self, repo):

		from tenpyplus.states import StateBuilder
		psit = self._state.psi
		model_options = self._state.model.to_dict()
		model_options['dynamic'] = False
		model_options['type'] = model_options['name']
		model_options['conserve'] = 'parity'
		product_options = {'type': self._state.initial}
		ground_state = StateBuilder().build(options={'type': 'Ground', 'model_options': model_options, 'product_options': product_options})
		psi0 = ground_state.psi

		model = ground_state.model
		l = abs(psi0.overlap(psit))
		Ep = np.mean(model.bond_energies(psit))
		Ec = np.mean(model.bond_energies(psi0))
		E0 = model.exact_energy()
		res = {'l': l, 'Ep': Ep, 'E0': E0, 'Ec': Ec}
		print(res)
		res.update(self._state.get_labels())
		res['state'] = self._state.name
		res['conserve'] = ground_state.model.conserve
		self._data.update(res)

		repo.save(self)

	@property
	def mongo_type(self):
		from ._data import MongoKZMSweepMeasurement
		return MongoKZMSweepMeasurement

class XXSineGordonMassMeasurement(Measurement):

	def _set_data(self, **data):
		super()._set_data(**data)
		self._state = data.get('state', None)
		self._query_skips += ['E', 'm']

	def measure(self, repo):
		psi = self._state.psi
		model = self._state.model
		
		E = np.mean(model.bond_energies(psi))
		Xs = psi.expectation_value('Sigmax')
		m = 0
		for i,X in enumerate(Xs):
			m += (-1.0)**(i+1)*X
		res= {'E': E, 'm': m}
		res.update(self._state.get_labels())
		res['state'] = self._state.name
		self._data.update(res)
		repo.save(self)

	@property
	def mongo_type(self):
		from ._data import MongoXXSineGordonMassMeasurement
		return MongoXXSineGordonMassMeasurement

class IsingGroundStateOverlapMeasurement(Measurement):

	def _set_data(self, **data):
		super()._set_data(**data)
		self._state = data.get('state', None)
		self._query_skips += ['O']

	def measure(self, repo):
		from tenpyplus.states import MongoGroundState

		psi = self._state.psi
		chi_max = int(self._state.chi)
		query = {
		    'chi': 50,
		    'model__conserve': 'None',
		    'model__name': 'Ising',
		    'model__J': 1.0,
		}
		# gs = np.array(list(np.linspace(0.5, 1.5, 101)) + list(np.linspace(0,0.5,51)) + list(np.linspace(1.5,2,51)))
		# hs = np.array([0] + list(np.linspace(-0.5,0.5,101)) + list(np.linspace(-1,-0.5,51)) + list(np.linspace(0.5,1,51)))
		gs = np.array(list(np.linspace(0.5, 1.5, 101)))
		hs = np.array([0] + list(np.linspace(-0.5,0.5,101)))
		for h in hs:
			for g in gs:
				print('h:',h,'g:',g,end='\r')
				query['model__g'] = g
				query['model__h'] = h
				doc = MongoGroundState.objects(**query).first()
				state = doc.to_object()
				phi = state.psi
				phi.compress({'trunc_params': {'chi_max': chi_max},
							  'compression_method': 'variational'})
				O = abs(psi.overlap(phi))
				mc = np.mean(psi.expectation_value('Sx'))
				m = np.mean(phi.expectation_value('Sx'))
				res = self._state.get_labels().copy()
				res.update({'O': O, 'g': g, 'h': h, 'mc': mc, 'm': m})
				res['state'] = self._state.name
				self._data.update(res)
				repo.save(self)

	def get_query(self, tag=''):

		query = {}
		for k,v in self._data.items():
			if (k in self._query_skips) or (v is None):
				continue
			query[k] = v
		self._query = query
		return query

	@property
	def mongo_type(self):
		from ._data import MongoIsingGroundStateOverlapMeasurement
		return MongoIsingGroundStateOverlapMeasurement

		        
