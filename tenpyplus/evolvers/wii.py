from ._base import Evolver
import tenpyplus.evolvers as evolvers

from tenpy.algorithms.mpo_evolution import ExpMPOEvolution

class WIIEvolver(Evolver):
    
    def __init__(self, **data):
        super().__init__(**data)
        
        
    def _set_data(self, **data):
        super()._set_data(**data)
        data['compression_method'] = data.get('compression_method', data.get('compression', 'variational'))
        self._data.update({'order' : data.get('order',2), 'compression' : data.get('compression_method', 'variational')})
        data['approximation'] = 'II'
        self.options = {}
        self.options.update(data)
        if not ( (self.order == 1) or (self.order == 2) ):
            self.order = 2
        
    def evolve(self, psi, model):
        eng = ExpMPOEvolution(psi, model, self.options)
        eng.run()
        return psi
    
    @property
    def mongo_type(self):
        from ._data import MongoWIIEvolver
        return MongoWIIEvolver

