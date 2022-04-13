import mongoengine
from ._base import Solver
from .dmrg import DMRGSolver
from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument

class MongoSolverBase(MongoDynamicEmbeddedDocument):
        
    _object = Solver
    meta = {'allow_inheritance': True}
    
class MongoDMRGSolver(MongoSolverBase):
    
    _object = DMRGSolver
    sites = mongoengine.IntField(Required=True)
    mixer = mongoengine.BooleanField(required=True)