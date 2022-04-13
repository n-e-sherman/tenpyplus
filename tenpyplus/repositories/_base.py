




class Repository:

    def __init__(self, options):
        pass

    def load(self, obj):
        return False
        

    def save(self, obj):
        pass

    def _hash(self, obj):
        res = obj.__class__.__name__
        query = obj.get_query()
        for k,v in query.items():
            res += '-'+k+'='+str(v)
        return res
