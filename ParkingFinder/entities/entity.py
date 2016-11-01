from schematics.models import Model

class Entity(Model):

    def __str__(self):
        return self.to_primitive()

    def __repr__(self):
        return str(self.to_primitive())