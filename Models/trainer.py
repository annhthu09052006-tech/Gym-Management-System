class Trainer:
    def __init__(self, trainer_id, name, specialty):
        self.trainer_id = trainer_id
        self.name = name
        self.specialty = specialty

    def to_dict(self):
        return {"trainer_id": self.trainer_id, "name": self.name, "specialty": self.specialty}