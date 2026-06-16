import tkinter as tk
from tkinter import ttk, messagebox
from Services.membership_service import MembershipService
from Services.trainer_service import TrainerService
from Services.report_service import ReportService
from Models.standard import StandardMembership
from Models.premium import PremiumMembership
from Models.vip import VIPMembership

class ManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG QUẢN LÝ TRUNG TÂM GYM")
        self.root.geometry("900x600")
        
        # Khởi tạo các dịch vụ nghiệp vụ
        self.mem_service = MembershipService()
        self.train_service = TrainerService()
        self.rep_service = ReportService(self.mem_service)
        
        # Thiết kế giao diện bố cục chính (Gồm Form nhập bên trái và Bảng bên phải)
        self.create_widgets()
        self.load_member_data()

    def create_widgets(self):
        # ---- KHUNG TIÊU ĐỀ ----
        title_label = tk.Label(self.root, text="GYM MANAGEMENT SYSTEM", font=("Helvetica", 18, "bold"), fg="blue")
        title_label.pack(pady=10)

        # ---- LÀM KIẾN TRÚC CHIA ĐÔI MÀN HÌNH ----
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 1. Khung bên trái: Nhập thông tin (Form nhập liệu)
        form_frame = tk.LabelFrame(main_frame, text=" Thông tin Hội Viên ", font=("Helvetica", 11, "bold"), padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(form_frame, text="Mã Hội Viên (ID):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_id = tk.Entry(form_frame, width=22)
        self.ent_id.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Tên Khách Hàng:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ent_name = tk.Entry(form_frame, width=22)
        self.ent_name.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Số Điện Thoại:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ent_phone = tk.Entry(form_frame, width=22)
        self.ent_phone.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Hạng Thẻ Tập:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cbo_tier = ttk.Combobox(form_frame, values=["Standard", "Premium", "VIP"], width=19, state="readonly")
        self.cbo_tier.current(0)
        self.cbo_tier.grid(row=3, column=1, pady=5)

        # Khung chứa các nút chức năng quản lý CRUD
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Thêm Mới", width=10, bg="#4CAF50", fg="white", command=self.add_member).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Sửa SĐT/Tên", width=10, bg="#2196F3", fg="white", command=self.update_member).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Xóa", width=10, bg="#F44336", fg="white", command=self.delete_member).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Làm Trống", width=10, bg="#9E9E9E", fg="white", command=self.clear_entries).grid(row=1, column=1, padx=5, pady=5)

        # Khung công cụ Tìm kiếm & Thống kê
        tool_frame = tk.LabelFrame(form_frame, text=" Tiện ích nâng cao ", padx=5, pady=5)
        tool_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)

        self.ent_search = tk.Entry(tool_frame, width=13)
        self.ent_search.grid(row=0, column=0, padx=2, pady=5)
        tk.Button(tool_frame, text="Tìm Kiếm", command=self.search_member, bg="#FF9800", fg="white").grid(row=0, column=1, padx=2, pady=5)
        tk.Button(tool_frame, text="Xếp A-Z", command=self.sort_members, width=8).grid(row=0, column=2, padx=2, pady=5)

        tk.Button(tool_frame, text="Báo Cáo Doanh Thu & Xuất CSV", bg="#9C27B0", fg="white", command=self.show_statistics).grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=5)

        # 2. Khung bên phải: Hiển thị danh sách bảng Grid (Treeview)
        data_frame = tk.LabelFrame(main_frame, text=" Danh Sách Hội Viên Hiện Có ", font=("Helvetica", 11, "bold"), padx=5, pady=5)
        data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Thiết lập bảng hiển thị Treeview
        columns = ("id", "name", "phone", "tier", "fee")
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="Mã Hội Viên")
        self.tree.heading("name", text="Tên Khách Hàng")
        self.tree.heading("phone", text="Số Điện Thoại")
        self.tree.heading("tier", text="Hạng Thẻ")
        self.tree.heading("fee", text="Học Phí (VND)")

        self.tree.column("id", width=90, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("phone", width=100, anchor=tk.CENTER)
        self.tree.column("tier", width=90, anchor=tk.CENTER)
        self.tree.column("fee", width=110, anchor=tk.E)

        # Tạo thanh cuộn cho bảng dữ liệu
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sự kiện click chuột chọn dòng trong bảng để tự điền dữ liệu lên form nhập
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # ---- CÁC HÀM XỬ LÝ SỰ KIỆN / NGHIỆP VỤ ----

    def load_member_data(self, member_list=None):
        """Nạp dữ liệu vào bảng hiển thị trực quan"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if member_list is None:
            member_list = self.mem_service.get_all_members()
            
        for m in member_list:
            tier_name = m.__class__.__name__.replace("Membership", "")
            self.tree.insert("", tk.END, values=(
                m.member_id, 
                m.name, 
                m.phone, 
                tier_name, 
                f"{m.calculate_fee():,}"
            ))

    def on_tree_select(self, event):
        """Tự động điền thông tin khi nhấn chuột chọn dòng trong bảng"""
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        
        self.clear_entries()
        self.ent_id.insert(0, values[0])
        self.ent_name.insert(0, values[1])
        self.ent_phone.insert(0, values[2])
        self.cbo_tier.set(values[3])

    def add_member(self):
        m_id = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        phone = self.ent_phone.get().strip()
        tier = self.cbo_tier.get()

        if not m_id or not name or not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ các thông tin!")
            return

        if tier == "Standard": m = StandardMembership(m_id, name, phone)
        elif tier == "Premium": m = PremiumMembership(m_id, name, phone)
        elif tier == "VIP": m = VIPMembership(m_id, name, phone)

        self.mem_service.add_member(m)
        messagebox.showinfo("Thành công", f"Đã thêm thành công hội viên {name}!")
        self.load_member_data()
        self.clear_entries()

    def update_member(self):
        m_id = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        phone = self.ent_phone.get().strip()

        if not m_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoặc nhập Mã hội viên cần sửa!")
            return

        if self.mem_service.update_member(m_id, name, phone):
            messagebox.showinfo("Thành công", "Cập nhật thông tin hội viên thành công!")
            self.load_member_data()
            self.clear_entries()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy hội viên có mã này trong hệ thống!")

    def delete_member(self):
        m_id = self.ent_id.get().strip()
        if not m_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập hoặc chọn mã hội viên muốn xóa!")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa hội viên {m_id} không?")
        if confirm:
            if self.mem_service.delete_member(m_id):
                messagebox.showinfo("Thành công", "Đã xóa hội viên thành công!")
                self.load_member_data()
                self.clear_entries()
            else:
                messagebox.showerror("Lỗi", "Mã hội viên không tồn tại!")
    def search_member(self):
        keyword = self.ent_search.get().strip()
        if not keyword:
            self.load_member_data()
            return
        results = self.mem_service.search_member(keyword)
        self.load_member_data(results)

    def sort_members(self):
        sorted_list = self.mem_service.sort_members_by_name()
        self.load_member_data(sorted_list)
        messagebox.showinfo("Thông báo", "Đã sắp xếp danh sách hội viên theo thứ tự A-Z!")

    def show_statistics(self):
        stats, total = self.rep_service.get_revenue_by_tier()
        msg = "--- THỐNG KÊ DOANH THU THEO GÓI TẬP ---\n"
        for tier, fee in stats.items():
            msg += f"• Thẻ {tier}: {fee:,} VND\n"
        msg += f"\n💵 TỔNG DOANH THU: {total:,} VND\n\n"
        msg += "Bạn có muốn đồng thời xuất báo cáo này ra tệp dữ liệu CSV hay không?"
        
        export_confirm = messagebox.askyesno("Thống kê doanh thu", msg)
        if export_confirm:
            path = self.rep_service.export_csv()
            messagebox.showinfo("Xuất dữ liệu", f"Đã xuất tệp báo cáo thành công tại thư mục:\n{path}")

    def clear_entries(self):
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.cbo_tier.current(0)