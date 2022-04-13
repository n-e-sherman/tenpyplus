from ._base import Model, DynamicModel

from tenpy.networks.site import SpinHalfSite
from tenpy.models.model import NearestNeighborModel, CouplingMPOModel
import numpy as np

class _Ising(CouplingMPOModel, NearestNeighborModel):

    def __init__(self, model_params):
        super().__init__(self.model_params)
        self._label_skips += ['Jf','gf','hf']
        self.name = 'Ising'


    def init_sites(self, model_params):
        conserve = model_params.get('conserve', None)
        site = SpinHalfSite(conserve=conserve)
        return site
    
    def init_terms(self, model_params):

        J = self.J = model_params['J']
        g = self.g = model_params['g']
        h = self.h = model_params['h']

        # onsite
        if (h != 0) or (g != 0 ):
            for u in range(len(self.lat.unit_cell)):
                self.add_onsite(-g, u, 'Sigmaz')
            for u in range(len(self.lat.unit_cell)):
                self.add_onsite(-h, u, 'Sigmax')

        # couplings
        if not J == 0:
            for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
                self.add_coupling(-J, u1, 'Sigmax', u2, 'Sigmax', dx)

    def exact_energy(self):
        from scipy.special import ellipe, ellipk
        J = self.J
        g = self.g
        if not J==0:
            return -J*(2.0/np.pi)*abs(1.0+(g/J))*ellipe(4.0*(g/J)/((1.0+(g/J))**2))
        else:
            return -g

class IsingModel(Model, _Ising):

    def __init__(self, **data):

        super().__init__(**data)
        _Ising.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'g': data.get('g',0), 
                           'J': data.get('J',1), 
                           'h': data.get('h',0)})

    @property
    def mongo_type(self):
        from ._data import MongoIsingModel
        return MongoIsingModel


class DynamicIsingModel(DynamicModel, _Ising):

    def __init__(self, **data):
        super().__init__(**data)
        _Ising.__init__(self, self.model_params)
        self.update_couplings(t=self.t)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'g': data.get('g',data.get('g0',0)), 
                           'J': data.get('J',data.get('J0',1)), 
                           'h': data.get('h',data.get('h0',0))})
        self._data.update({'g0': data.get('g0',self._data['g']), 'gf' : data.get('gf',self._data['g']),
                           'J0': data.get('J0',self._data['J']), 'Jf' : data.get('Jf',self._data['J']),
                           'h0': data.get('h0',self._data['h']), 'hf' : data.get('hf',self._data['h'])})
        self._query_skips += ['g','J','h']


    def set_params_func(self):

        self.params_func = {
            'J': self.path.make_function(self.J0, self.Jf), 
            'g': self.path.make_function(self.g0, self.gf), 
            'h': self.path.make_function(self.h0, self.hf)
        }

    @property
    def mongo_type(self):
        from ._data import MongoDynamicIsingModel
        return MongoDynamicIsingModel


