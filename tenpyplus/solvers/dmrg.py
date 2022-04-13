from ._base import Solver
from tenpy.algorithms import dmrg


class DMRGSolver(Solver):
    
    def __init__(self, **data):
        super().__init__(**data)
        self._data.update({'sites' : data.get('sites', 2),
                           'mixer' : data.get('mixer', True)})
        self.engine = dmrg.TwoSiteDMRGEngine
        if self.sites == 1:
            self.engine = dmrg.SingleSiteDMRGEngine
        self._label_skips.append('mixer')
        
    def solve(self, psi, model):
        eng = self.engine(psi, model, self.options)
        return eng.run()

    @property
    def mongo_type(self):
        from ._data import MongoDMRGSolver
        return MongoDMRGSolver
