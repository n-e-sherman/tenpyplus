from ._base import Model, DynamicModel

from tenpy.networks.site import Site, SpinHalfSite, SpinSite
from tenpy.models.model import NearestNeighborModel, CouplingMPOModel
from tenpy.linalg import np_conserved as npc
import numpy as np

class PottsSite(Site):

    def __init__(self, conserve='Z3'):
        if not conserve:
            conserve = 'None'
        if conserve not in ['None','Z3']:
            raise ValueError("invalid `conserve`: " + repr(conserve))

        qcharges = np.array([0,1,2])
        Omega = Gamma1 = [[0,1,0],[0,0,1],[1,0,0]]
        Omegadag = Gamma2 = [[0,0,1],[1,0,0],[0,1,0]]
        Gamma = D = [[2,0,0],[0,-1,0],[0,0,-1]]
        ops = dict(Gamma1=Gamma1, Gamma2=Gamma2, D=D, Omega=Omega, Omegadag=Omegadag, Gamma=Gamma)
        if conserve == 'Z3':
            chinfo = npc.ChargeInfo([3], ['Z3_potts'])
            leg = npc.LegCharge.from_qflat(chinfo, np.array(qcharges, dtype=np.int64))
        else:
            leg = npc.LegCharge.from_trivial(3)
        self.conserve = conserve
        names = [str(i) for i in range(3)]
        Site.__init__(self, leg, names, **ops)

    def __repr__(self):
        """Debug representation of self."""
        return "PottsSite(conserve={c!r})".format(c=self.conserve)

class _Potts(CouplingMPOModel, NearestNeighborModel):

    def __init__(self, model_params):
 
        super().__init__(self.model_params)
        self._label_skips += ['Jf','gf']
        self.name = 'Potts'


    def init_sites(self, model_params):
        conserve = model_params.get('conserve', None) # what to do here?
        site = PottsSite(conserve=conserve)
        return site
    
    def init_terms(self, model_params):

        J = self.J = model_params['J']
        g = self.g = model_params['g']

        # onsite
        if not g == 0:
            for u in range(len(self.lat.unit_cell)):
                self.add_onsite(-g, u, 'D')

        # couplings
        if not J == 0:
            for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
                self.add_coupling(-J, u1, 'Gamma1', u2, 'Gamma2', dx)
                self.add_coupling(-J, u1, 'Gamma2', u2, 'Gamma1', dx)

class PottsModel(Model, _Potts):
    
    def __init__(self, **data):

        super().__init__(**data)
        _Potts.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'g': data.get('g',1)})

    @property
    def mongo_type(self):
        from ._data import MongoPottsModel
        return MongoPottsModel

class DynamicPottsModel(DynamicModel, _Potts):

    def __init__(self, **data):

        super().__init__(**data)
        _Potts.__init__(self, self.model_params)

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'J': data.get('J',1),
                           'g': data.get('g',1)})
        self._data.update({'J0': data.get('J0',self._data['J']), 'Jf' : data.get('Jf',self._data['J']),
                           'g0': data.get('g0',self._data['g']), 'gf' : data.get('gf',self._data['g'])})
        self._query_skips += ['J','g']

    def set_params_func(self):

        self.params_func = {
            'J': self.path.make_function(self.J0, self.Jf), 
            'g': self.path.make_function(self.g0, self.gf)
        }

    @property
    def mongo_type(self):
        from ._data import MongoDynamicPottsModel
        return MongoDynamicPottsModel