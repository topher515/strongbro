class ClassRegistry(dict):

    def register(self, class_):
        self[class_.__name__] = class_

    @property
    def choices(self):
        return [(k,k) for k in self.keys()]