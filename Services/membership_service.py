import json
import os
from Models.standard import StandardMembership
from Models.premium import PremiumMembership
from Models.vip import VIPMembership

class MembershipService:
    def __init__(self, file_path="data/memberships.json"):
        self.file_path = file_path
        self.members = []
        self.load_data()

    def load_data(self):
        """Tự động đọc dữ liệu từ file JSON khi khởi động phần mềm"""
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            self.members = []
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                for d in data_list:
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
        """Lưu vĩnh viễn dữ liệu vào tệp JSON"""
        # Đảm bảo thư mục data/ tồn tại
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.members], f, ensure_ascii=False, indent=4)

    def add_membership(self, membership):
        """Thêm mới một hội viên (Nghiệp vụ CRUD)"""
        self.members.append(membership)
        self.save_data()

    def get_all_memberships(self):
        """Xem toàn bộ danh sách hội viên (Nghiệp vụ CRUD)"""
        return self.members
    
    def search_by_id_or_name(self, keyword: str):
        """Tìm kiếm hội viên theo định danh Mã hoặc Tên (Yêu cầu 4.1)"""
        result = []
        for m in self.members:
            if keyword.lower() in m.member_id.lower() or keyword.lower() in m.name.lower():
                result.append(m)
        return result

    def get_members_sorted_by_name(self):
        """Sắp xếp danh sách hội viên theo bảng chữ cái A-Z (Yêu cầu 4.1)"""
        return sorted(self.members, key=lambda m: m.name)