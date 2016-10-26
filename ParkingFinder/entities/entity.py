from schematics.models import Model

class Entity(Model):

    def __str__(self):
        return self.to_primitive()
