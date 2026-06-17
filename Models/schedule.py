class Schedule:
    def __init__(self, schedule_id, member_id, trainer_id, time_slot):
        self._schedule_id = schedule_id
        self._member_id = member_id
        self._trainer_id = trainer_id
        self._time_slot = time_slot

    @property
    def schedule_id(self): return self._schedule_id
    
    @property
    def member_id(self): return self._member_id
    
    @property
    def trainer_id(self): return self._trainer_id
    
    @property
    def time_slot(self): return self._time_slot

    def to_dict(self):
        return {
            "schedule_id": self.schedule_id,
            "member_id": self.member_id,
            "trainer_id": self.trainer_id,
            "time_slot": self.time_slot
        }