
from tenpyplus.infrastructure import MongoDynamicDocument
import mongoengine
from ._base import Measurement
from .measurement import StateMeasurement, IsingCriticalMeasurement, XXSineGordonMassMeasurement, IsingGroundStateOverlapMeasurement, KZMSweepMeasurement

class MongoMeasurementBase(MongoDynamicDocument):

    _object = Measurement
    
    # state params
    state = mongoengine.StringField()
    chi = mongoengine.FloatField()
    initial = mongoengine.StringField()

    # model params
    model = mongoengine.StringField()
    g = mongoengine.FloatField()
    J = mongoengine.FloatField()
    h = mongoengine.FloatField()
    L = mongoengine.IntField()
    conserve = mongoengine.StringField()
    bc = mongoengine.StringField()

    # dynamic model params
    g0 = mongoengine.FloatField()
    J0 = mongoengine.FloatField()
    h0 = mongoengine.FloatField()
    path = mongoengine.StringField()
    v = mongoengine.FloatField()
    ramp = mongoengine.StringField()

    # evolver params
    evolver = mongoengine.StringField()
    dt = mongoengine.FloatField()
    order = mongoengine.IntField()

    # solver params
    solver = mongoengine.StringField()
    sites = mongoengine.IntField()

    meta = {'allow_inheritance': True}

class MongoStateMeasurement(MongoMeasurementBase):

    _object = StateMeasurement

    E = mongoengine.FloatField()
    S = mongoengine.FloatField()
    Sx = mongoengine.FloatField()
    Sy = mongoengine.FloatField()
    Sz = mongoengine.FloatField()
    xi = mongoengine.FloatField()

class MongoIsingCriticalMeasurement(MongoMeasurementBase):

    _object = IsingCriticalMeasurement

    Ec = mongoengine.FloatField()
    S = mongoengine.FloatField()

class MongoKZMSweepMeasurement(MongoMeasurementBase):

    _object = KZMSweepMeasurement

    l = mongoengine.FloatField()
    Ep = mongoengine.FloatField()
    E0 = mongoengine.FloatField()
    Ec = mongoengine.FloatField()
    conserve = mongoengine.StringField()

class MongoXXSineGordonMassMeasurement(MongoMeasurementBase):

    _object = XXSineGordonMassMeasurement
    E = mongoengine.FloatField()
    m = mongoengine.FloatField()

class MongoIsingGroundStateOverlapMeasurement(MongoMeasurementBase):

    _object = IsingGroundStateOverlapMeasurement

    O = mongoengine.FloatField()
    m = mongoengine.FloatField()
    mc = mongoengine.FloatField()
