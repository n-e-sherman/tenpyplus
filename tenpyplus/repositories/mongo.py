from ._base import Repository
import os
import mongoengine

class MongoRepository(Repository):

    loaded = True
    cache = {}
    def __init__(self, options):

        self.cache = {}
        loaded = True
        db = options.get('db',os.environ.get('db', 'Research'))
        
        mongoengine.disconnect()
        mongoengine.connect(db)
        self._load = options.get('load', True)

    def load(self, obj):

        if not self._load:
            print('self._load turned off')
            return False
        document = self._get_document(obj)
        if self.loaded:
            try:
                data = document.to_dict()
                if not document.load_failed:
                    obj.update(**data)
                    return True
                print('to_dict not loaded')
            except:
                print('document.to_dict failed, trying to_object_dict')
            try:
                data = document.to_object_dict()
                if not document.load_failed:
                    obj.update(**data)
                    return True
                print('to_object_dict not loaded')
            except:
                pass
            print('load failed')
        print('document not in db')
        return False

    def save(self, obj):

        document = self._get_document(obj)
        data = obj.to_mongo_dict()
        document.modify(**data)
        document.save()


    def _get_document(self, obj):

        key = self._hash(obj)
        if key in self.cache:
            return self.cache[key]


        query = obj.get_query()
        mongo_type = obj.mongo_type

        try: # got document
            document = mongo_type.objects.get(**query)

        except mongoengine.MultipleObjectsReturned: # duplicates in db
            document = obj.mongo_resolve_multiple(mongo_type.objects(**query))

        except mongoengine.DoesNotExist:
            document = self._create_document(obj)
            self.loaded = False
            
        self.cache[key] = document

        return document

    def _create_document(self, obj):

        document = obj.to_mongo()
        document.save()
        self.cache[self._hash(obj)] = document
        return document


