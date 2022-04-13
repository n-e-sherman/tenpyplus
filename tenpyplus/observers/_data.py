
from tenpyplus.infrastructure import MongoDynamicEmbeddedDocument
import mongoengine
from ._base import Observer
from .staggeredfield import StaggeredFieldObserver

class MongoObserverBase(MongoDynamicEmbeddedDocument):

    _object = Observer
    
    meta = {'allow_inheritance': True}

class MongoStaggeredFieldObserver(MongoObserverBase):

    _object = StaggeredFieldObserver