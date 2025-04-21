import inspect

class CallableClass(type):
    def __call__(cls, *args, **kwargs):
        return cls.call(*args, **kwargs)

class Save(metaclass=CallableClass):
    _collection = []

    @classmethod
    def call(self, data):
        self._collection.append(data)
        return self._collection[-1]
    
class TkVariables():
    _collection = {}

    @classmethod
    def __setattr__(self, name, value):
        if name == '_collection':
            super().__setattr__(name, value)
        else:
            self._collection[name] = value

    @classmethod
    def __getattr__(self, name):
        if name in self._collection:
            return self._collection[name]
        raise AttributeError(f"'Saver' object has no attribute '{name}'")
