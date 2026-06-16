import csv
import os
from Services.membership_service import MembershipService

class ReportService:
    def __init__(self, membership_service: MembershipService):
        self.membership_service = membership_service

    def get_revenue_by_tier(self):
        """Thống kê doanh thu theo từng nhóm gói tập (Yêu cầu 11 nâng cao)"""
        stats = {"Standard": 0.0, "Premium": 0.0, "VIP": 0.0}
        total = 0.0
        for m in self.membership_service.get_all_members():
            tier = m.__class__.__name__.replace("Membership", "")
            fee = m.calculate_fee()
            if tier in stats:
                stats[tier] += fee
            total += fee
        return stats, total

    def export_csv(self, filepath="Data/gym_revenue_report.csv"):
        """Xuất báo cáo doanh thu ra file CSV (Yêu cầu 11 nâng cao)"""
        members = self.membership_service.get_all_members()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Mã Hội Viên", "Tên Khách Hàng", "Số Điện Thoại", "Hạng Thẻ", "Giá Gói Tập (VND)"])
            
            total_rev = 0
            for m in members:
                tier = m.__class__.__name__.replace("Membership", "")
                fee = m.calculate_fee()
                writer.writerow([m.member_id, m.name, m.phone, tier, f"{fee:,}"])
                total_rev += fee
                
            writer.writerow([])
            writer.writerow(["TỔNG DOANH THU TRUNG TÂM", "", "", "", f"{total_rev:,} VND"])
        return filepath