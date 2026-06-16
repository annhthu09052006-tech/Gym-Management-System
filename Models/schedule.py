class Schedule:
    def __init__(self, schedule_id, member_id, trainer_id, time_slot):
        self.schedule_id = schedule_id
        self.member_id = member_id
        self.trainer_id = trainer_id
        self.time_slot = time_slot

    def to_dict(self):
        return {
            "schedule_id": self.schedule_id, 
            "member_id": self.member_id, 
            "trainer_id": self.trainer_id, 
            "time_slot": self.time_slot
        }