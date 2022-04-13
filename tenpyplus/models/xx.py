from ._base import Model, DynamicModel

from tenpy.networks.site import SpinHalfSite
from tenpy.models.model import NearestNeighborModel, CouplingMPOModel
import numpy as np

class _XX(CouplingMPOModel, NearestNeighborModel):

    def __init__(self, model_params):
 
        super().__init__(self.model_params)
        self._label_skips += ['Jf','hf']
        self.name = 'XX'


    def init_sites(self, model_params):
        conserve = model_params.get('conserve', None)
        site = SpinHalfSite(conserve=conserve)
        Hadamard = [[1.0/np.sqrt(2), 1.0/np.sqrt(2)], [1.0/np.sqrt(2), -1.0/np.sqrt(2)]]
        site.add_op('Hadamard', Hadamard)
        return site
    
    def init_terms(self, model_params):

        L = self.L = model_params['L']
        J = self.J = model_params['J']
        h = self.h = model_params['h']

        if not h == 0:
            for i in range(L):
                self.add_onsite_term(h*(-1.0)**(i+1), i, 'Sigmax')
        if not J == 0:
            for i in range(L-1):
                self.add_coupling_term(J, i, i+1, 'Sigmax', 'Sigmax')
                self.add_coupling_term(J, i, i+1, 'Sigmay', 'Sigmay')

class XXModel(Model, _XX):
    
    def __init__(self, **data):

        super().__init__(**data)
        _XX.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'h': data.get('h',1)})

    @property
    def mongo_type(self):
        from ._data import MongoXXModel
        return MongoXXModel

class DynamicXXModel(DynamicModel, _XX):

    def __init__(self, **data):

        super().__init__(**data)
        _XX.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'h': data.get('h',1)})
        self._data.update({'J0': data.get('J0',self._data['J']), 'Jf' : data.get('Jf',self._data['J']),
                           'h0': data.get('h0',self._data['h']), 'hf' : data.get('hf',self._data['h'])})
        self._query_skips += ['J','h']

    def set_params_func(self):

        self.params_func = {
            'J': self.path.make_function(self.J0, self.Jf), 
            'h': self.path.make_function(self.h0, self.hf)
        }

    @property
    def mongo_type(self):
        from ._data import MongoDynamicXXModel
        return MongoDynamicXXModel