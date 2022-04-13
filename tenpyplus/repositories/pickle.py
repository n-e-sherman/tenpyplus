from ._base import Repository

class PickleRepository(Repository):
    
    def __init__(self, options, model):
        super().__init__(options, model)
        
    def write(self, *args, **kwargs):
        file, df = args
        df.to_csv(self.results_dir + file, index=False)
    
    def save(self, *args, **kwargs):
        file, data = args
        with open(self.data_dir + file, 'wb') as f:
            for k,v in data.items():
                # print(k)
                pickle.dump(v, f)
                
    def log(self, *args, **kwargs):
        file, df = args
        df.to_csv(self.log_dir + file, index=False)
        
    def load(self, *args, **kwargs):
        file, data = args
        if not os.path.exists(self.data_dir + file):
            return False
        try:
            with open(self.data_dir + file, 'rb') as f:
                for key in data:
                    data[key] = pickle.load(f)
            return True
        except:
            return False