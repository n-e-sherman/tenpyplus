from .paths import MongoDirectPath
from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument
import mongoengine
from ._base import Model, DynamicModel
from .ising import IsingModel, DynamicIsingModel
from .xx import XXModel, DynamicXXModel
from .potts import PottsModel, DynamicPottsModel

class MongoModelBase(MongoDynamicEmbeddedDocument):

    _object = Model

    L = mongoengine.IntField(required=True)
    conserve = mongoengine.StringField(required=True)
    bc = mongoengine.StringField(required=True)
    
    meta = {'allow_inheritance': True}


class MongoDynamicModelBase(MongoModelBase):

    _object = DynamicModel

    t = mongoengine.FloatField(required=True, default=0)
    path = mongoengine.EmbeddedDocumentField(MongoDirectPath, Required=True)

    meta = {'allow_inheritance': True}
    
    def _to_object_dict(self):
        data = super()._to_object_dict()
        data['path'] = self.path.to_object()
        return data
   

class MongoIsingModel(MongoModelBase):
    
    _object = IsingModel

    J = mongoengine.FloatField(required=True, default=0)
    g = mongoengine.FloatField(required=True, default=0)
    h = mongoengine.FloatField(required=True, default=0)

class MongoDynamicIsingModel(MongoDynamicModelBase):

    _object = DynamicIsingModel


    
    J = mongoengine.FloatField(required=True, default=0)
    J0 = mongoengine.FloatField(Required=True, default=0)
    Jf = mongoengine.FloatField(Required=True, default=0)

    g = mongoengine.FloatField(required=True, default=0)
    g0 = mongoengine.FloatField(Required=True, default=0)
    gf = mongoengine.FloatField(Required=True, default=0)

    h = mongoengine.FloatField(required=True, default=0)
    h0 = mongoengine.FloatField(Required=True, default=0)
    hf = mongoengine.FloatField(Required=True, default=0)

class MongoPottsModel(MongoModelBase):
    
    _object = PottsModel

    J = mongoengine.FloatField(required=True, default=0)
    g = mongoengine.FloatField(required=True, default=0)

class MongoDynamicPottsModel(MongoDynamicModelBase):

    _object = DynamicPottsModel

    J = mongoengine.FloatField(required=True, default=0)
    J0 = mongoengine.FloatField(Required=True, default=0)
    Jf = mongoengine.FloatField(Required=True, default=0)

    g = mongoengine.FloatField(required=True, default=0)
    g0 = mongoengine.FloatField(Required=True, default=0)
    gf = mongoengine.FloatField(Required=True, default=0)

class MongoXXModel(MongoModelBase):

    _object = XXModel

    J = mongoengine.FloatField(Required=True, default=0)
    h = mongoengine.FloatField(Required=True, default=0)

class MongoDynamicXXModel(MongoDynamicModelBase):

    _object = DynamicXXModel

    J = mongoengine.FloatField(Required=True, default=0)
    J0 = mongoengine.FloatField(Required=True, default=0)
    Jf = mongoengine.FloatField(Required=True, default=0)

    h = mongoengine.FloatField(Required=True, default=0)
    h0 = mongoengine.FloatField(Required=True, default=0)
    hf = mongoengine.FloatField(Required=True, default=0)





