
from tenpyplus.infrastructure import Object

class Evolver(Object):
    
    def __init__(self, **data):
        super().__init__(**data)
        self.options = data

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'dt': data.get('dt',0.1)})

    def evolve(self, psi, model):
        return psi

    @property
    def mongo_type(self):
        from ._data import MongoEvolverBase
        return MongoEvolverBase

    
