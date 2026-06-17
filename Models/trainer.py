class Trainer:
    def __init__(self, trainer_id, name, specialty):
        self._trainer_id = trainer_id
        self._name = name
        self._specialty = specialty

    @property
    def trainer_id(self): return self._trainer_id
    
    @property
    def name(self): return self._name
    
    @property
    def specialty(self): return self._specialty

    def to_dict(self):
        return {"trainer_id": self.trainer_id, "name": self.name, "specialty": self.specialty}