from .ground import GroundState
from .kzm import KZMState
from tenpyplus.infrastructure import Builder, Options
from tenpyplus.models import ModelBuilder
from tenpyplus.solvers import SolverBuilder
from tenpyplus.evolvers import EvolverBuilder
from tenpyplus.observers import ObserverBuilder
from tenpyplus.repositories import RepositoryBuilder

from tenpy.networks.mps import MPS
import numpy as np
import random

class StateBuilder(Builder):

	def __init__(self):
		self.modelBuilder = ModelBuilder()
		self.solverBuilder = SolverBuilder()
		self.evolverBuilder = EvolverBuilder()
		self.observerBuilder = ObserverBuilder()
		self.productBuilder = ProductBuilder()
		self.repoBuilder = RepositoryBuilder()

	def build(self, options = {}):
		
		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('state_options',{}))
		params.update(options)
		options = params.copy()

		choice = options['type'] = options.get('type', 'Ground')

		
		print(options)
		repo = self.repoBuilder.build(options.get('repository_options',{}))
		if choice == 'Ground':
			options['model'] = self.modelBuilder.build(options.get('model_options', {}))
			options['psi0'] = self.productBuilder.build({**options.get('product_options', {}), **{'lattice': options['model'].lat}})
			options['solver'] = self.solverBuilder.build(options.get('solver_options', {}))
			product_options = options.get('product_options', _options.get('product_options', {}))
			options['initial'] = product_options.get('type', 'random')
			state = GroundState(**options)
			if not repo.load(state):
				state.calculate(repo)


		elif choice == 'KZM':
			options['model'] = self.modelBuilder.build({**options.get('model_options', {}), **{'dynamic': True}})
			options['observer'] = self.observerBuilder.build(options.get('observer_options', {}))
			options['evolver'] = self.evolverBuilder.build(options.get('evolver_options', {}))
			product_options = options.get('product_options', _options.get('product_options', {}))
			options['initial'] = product_options.get('type', 'random')
			state = KZMState(**options)
			if not repo.load(state):
				psi = self._make_initial(options)
				state.update(psi=psi)
			state.calculate(repo)

		else:
			raise NotImplementedError('state choice ' + choice + ' not implemented.')

		return state



	def _make_initial(self, options):

		initial = options.get('initial','Product')
		if initial == 'Ground':
			state = self.build({**options.get('ground_options',{}), **{'type': 'Ground'}})
			return state.psi
		return self.productBuilder.build(options.get('product_options',{}))


class ProductBuilder(Builder):

	def __init__(self):
		self.modelBuilder = ModelBuilder()


	def build(self, options = {}):

		_options = Options.get_instance().get_data()
		params = _options.get('global_options',{})
		params.update(_options.get('product_options',{}))
		params.update(options)
		options = params.copy()

		if 'lattice' not in options:
			model = options.get('model', self.modelBuilder.build(options.get('model_options', {})))
			options['lattice'] = model.lat
		lattice = options['lattice']
		cell = self._make_cell(options.get('type', 'random'), lattice)
		return self._make_product(lattice, cell)

	def _make_product(self, lattice, cell):

		L = lattice.N_sites
		product_state = (cell * L)[:L]
		return MPS.from_product_state(lattice.mps_sites(), product_state, bc=lattice.bc_MPS)

	def _make_random_product(self, lattice):
		cell = []
		for site in lattice.unit_cell:
		    site_tensor = np.array([random.uniform(0,1) for _ in range(site.dim)])
		    site_tensor = site_tensor / np.linalg.norm(site_tensor)
		    cell.append(site_tensor)
		return cell
	def _make_all_product(self, lattice):
		cell = []
		for site in lattice.unit_cell:
		    site_tensor = np.array([1.0 for _ in range(site.dim)])
		    site_tensor = site_tensor / np.linalg.norm(site_tensor)
		    cell.append(site_tensor)
		return cell

	def _make_cell(self, choice, lattice):

		if choice == 'random':
			return self._make_random_product(lattice)
		elif choice == 'all':
			return self._make_all_product(lattice)
		elif choice == 'up':
			return ['up']
		elif choice == 'down':
			return ['up']
		elif choice == 'updown':
			return ['up','down']
		elif choice == 'downup':
			return ['down','up']
		elif choice == 'right':
			return [np.array([1.0/np.sqrt(2), 1.0/np.sqrt(2)])]
		elif choice == 'left':
			return [np.array([1.0/np.sqrt(2), -1.0/np.sqrt(2)])]
		elif choice == 'rightleft':
			return [np.array([1.0/np.sqrt(2), 1.0/np.sqrt(2)]), np.array([1.0/np.sqrt(2), -1.0/np.sqrt(2)])]
		elif choice == 'leftright':
			return [np.array([1.0/np.sqrt(2), -1.0/np.sqrt(2)]), np.array([1.0/np.sqrt(2), 1.0/np.sqrt(2)])]
		elif choice == 'all':
			return [np.array([1.0/np.sqrt(2), -1.0/np.sqrt(2)]), np.array([1.0/np.sqrt(2), 1.0/np.sqrt(2)])]
		else:
			raise NotImplementedError('product choice ' + choice + ' not implemented.')
