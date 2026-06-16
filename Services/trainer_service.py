import json
import os
from Models.trainer import Trainer
from Models.schedule import Schedule

class TrainerService:
    def __init__(self, trainer_path="Data/trainers.json", schedule_path="Data/schedules.json"):
        self.trainer_path = trainer_path
        self.schedule_path = schedule_path
        self.trainers = []
        self.schedules = []
        self.load_data()

    def load_data(self):
        # Đọc dữ liệu huấn luyện viên
        if os.path.exists(self.trainer_path) and os.stat(self.trainer_path).st_size > 0:
            with open(self.trainer_path, 'r', encoding='utf-8') as f:
                self.trainers = [Trainer(d['trainer_id'], d['name'], d['specialty']) for d in json.load(f)]
        # Đọc dữ liệu lịch tập
        if os.path.exists(self.schedule_path) and os.stat(self.schedule_path).st_size > 0:
            with open(self.schedule_path, 'r', encoding='utf-8') as f:
                self.schedules = [Schedule(d['schedule_id'], d['member_id'], d['trainer_id'], d['time_slot']) for d in json.load(f)]

    def save_trainers(self):
        os.makedirs(os.path.dirname(self.trainer_path), exist_ok=True)
        with open(self.trainer_path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.trainers], f, ensure_ascii=False, indent=4)

    def save_schedules(self):
        os.makedirs(os.path.dirname(self.schedule_path), exist_ok=True)
        with open(self.schedule_path, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self.schedules], f, ensure_ascii=False, indent=4)

    def add_trainer(self, trainer):
        self.trainers.append(trainer)
        self.save_trainers()

    def add_schedule(self, schedule):
        self.schedules.append(schedule)
        self.save_schedules()