from ._base import Evolver
import tenpyplus.evolvers as evolvers

from tenpy.algorithms import tebd
import tenpy.linalg.np_conserved as npc
from tenpy.networks.mps import TransferMatrix

class UTEBDEvolver(Evolver):
    
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
        return self._make_uniform(psi)

    def _make_uniform(self, psi):

        res = psi.copy()
        #RCF
        TB = TransferMatrix(psi, psi, shift_bra=1, shift_ket=0)
        es_B, evs_B = TB.eigenvectors()
        U = evs_B[0].split_legs(['(vL.vL*)']).iset_leg_labels(['vL','vR'])
        _B = psi.get_B(1)
        B = npc.tensordot(_B, U, axes=('vR','vL'))
        res.set_B(0, B)
        res.set_B(1, B)
        res.canonical_form()
        return res
    
    @property
    def mongo_type(self):
        from ._data import MongoUTEBDEvolver
        return MongoUTEBDEvolver

    