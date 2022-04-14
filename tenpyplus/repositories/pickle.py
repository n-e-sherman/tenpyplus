from ._base import Repository
import os
import pickle
import hashlib
import json
import pandas as pd


class PickleRepository(Repository):
    
    def __init__(self, options):
        self.data_dir = os.environ.get('data_dir', os.path.join(os.getcwd(), '.data/'))
        self.res_dir = os.environ.get('res_dir', os.path.join(os.getcwd(), '.results/'))
        self._load = options.get('load', True)

        self.make_dirs(self.data_dir)
        self.make_dirs(self.res_dir)

    def make_dirs(self, file):
        if not os.path.exists(file):
            os.makedirs(file)

    
    def load(self, obj):

        if not self._load:
            print('self._load turned off')
            return False

        _hash = self._hash(obj)
        _dir = obj._dir_choice(self.data_dir, self.res_dir)
        file = os.path.join(_dir, _hash)
        if not os.path.exists(file):
            print('pickle file does not exist')
            return False

        _type = obj.pickle_type
        if _type == 'check_point':
            return self._load_check_point(file, obj)
        elif _type == 'data_frame':
            return self._load_data_frame(file, obj)
        else:
            raise NotImplementedError('pickle_type ' + _type + ' is not implemented.' )

    def _load_check_point(self, file, obj):
        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)
        except:
            print('pickle check_point load failed')
            return False
        obj.update(**data)
        return True

    def _load_data_frame(self, file, obj):

        try:
            datadf = pd.read_csv(file)
            data = datadf.to_dict()
        except:
            print('pickle data_frame load failed')
            return False
        obj.update(**data)
        return True

    def save(self, obj):
        _hash = self._hash(obj)
        _dir = obj._dir_choice(self.data_dir, self.res_dir)
        self.make_dirs(_dir)
        file = os.path.join(_dir, _hash)
        _type = obj.pickle_type
        if _type == 'check_point':
            return self._save_check_point(file, obj)
        elif _type == 'data_frame':
            return self._save_data_frame(file, obj)
        else:
            raise NotImplementedError('pickle_type ' + _type + ' is not implemented.' )
        
    

    def _save_check_point(self, file, obj):

        data = obj.to_dict()
        try:
            with open(file, 'wb') as f:
                pickle.dump(data, f)
        except:
            print('pickle check_point save failed')
            return False

    def _save_data_frame(self, file, obj):

        data = obj.to_dict()
        try:
            df = pd.DataFrame(data)
        except ValueError:
            df = pd.DataFrame([data])
        except:
            print('pickle data_frame save failed')
            return False

        df.to_csv(file, index=False)

    def _hash(self, obj):

        query = obj.get_query()
        dhash = hashlib.md5()
        encoded = json.dumps(query, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

