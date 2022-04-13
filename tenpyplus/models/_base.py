from tenpyplus.infrastructure import Object
from tenpy.models.lattice import Site, Chain
from tenpy.networks.site import SpinHalfSite
from tenpy.models.model import CouplingModel, NearestNeighborModel, MPOModel, CouplingMPOModel
import numpy as np

class Model(Object):

    default_lattice = 'Chain'
    manually_call_init_H = True

    def __init__(self, **data):
        super().__init__(**data)


    def _set_data(self, **data):
        super()._set_data(**data)
        if 'bc_MPS' in data:
            bc = data.pop('bc_MPS')
            data['bc'] = bc
        data['conserve'] = str(data.get('conserve',None))
        self._data.update({'L': data.get('L',2), 
                           'conserve': data['conserve'], 
                           'bc': data.get('bc','infinite')})
        
    # def exact_energy(self):
    #     return 0

    @property
    def model_params(self):
        model_params = self._data.copy()
        if 'bc' in model_params:
            bc = model_params.pop('bc')
            model_params['bc_MPS'] = bc
        if model_params.get('conserve', None) == 'None':
            model_params['conserve'] = None
        return model_params

    def update_couplings(self, **params):
        self.update(**params)
        # self._data.update(params)
        self.options.update(params)
        self.onsite_terms = {}
        self.coupling_terms = {}
        self.init_terms(self.model_params)
        self.init_H_from_terms()

    @property
    def mongo_type(self):
        from ._data import MongoModelBase
        return MongoModelBase


class DynamicModel(Model):

    def __init__(self, **data):
    
        super().__init__(**data)
        self._query_skips.append('t')
        self.set_params_func()
        
    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'path' : data.get('path',None), 
                           't' : data.get('t', None)})
        if self.t is None and self.path:
            self.t = self.path.t0

    def path_times(self):

        return self.path.ts[self.path.ts > self.t]

    def update_couplings(self, **params):

        if 't' in params:
            self.t = params['t']
            params = self._time_couplings(self.t)
        super().update_couplings(**params)

    def _time_couplings(self, t):

        params = {}
        for k,v in self.params_func.items():
            params[k] = v(t)
        return params

    def set_params_func(self):
        self.params_func = {}

    @property
    def mongo_type(self):
        from ._data import MongoDynamicModelBase
        return MongoDynamicModelBase
