import mongoengine
from ._base import Evolver
from .tebd import TEBDEvolver
from .utebd import UTEBDEvolver
from .tebdvar import TEBDVarEvolver
from .wii import WIIEvolver
from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument

class MongoEvolverBase(MongoDynamicEmbeddedDocument):
    
    _object = Evolver
    dt = mongoengine.FloatField(required=True)
        
    meta = {'allow_inheritance': True}
    
class MongoTEBDEvolver(MongoEvolverBase):
    
    _object = TEBDEvolver
    order = mongoengine.IntField(required=True)
    optimum = mongoengine.BooleanField(required=True, default=False)

class MongoUTEBDEvolver(MongoEvolverBase):
    
    _object = UTEBDEvolver
    order = mongoengine.IntField(required=True)
    optimum = mongoengine.BooleanField(required=True, default=False)

class MongoTEBDVarEvolver(MongoEvolverBase):
    
    _object = TEBDVarEvolver
    order = mongoengine.IntField(required=True)
    optimum = mongoengine.BooleanField(required=True, default=False)


class MongoWIIEvolver(MongoEvolverBase):
    
    _object = WIIEvolver
    order = mongoengine.IntField(required=True)
    compression = mongoengine.StringField(required=True)
