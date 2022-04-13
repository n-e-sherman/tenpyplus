import mongoengine
from ._base import Evolver
from .tebd import TEBDEvolver
from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument

class MongoEvolverBase(MongoDynamicEmbeddedDocument):
    
    _object = Evolver
    dt = mongoengine.FloatField(required=True)
        
    meta = {'allow_inheritance': True}
    
class MongoTEBDEvolver(MongoEvolverBase):
    
    _object = TEBDEvolver
    order = mongoengine.IntField(required=True)
    optimum = mongoengine.BooleanField(required=True, default=False)
