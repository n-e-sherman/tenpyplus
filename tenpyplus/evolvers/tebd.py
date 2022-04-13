from ._base import Evolver
import tenpyplus.evolvers as evolvers

from tenpy.algorithms import tebd

class TEBDEvolver(Evolver):
    
    def __init__(self, **data):
        super().__init__(**data)
        
        
    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'order' : data.get('order',2), 'optimum': False})
        self.options = {}
        self.options.update(data)
        if self.order == '4_opt':
            self._data['optimum'] = True
            self.order = 4
        
    def evolve(self, psi, model):
        eng = tebd.TEBDEngine(psi, model, self.options)
        eng.run()
        return psi
    
    @property
    def mongo_type(self):
        from ._data import MongoTEBDEvolver
        return MongoTEBDEvolver

