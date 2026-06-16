import json
import os
from Models.standard import StandardMembership
from Models.premium import PremiumMembership
from Models.vip import VIPMembership

class MembershipService:
    def __init__(self, file_path="Data/memberships.json"):
        self.file_path = file_path
        self.members = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            self.members = []
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.members = []
                for d in data:
                    if d['type'] == "Standard":
                        m = StandardMembership(d['member_id'], d['name'], d['phone'])
                    elif d['type'] == "Premium":
                        m = PremiumMembership(d['member_id'], d['name'], d['phone'])
                    elif d['type'] == "VIP":
                        m = VIPMembership(d['member_id'], d['name'], d['phone'])
                    self.members.append(m)
        except Exception:
            self.members = []

    def save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.members], f, ensure_ascii=False, indent=4)

    def add_member(self, member):
        """1. Add Member"""
        self.members.append(member)
        self.save_data()

    def get_all_members(self):
        """2. View Members"""
        return self.members

    def update_member(self, member_id, new_name, new_phone) -> bool:
        """3. Update Member"""
        for m in self.members:
            if m.member_id == member_id:
                m._name = new_name
                m._phone = new_phone
                self.save_data()
                return True
        return False

    def delete_member(self, member_id) -> bool:
        """4. Delete Member"""
        for i, m in enumerate(self.members):
            if m.member_id == member_id:
                self.members.pop(i)
                self.save_data()
                return True
        return False