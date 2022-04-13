
from tenpyplus.infrastructure import Object

class Solver(Object):

    def __init__(self, **data):
        super().__init__(**data)
        self.options = data

    def solve(self, psi, model):
        return None, psi
        
    @property
    def mongo_type(self):
        from ._data import MongoSolverBase
        return MongoSolverBase

