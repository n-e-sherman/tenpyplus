from ._base import Evolver
import tenpyplus.evolvers as evolvers

from tenpy.algorithms import tebd

class TEBDVarEvolver(Evolver):
    
    def __init__(self, **data):
        super().__init__(**data)
        
        
    def _set_data(self, **data):
        super()._set_data(**data)
        data['compression_method'] = 'variational'
        self._data.update({'order' : data.get('order',2), 'optimum': False})
        self.options = {}
        self.options.update(data)
        if self.order == '4_opt':
            self._data['optimum'] = True
            self.order = 4
        
    def evolve(self, psi, model):
        chi_max = self.options['trunc_params']['chi_max']
        self.options['trunc_params']['chi_max'] = int(10*chi_max)
        eng = tebd.TEBDEngine(psi, model, self.options)
        eng.run()
        self.options['trunc_params']['chi_max'] = chi_max
        psi.compress(self.options)
        return psi
    
    @property
    def mongo_type(self):
        from ._data import MongoTEBDVarEvolver
        return MongoTEBDVarEvolver

