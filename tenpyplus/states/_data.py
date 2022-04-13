import mongoengine
import os
import pickle
import pandas as pd
from tenpyplus.infrastructure import MongoDynamicDocument
from tenpyplus.models import MongoModelBase
from tenpyplus.evolvers import MongoEvolverBase
from tenpyplus.solvers import MongoSolverBase
from tenpyplus.observers import MongoObserverBase

from ._base import State
from .kzm import KZMState
from .ground import GroundState

from tenpy.networks.mps import MPS





class MongoStateBase(MongoDynamicDocument):

    _object = State

    directory = mongoengine.StringField(required=True, default=os.environ.get('data_dir', os.path.join(os.getcwd(), '.data/') ))
    initial = mongoengine.StringField()
    chi = mongoengine.FloatField(required=True)

    def __init__(self, *args, **kwargs):

        psi = kwargs.pop('psi') if 'psi' in kwargs else None
        super().__init__(*args, **kwargs)
        self.make_dir()
        self.save()
        self.put_psi(psi)

    def modify(self, *args, **kwargs):

        psi = kwargs.pop('psi') if 'psi' in kwargs else None
        super().modify(*args, **kwargs)
        self.put_psi(psi) ### <---- don't need to replace anything if 'psi' is not in kwargs

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if os.path.exists(self.psi_path):
            os.remove(self.psi_path)

    def put_psi(self, psi):
        if isinstance(psi, MPS):
            with open(self.psi_path, 'wb') as f:
                pickle.dump(psi, f)

    def read_psi(self):
        try:
            with open(self.psi_path, 'rb') as f:
                psi = pickle.load(f)
            return psi
        except:
            print('could not read psi')
            self.load_failed = True
            return None

    def make_dir(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @property
    def psi_path(self):
        if self.id is None:
            return ''
        else:
            return os.path.join(self.directory, f'{self.id}.data')

    def _to_dict(self):
        data = super()._to_dict()
        data['psi'] = self.read_psi()
        return data

    def _to_object_dict(self):
        data = super()._to_object_dict()
        data['psi'] = self.read_psi()
        return data

    meta = {'allow_inheritance': True}
    
class MongoGroundState(MongoStateBase):

    _object = GroundState

    E0 = mongoengine.FloatField(required=True, default=0)
    model = mongoengine.EmbeddedDocumentField(MongoModelBase, Required=True)
    solver = mongoengine.EmbeddedDocumentField(MongoSolverBase, Required=True)    

    def _to_object_dict(self):
        data = super()._to_object_dict()
        data['model'] = self.model.to_object()
        data['solver'] = self.solver.to_object()
        return data
    
class MongoKZMState(MongoStateBase):
    
    _object = KZMState

    
    model = mongoengine.EmbeddedDocumentField(MongoModelBase, required=True)
    evolver = mongoengine.EmbeddedDocumentField(MongoEvolverBase, Required=True)

    observer = mongoengine.EmbeddedDocumentField(MongoObserverBase, required=False)

    def __init__(self, *args, **kwargs):

        log = kwargs.pop('log') if 'log' in kwargs else None
        super().__init__(*args, **kwargs)
        self.put_log(log)

    def modify(self, *args, **kwargs):

        log = kwargs.pop('log') if 'log' in kwargs else None
        super().modify(*args, **kwargs)
        self.put_log(log)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def put_log(self, log):
        if log is None:
            return
        log.to_csv(self.log_path, index=False)

    def read_log(self):
        try:
            with open(self.log_path, 'rb') as f:
                log = pd.read_csv(f)
            return log
        except:
            return None

    @property
    def log_path(self):
        if self.id is None:
            return ''
        else:
            return os.path.join(self.directory, f'{self.id}.log')

    def _to_dict(self):
        data = super()._to_dict()
        data['log'] = self.read_log()
        return data
    
    def _to_object_dict(self):
        data = super()._to_object_dict()
        if self.observer is not None:
            data['observer'] = self.observer.to_object()
        data['model'] = self.model.to_object()
        data['evolver'] = self.evolver.to_object()
        data['log'] = self.read_log()
        return data
    
# class MongoGroundStateTemp(MongoStateBase):

#     _object = GroundState

#     E0 = mongoengine.FloatField(required=True, default=0)
#     model = mongoengine.EmbeddedDocumentField(MongoModelBase, Required=True)
#     solver = mongoengine.EmbeddedDocumentField(MongoSolverBase, Required=True)    

#     def _to_object_dict(self):
#         data = super()._to_object_dict()
#         data['model'] = self.model.to_object()
#         data['solver'] = self.solver.to_object()
#         return data
    
# class MongoKZMStateTemp(MongoStateBase):
    
#     _object = KZMState

    
#     model = mongoengine.EmbeddedDocumentField(MongoModelBase, required=True)
#     evolver = mongoengine.EmbeddedDocumentField(MongoEvolverBase, Required=True)

#     observer = mongoengine.EmbeddedDocumentField(MongoObserverBase, required=False)

#     def __init__(self, *args, **kwargs):

#         log = kwargs.pop('log') if 'log' in kwargs else None
#         super().__init__(*args, **kwargs)
#         self.put_log(log)

#     def modify(self, *args, **kwargs):

#         log = kwargs.pop('log') if 'log' in kwargs else None
#         super().modify(*args, **kwargs)
#         self.put_log(log)

#     def delete(self, *args, **kwargs):
#         super().delete(*args, **kwargs)
#         if os.path.exists(self.log_path):
#             os.remove(self.log_path)

#     def put_log(self, log):
#         if log is None:
#             return
#         log.to_csv(self.log_path, index=False)

#     def read_log(self):
#         try:
#             with open(self.log_path, 'rb') as f:
#                 log = pd.read_csv(f)
#             return log
#         except:
#             print('could not read log')
#             return None

#     @property
#     def log_path(self):
#         if self.id is None:
#             return ''
#         else:
#             return os.path.join(self.directory, f'{self.id}.log')

#     def _to_dict(self):
#         data = super()._to_dict()
#         data['log'] = self.read_log()
#         return data
    
#     def _to_object_dict(self):
#         data = super()._to_object_dict()
#         if self.observer is not None:
#             data['observer'] = self.observer.to_object()
#         data['model'] = self.model.to_object()
#         data['evolver'] = self.evolver.to_object()
#         data['log'] = self.read_log()
#         return data
    
    
    
