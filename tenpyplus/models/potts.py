from ._base import Model, DynamicModel

from tenpy.networks.site import SpinHalfSite, SpinSite
from tenpy.models.model import NearestNeighborModel, CouplingMPOModel
import numpy as np

class _Potts(CouplingMPOModel, NearestNeighborModel):

    def __init__(self, model_params):
 
        super().__init__(self.model_params)
        self._label_skips += ['Jf','gf']
        self.name = 'Potts'


    def init_sites(self, model_params):
        conserve = model_params.get('conserve', None) # what to do here?
        site = SpinSite(conserve=conserve, s=1)
        Omega = [[1,0,0],[0,np.exp(1j*2*np.pi/3),0],[0,0,np.exp(-1j*2*np.pi/3)]]
        Omegadag = [[1,0,0],[0,np.exp(-1j*2*np.pi/3),0],[0,0,np.exp(1j*2*np.pi/3)]]
        Gamma = [[0,1,1],[1,0,1],[1,1,0]]
        site.add_op('Omega', Omega)
        site.add_op('Omegadag', Omegadag)
        site.add_op('Gamma', Gamma)
        return site
    
    def init_terms(self, model_params):

        J = self.J = model_params['J']
        g = self.h = model_params['g']

        if not h == 0:
            for i in range(L):
                self.add_onsite_term(-g, i, 'Gamma')
        if not J == 0:
            for i in range(L-1):
                self.add_coupling_term(-J, i, i+1, 'Omega', 'Omegadag')
                self.add_coupling_term(-J, i, i+1, 'Omegadag', 'Omega')

class PottsModel(Model, _XX):
    
    def __init__(self, **data):

        super().__init__(**data)
        _Potts.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'g': data.get('g',1)})

    @property
    def mongo_type(self):
        from ._data import MongoXXModel
        return MongoXXModel

class DynamicPottsModel(DynamicModel, _XX):

    def __init__(self, **data):

        super().__init__(**data)
        _Potts.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'g': data.get('g',1)})
        self._data.update({'J0': data.get('J0',self._data['J']), 'Jf' : data.get('Jf',self._data['J']),
                           'g0': data.get('g0',self._data['h']), 'gf' : data.get('hf',self._data['h'])})
        self._query_skips += ['J','h']

    def set_params_func(self):

        self.params_func = {
            'J': self.path.make_function(self.J0, self.Jf), 
            'g': self.path.make_function(self.g0, self.gf)
        }

    @property
    def mongo_type(self):
        from ._data import MongoDynamicXXModel
        return MongoDynamicXXModel