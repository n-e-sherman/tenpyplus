from tenpyplus.infrastructure import Object

class State(Object):

    def __init__(self, **data):
        super().__init__(**data)
        
        

    def _set_data(self, **data):
        super()._set_data(**data)
        self._data.update({'chi' : data.get('chi', None), 
                           'psi' : data.get('psi',None)})
        self._label_skips.append('psi')
        self._query_skips.append('psi')

    @property
    def mongo_type(self):
        from ._data import MongoStateBase
        return MongoStateBase
