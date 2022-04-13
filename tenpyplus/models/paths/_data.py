from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument
from .path import DirectPath, SymmetricPath
import mongoengine

class MongoDirectPath(MongoDynamicEmbeddedDocument):

    _object = DirectPath

    ramp = mongoengine.StringField(required=True)
    v = mongoengine.FloatField(required=True)
    dt = mongoengine.FloatField(required=True)
    
    meta = {'allow_inheritance': True}

class MongoSymmetricPath(MongoDirectPath):

    _object = SymmetricPath