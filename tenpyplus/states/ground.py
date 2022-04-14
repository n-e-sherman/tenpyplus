from ._base import State


class GroundState(State):

	def __init__(self, **data):

		super().__init__(**data)

	def _set_data(self, **data):
		super()._set_data(**data)
		self._data.update({'initial': data.get('initial',None),
						   'model': data.get('model',None), 
						   'solver': data.get('solver',None),
						   'initial'
						   'E0': None})
		self.psi0 = data.get('psi0', None)

	def calculate(self, repo):

		print('finding ground state for model: ', self.model.model_params)
		self.E0, self.psi = self.solver.solve(self.psi0, self.model)
		print('done')
		print('*'*80)
		repo.save(self)

	@property
	def mongo_type(self):
	    from ._data import MongoGroundState
	    return MongoGroundState

		