import csv
import os
from Services.membership_service import MembershipService

class ReportService:
    def __init__(self, membership_service: MembershipService):
        self.membership_service = membership_service

    def calculate_total_revenue(self) -> float:
        """Tính tổng số tiền thu được dựa vào Đa hình phương thức tính phí"""
        total = 0
        members = self.membership_service.get_all_memberships()
        for m in members:
            total += m.calculate_fee()
        return total

    def export_revenue_report(self, filepath="data/bao_cao_doanh_thu.csv"):
        """Xuất báo cáo dữ liệu định dạng CSV (Yêu cầu 4.2 nâng cao)"""
        members = self.membership_service.get_all_memberships()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Mã Hội Viên", "Tên Khách Hàng", "Số Điện Thoại", "Hạng Thẻ", "Học Phí Gói Tập (VND)"])
            
            for m in members:
                tier_name = m.__class__.__name__.replace("Membership", "")
                writer.writerow([m.member_id, m.name, m.phone, tier_name, f"{m.calculate_fee():,}"])
                
            writer.writerow([])
            writer.writerow(["TỔNG DOANH THU HỆ THỐNG", "", "", "", f"{self.calculate_total_revenue():,} VND"])
        return filepath