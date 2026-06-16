from Services.membership_service import MembershipService
from Services.trainer_service import TrainerService
from Services.report_service import ReportService
from Models.standard import StandardMembership
from Models.premium import PremiumMembership
from Models.vip import VIPMembership
from Models.trainer import Trainer
from Models.schedule import Schedule

class ConsoleMenu:
    def __init__(self):
        self.mem_service = MembershipService()
        self.train_service = TrainerService()
        self.rep_service = ReportService(self.mem_service)

    def show(self):
        while True:
            print("\n===== GYM MANAGEMENT =====")
            print("1. Add Member")
            print("2. View Members")
            print("3. Update Member")
            print("4. Delete Member")
            print("5. Search Member")
            print("6. Sort Members")
            print("7. Manage Trainers")
            print("8. Manage Schedule")
            print("9. Statistics")
            print("0. Exit")
            print("==========================")
            
            try:
                choice = int(input("Nhập lựa chọn của bạn: "))
                if choice == 1:
                    m_id = input("Nhập ID hội viên: ")
                    name = input("Nhập tên hội viên: ")
                    phone = input("Nhập số điện thoại: ")
                    tier = input("Hạng thẻ (Standard/Premium/VIP): ").strip()
                    
                    if tier.lower() == "standard": m = StandardMembership(m_id, name, phone)
                    elif tier.lower() == "premium": m = PremiumMembership(m_id, name, phone)
                    elif tier.lower() == "vip": m = VIPMembership(m_id, name, phone)
                    else:
                        print("❌ Hạng thẻ sai quy định!"); continue
                    self.mem_service.add_member(m)
                    print("🎉 Thêm hội viên thành công!")

                elif choice == 2:
                    print("\n--- DANH SÁCH HỘI VIÊN ---")
                    for m in self.mem_service.get_all_members():
                        t = m.__class__.__name__.replace("Membership", "")
                        print(f"[{t}] ID: {m.member_id} | Tên: {m.name} | SĐT: {m.phone} | Phí: {m.calculate_fee():,}đ")

                elif choice == 3:
                    m_id = input("Nhập ID hội viên cần sửa: ")
                    n_name = input("Nhập tên mới: ")
                    n_phone = input("Nhập SĐT mới: ")
                    if self.mem_service.update_member(m_id, n_name, n_phone):
                        print("🎉 Cập nhật thành công!")
                    else: print("❌ Không tìm thấy hội viên!")

                elif choice == 4:
                    m_id = input("Nhập ID hội viên cần xóa: ")
                    if self.mem_service.delete_member(m_id):print("🎉 Đã xóa thành công!")
                    else: print("❌ Không tìm thấy hội viên!")

                elif choice == 5:
                    kw = input("Nhập ID hoặc tên để tìm kiếm: ")
                    for m in self.mem_service.search_member(kw):
                        print(f"-> ID: {m.member_id} | Tên: {m.name} | SĐT: {m.phone}")

                elif choice == 6:
                    print("\n--- SẮP XẾP THEO TÊN A-Z ---")
                    for m in self.mem_service.sort_members_by_name():
                        print(f"-> Tên: {m.name} | ID: {m.member_id}")

                elif choice == 7:
                    t_id = input("Nhập ID huấn luyện viên: ")
                    t_name = input("Nhập tên huấn luyện viên: ")
                    spec = input("Nhập chuyên môn (Yoga/Cardio/Gym...): ")
                    self.train_service.add_trainer(Trainer(t_id, t_name, spec))
                    print("🎉 Đã thêm huấn luyện viên thành công!")

                elif choice == 8:
                    s_id = input("Nhập ID lịch tập: ")
                    m_id = input("Nhập ID hội viên: ")
                    t_id = input("Nhập ID Trainer: ")
                    slot = input("Nhập khung giờ tập (Ví dụ: 18h-20h): ")
                    self.train_service.add_schedule(Schedule(s_id, m_id, t_id, slot))
                    print("🎉 Xếp lịch tập thành công!")

                elif choice == 9:
                    stats, total = self.rep_service.get_revenue_by_tier()
                    print("\n--- THỐNG KÊ DOANH THU GÓI TẬP ---")
                    for tier, fee in stats.items():
                        print(f" * Thẻ {tier}: {fee:,} VND")
                    print(f"💵 Tổng doanh thu: {total:,} VND")
                    
                    csv_opt = input("Bạn có muốn xuất báo cáo thành file CSV không? (y/n): ")
                    if csv_opt.lower() == 'y':
                        path = self.rep_service.export_csv()
                        print(f"📊 Đã xuất file thành công tại: {path}")

                elif choice == 0:
                    print("👋 Hệ thống đang thoát..."); break
                else:
                    print("❌ Lựa chọn sai khoảng cách cho phép (0-9)!")
            except ValueError:
                print("❌ Lỗi đầu vào: Vui lòng nhập số, không gõ chữ tại Menu!")
            except Exception as e:
                print(f"❌ Hệ thống phát sinh lỗi: {e}")